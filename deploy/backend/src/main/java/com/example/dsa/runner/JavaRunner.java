package com.example.dsa.runner;

import java.io.IOException;
import java.nio.file.Path;
import java.time.Duration;
import java.util.List;

/** Compiles and runs untrusted Java code in an isolated sandbox. */
public interface JavaRunner {

    record CompileResult(boolean ok, String output, boolean timedOut) {}

    record RunResult(int exitCode, String output, long timeMs, boolean timedOut) {}

    CompileResult compile(Path workDir, List<String> sources, Duration timeout) throws IOException;

    RunResult run(Path workDir, String mainClass, String stdin, Duration timeout) throws IOException;
}
