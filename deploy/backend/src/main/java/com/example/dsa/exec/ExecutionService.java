package com.example.dsa.exec;

import com.example.dsa.catalog.Question;
import com.example.dsa.harness.HarnessGenerator;
import com.example.dsa.runner.JavaRunner;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Orchestrates compile + run for both execution modes:
 * <ul>
 *   <li><b>method mode</b>: wraps the user's {@code Solution} with a generated harness Main
 *       ({@code Solution.java} + {@code Harness.java} + {@code Main.java}).</li>
 *   <li><b>program mode</b>: compiles the user's complete program ({@code Main.java}) as-is.</li>
 * </ul>
 * Every compile and every test runs in a fresh sandbox container via the injected JavaRunner.
 */
@Service
public class ExecutionService {
    public static final int MAX_CODE = 30000;
    public static final int MAX_TESTS = 20;
    public static final int MAX_INPUT = 4000;

    private static final Duration COMPILE_TIMEOUT = Duration.ofSeconds(12);
    private static final Duration RUN_TIMEOUT = Duration.ofSeconds(3);

    private final JavaRunner runner;

    public ExecutionService(JavaRunner runner) {
        this.runner = runner;
    }

    public record TestSpec(String input, String expected) {}

    public record TestOutcome(int index, String input, String expected, String actual,
                              boolean passed, String error, long timeMs, String verdict) {}

    public record RunOutcome(boolean compiled, String compileOutput, List<TestOutcome> results) {}

    public record SubmitOutcome(boolean compiled, String compileOutput, String verdict,
                                int passedCount, int totalCount, TestOutcome failedTest, long timeMs) {}

    /** Method mode: run the user's Solution against client-supplied tests (never hidden tests). */
    public RunOutcome runMethod(Question question, String code, List<TestSpec> tests) {
        validateCode(code);
        validateTests(tests);
        Map<String, String> sources = new LinkedHashMap<>();
        sources.put("Solution.java", code);
        sources.put("Harness.java", HarnessGenerator.harnessSource());
        sources.put("Main.java", HarnessGenerator.generateMainForQuestion(question));
        return execute(sources, tests);
    }

    /** Method mode with an ad-hoc signature (no catalog question needed). */
    public RunOutcome runMethod(Question.Signature signature, String code, List<TestSpec> tests) {
        validateCode(code);
        validateTests(tests);
        Map<String, String> sources = new LinkedHashMap<>();
        sources.put("Solution.java", code);
        sources.put("Harness.java", HarnessGenerator.harnessSource());
        sources.put("Main.java", HarnessGenerator.generateMain(signature));
        return execute(sources, tests);
    }

    /** Program mode: run a complete user program (class Main + main) against client-supplied tests. */
    public RunOutcome runProgram(String code, List<TestSpec> tests) {
        validateCode(code);
        validateTests(tests);
        if (!code.matches("(?s).*\\bclass\\s+Main\\b.*")) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Program mode needs a complete Java program with class Main and public static void main(String[] args). "
                    + "For a LeetCode-style method-only submission, use method mode with a problemId.");
        }
        return execute(Map.of("Main.java", code), tests);
    }

    /** Submit: run the user's Solution against the question's hidden tests server-side. */
    public SubmitOutcome submit(Question question, String code) {
        validateCode(code);
        List<TestSpec> hidden = question.hiddenTests().stream()
                .map(t -> new TestSpec(t.input(), t.expected()))
                .toList();
        if (hidden.isEmpty() || hidden.size() > MAX_TESTS) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR,
                    "Question '" + question.id() + "' has an invalid hidden test set.");
        }
        Map<String, String> sources = new LinkedHashMap<>();
        sources.put("Solution.java", code);
        sources.put("Harness.java", HarnessGenerator.harnessSource());
        sources.put("Main.java", HarnessGenerator.generateMainForQuestion(question));
        RunOutcome run = execute(sources, hidden);
        if (!run.compiled()) {
            return new SubmitOutcome(false, run.compileOutput(), VerdictMapper.COMPILATION_ERROR,
                    0, hidden.size(), null, 0);
        }
        int passed = 0;
        TestOutcome failed = null;
        long maxMs = 0;
        for (TestOutcome o : run.results()) {
            maxMs = Math.max(maxMs, o.timeMs());
            if (o.passed()) passed++;
            else if (failed == null) failed = o;
        }
        String verdict = failed == null ? VerdictMapper.ACCEPTED : failed.verdict();
        return new SubmitOutcome(true, run.compileOutput(), verdict, passed, hidden.size(), failed, maxMs);
    }

    private RunOutcome execute(Map<String, String> sources, List<TestSpec> tests) {
        Path dir = null;
        try {
            // Work dirs must live on a host-mounted path (DSA_WORK_DIR) so the
            // Docker daemon can bind-mount them into sibling sandbox containers.
            // The default JVM temp dir is inside this container's filesystem and
            // invisible to the host, which makes javac see an empty /workspace.
            Path workBase = Path.of(System.getenv().getOrDefault("DSA_WORK_DIR", "/opt/dsa-work"))
                    .toAbsolutePath().normalize();
            Files.createDirectories(workBase);
            dir = Files.createTempDirectory(workBase, "dsa-run-");
            Files.createDirectories(dir.resolve("tmp"));
            for (Map.Entry<String, String> e : sources.entrySet()) {
                Files.writeString(dir.resolve(e.getKey()), e.getValue(), StandardCharsets.UTF_8);
            }
            JavaRunner.CompileResult compile = runner.compile(dir, new ArrayList<>(sources.keySet()), COMPILE_TIMEOUT);
            if (compile.timedOut()) {
                return new RunOutcome(false, "Compilation timed out after 12 seconds.", List.of());
            }
            if (!compile.ok()) {
                return new RunOutcome(false, compile.output(), List.of());
            }
            List<TestOutcome> outcomes = new ArrayList<>();
            int index = 1;
            for (TestSpec t : tests) {
                JavaRunner.RunResult r = runner.run(dir, "Main", safe(t.input()), RUN_TIMEOUT);
                String actual = truncate(r.output().stripTrailing(), MAX_INPUT);
                String expected = safe(t.expected()).stripTrailing();
                String verdict = VerdictMapper.decide(r.timedOut(), r.exitCode(), r.output(), actual, expected);
                boolean passed = VerdictMapper.ACCEPTED.equals(verdict);
                outcomes.add(new TestOutcome(index++, safe(t.input()), expected, actual, passed,
                        VerdictMapper.errorFor(verdict, r.timedOut(), r.exitCode()), r.timeMs(), verdict));
            }
            return new RunOutcome(true, "Compilation successful.", outcomes);
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.SERVICE_UNAVAILABLE,
                    "Could not start the Java sandbox: " + e.getMessage()
                    + " (is Docker installed and running, or is the local runner enabled?)");
        } finally {
            deleteTree(dir);
        }
    }

    public static void validateCode(String code) {
        if (code == null || code.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Java source code is required.");
        }
        if (code.length() > MAX_CODE) {
            throw new ResponseStatusException(HttpStatus.PAYLOAD_TOO_LARGE, "Code exceeds 30,000 characters.");
        }
    }

    static void validateTests(List<TestSpec> tests) {
        if (tests == null || tests.isEmpty() || tests.size() > MAX_TESTS) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Provide between 1 and 20 test cases.");
        }
        for (TestSpec t : tests) {
            if (t == null || safe(t.input()).length() > MAX_INPUT || safe(t.expected()).length() > MAX_INPUT) {
                throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                        "Each test input/output must be at most 4,000 characters.");
            }
        }
    }

    private static String safe(String s) {
        return s == null ? "" : s;
    }

    private static String truncate(String s, int max) {
        return s.length() > max ? s.substring(0, max) + "\n[output truncated]" : s;
    }

    private static void deleteTree(Path root) {
        if (root == null) return;
        try (var walk = Files.walk(root)) {
            walk.sorted(Comparator.reverseOrder()).forEach(p -> {
                try {
                    Files.deleteIfExists(p);
                } catch (IOException ignored) {
                }
            });
        } catch (IOException ignored) {
        }
    }
}
