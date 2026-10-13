package com.example.dsa.api;

import com.example.dsa.catalog.Question;
import com.example.dsa.catalog.QuestionBank;
import com.example.dsa.domain.Submission;
import com.example.dsa.domain.SubmissionRepository;
import com.example.dsa.exec.ExecutionService;
import com.example.dsa.harness.HarnessGenerator;
import com.example.dsa.security.AuthSupport;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.List;

/**
 * Code execution endpoints. {@code /api/run} only ever runs client-supplied tests;
 * {@code /api/submit} runs the question's hidden tests server-side (never exposed).
 * Rate-limited to 30 req/min/IP by {@code RateLimitFilter}.
 */
@RestController
@RequestMapping("/api")
public class ExecutionController {
    private final ExecutionService exec;
    private final QuestionBank bank;
    private final SubmissionRepository submissions;

    public ExecutionController(ExecutionService exec, QuestionBank bank, SubmissionRepository submissions) {
        this.exec = exec;
        this.bank = bank;
        this.submissions = submissions;
    }

    public record TestCaseDTO(String input, String expected) {}
    public record ParamDTO(String name, String type) {}
    public record SignatureDTO(String className, String methodName, String returnType, List<ParamDTO> params) {}
    public record RunRequest(String problemId, String mode, String code, List<TestCaseDTO> tests,
                             SignatureDTO signature) {}
    public record TestResultDTO(int index, String input, String expected, String actual, boolean passed,
                                String error, long timeMs, String verdict) {}
    public record RunResponse(boolean compiled, String compileOutput, List<TestResultDTO> results, String note) {}
    public record SubmitRequest(String problemId, String code) {}
    public record SubmitResponse(boolean compiled, String compileOutput, String verdict, int passedCount,
                                 int totalCount, TestResultDTO failedTest, long timeMs) {}

    @PostMapping("/run")
    public RunResponse run(@RequestBody RunRequest request, HttpServletRequest http) {
        if (request == null) throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Request body is required.");
        String mode = request.mode() == null || request.mode().isBlank()
                ? (request.problemId() != null ? "method" : "program")
                : request.mode().trim().toLowerCase();
        List<ExecutionService.TestSpec> tests = toSpecs(request.tests());

        ExecutionService.RunOutcome outcome;
        if ("method".equals(mode)) {
            Question.Signature sig = resolveSignature(request);
            outcome = exec.runMethod(sig, request.code(), tests);
        } else if ("program".equals(mode)) {
            outcome = exec.runProgram(request.code(), tests);
        } else {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "mode must be \"method\" or \"program\".");
        }
        List<TestResultDTO> results = outcome.results().stream().map(ExecutionController::toDTO).toList();
        return new RunResponse(outcome.compiled(), outcome.compileOutput(), results,
                "Executed in an isolated sandbox (Docker: network disabled, 128 MB / 0.5 CPU / 64 pids, "
                + "read-only filesystem). Output comparison trims trailing whitespace and normalizes line endings. "
                + "Per-test limits: 3 s wall clock, 64 MB heap.");
    }

    @PostMapping("/submit")
    @Transactional
    public SubmitResponse submit(@RequestBody SubmitRequest request, HttpServletRequest http) {
        if (request == null || request.problemId() == null || request.problemId().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "problemId is required.");
        }
        Question q = bank.findById(request.problemId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
                        "Unknown problem: " + request.problemId()));
        ExecutionService.SubmitOutcome outcome = exec.submit(q, request.code());

        AuthSupport.userId(http).ifPresent(uid -> {
            Submission s = new Submission();
            s.setUserId(uid);
            s.setProblemId(q.id());
            s.setCode(request.code());
            s.setVerdict(outcome.verdict());
            s.setPassed(outcome.passedCount());
            s.setTotal(outcome.totalCount());
            s.setCreatedAt(Instant.now());
            submissions.save(s);
        });

        TestResultDTO failed = outcome.failedTest() == null ? null : toDTO(outcome.failedTest());
        return new SubmitResponse(outcome.compiled(), outcome.compileOutput(), outcome.verdict(),
                outcome.passedCount(), outcome.totalCount(), failed, outcome.timeMs());
    }

    private Question.Signature resolveSignature(RunRequest request) {
        if (request.problemId() != null && !request.problemId().isBlank()) {
            return bank.findById(request.problemId())
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND,
                            "Unknown problem: " + request.problemId()))
                    .signature();
        }
        SignatureDTO s = request.signature();
        if (s == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Method mode needs either problemId or an explicit signature.");
        }
        try {
            List<Question.Param> params = s.params() == null ? List.of()
                    : s.params().stream().map(p -> new Question.Param(p.name(), p.type())).toList();
            Question.Signature sig = new Question.Signature(s.className(), s.methodName(), s.returnType(), params);
            HarnessGenerator.validateSignature(sig);
            return sig;
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, e.getMessage());
        }
    }

    private static List<ExecutionService.TestSpec> toSpecs(List<TestCaseDTO> tests) {
        if (tests == null) return List.of(new ExecutionService.TestSpec("", ""));
        return tests.stream()
                .map(t -> new ExecutionService.TestSpec(t == null ? null : t.input(), t == null ? null : t.expected()))
                .toList();
    }

    private static TestResultDTO toDTO(ExecutionService.TestOutcome o) {
        return new TestResultDTO(o.index(), o.input(), o.expected(), o.actual(), o.passed(),
                o.error(), o.timeMs(), o.verdict());
    }
}
