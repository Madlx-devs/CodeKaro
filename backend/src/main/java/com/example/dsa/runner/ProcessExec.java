package com.example.dsa.runner;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.List;
import java.util.concurrent.TimeUnit;

/** Shared process-execution helper: feeds stdin, captures merged stdout+stderr, enforces a timeout. */
final class ProcessExec {
    private ProcessExec() {}

    record ExecResult(int exitCode, String output, boolean timedOut) {}

    static ExecResult exec(List<String> cmd, String stdin, Duration timeout) throws IOException {
        Process p = new ProcessBuilder(cmd).redirectErrorStream(true).start();
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
        boolean finished;
        try {
            finished = p.waitFor(timeout.toMillis(), TimeUnit.MILLISECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            p.destroyForcibly();
            return new ExecResult(-1, "Interrupted.", false);
        }
        if (!finished) {
            p.destroyForcibly();
            return new ExecResult(-1, output.toString(StandardCharsets.UTF_8), true);
        }
        try {
            reader.join(500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        String text = output.toString(StandardCharsets.UTF_8);
        if (text.length() > 12000) text = text.substring(0, 12000) + "\n[output truncated]";
        return new ExecResult(p.exitValue(), text, false);
    }
}
