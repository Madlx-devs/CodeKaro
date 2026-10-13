package com.example.dsa.runner;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

/**
 * DEV-ONLY runner that compiles and runs code directly on the application host.
 * It is constructed only when BOTH JAVA_RUNNER_MODE=local and ALLOW_LOCAL_EXECUTION=true
 * are set (see RunnerConfig); any other combination refuses to start. Never the default.
 */
public class LocalJavaRunner implements JavaRunner {

    @Override
    public CompileResult compile(Path workDir, List<String> sources, Duration timeout) throws IOException {
        List<String> cmd = new ArrayList<>(List.of("javac", "-encoding", "UTF-8"));
        cmd.addAll(sources);
        Process p = new ProcessBuilder(cmd).directory(workDir.toFile()).redirectErrorStream(true).start();
        ProcResult r = runProc(p, "", timeout);
        return new CompileResult(!r.timedOut && r.exitCode == 0, r.output, r.timedOut);
    }

    @Override
    public RunResult run(Path workDir, String mainClass, String stdin, Duration timeout) throws IOException {
        List<String> cmd = List.of("java", "-Xms16m", "-Xmx64m", "-XX:MaxMetaspaceSize=64m", mainClass);
        Process p = new ProcessBuilder(cmd).directory(workDir.toFile()).redirectErrorStream(true).start();
        ProcResult r = runProc(p, stdin, timeout);
        return new RunResult(r.exitCode, r.output, r.timeMs, r.timedOut);
    }

    private record ProcResult(int exitCode, String output, long timeMs, boolean timedOut) {}

    private ProcResult runProc(Process p, String stdin, Duration timeout) throws IOException {
        try (OutputStream os = p.getOutputStream()) {
            os.write(stdin.getBytes(StandardCharsets.UTF_8));
        }
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        Thread reader = new Thread(() -> {
            try (InputStream in = p.getInputStream()) {
                in.transferTo(output);
            } catch (IOException ignored) {
            }
        });
        reader.setDaemon(true);
        reader.start();
        long start = System.nanoTime();
        boolean finished;
        try {
            finished = p.waitFor(timeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            p.destroyForcibly();
            throw new IOException("Interrupted while running local java process", e);
        }
        long timeMs = (System.nanoTime() - start) / 1_000_000;
        if (!finished) {
            p.destroyForcibly();
            return new ProcResult(-1, textOf(output), timeMs, true);
        }
        try {
            reader.join(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        return new ProcResult(p.exitValue(), textOf(output), timeMs, false);
    }

    private static String textOf(ByteArrayOutputStream output) {
        String t = output.toString(StandardCharsets.UTF_8);
        return t.length() > 12000 ? t.substring(0, 12000) + "\n[output truncated]" : t;
    }
}
