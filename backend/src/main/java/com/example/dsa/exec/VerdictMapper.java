package com.example.dsa.exec;

/**
 * Maps a finished (or timed-out) process to a judge verdict.
 * Pure function — unit tested, no I/O.
 */
public final class VerdictMapper {
    private VerdictMapper() {}

    public static final String ACCEPTED = "Accepted";
    public static final String WRONG_ANSWER = "Wrong Answer";
    public static final String RUNTIME_ERROR = "Runtime Error";
    public static final String TIME_LIMIT_EXCEEDED = "Time Limit Exceeded";
    public static final String MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded";
    public static final String COMPILATION_ERROR = "Compilation Error";

    /**
     * @param timedOut true when the run exceeded its wall-clock limit
     * @param exitCode process exit code (137 = killed by the container OOM killer)
     * @param output   merged stdout+stderr, may be null
     * @param actual   program output (trailing whitespace stripped) for comparison
     * @param expected expected output (trailing whitespace stripped)
     */
    public static String decide(boolean timedOut, int exitCode, String output, String actual, String expected) {
        if (timedOut) return TIME_LIMIT_EXCEEDED;
        String out = output == null ? "" : output;
        if (out.contains("OutOfMemoryError")) return MEMORY_LIMIT_EXCEEDED;
        if (exitCode == 137) return MEMORY_LIMIT_EXCEEDED;
        if (exitCode != 0) return RUNTIME_ERROR;
        return normalize(actual).equals(normalize(expected)) ? ACCEPTED : WRONG_ANSWER;
    }

    /** Comparison rule from the CONTRACT: trim trailing whitespace, normalize CRLF. */
    public static String normalize(String s) {
        return s == null ? "" : s.replace("\r\n", "\n").strip();
    }

    /** Short human-readable explanation attached to a non-Accepted test. */
    public static String errorFor(String verdict, boolean timedOut, int exitCode) {
        return switch (verdict) {
            case TIME_LIMIT_EXCEEDED -> "Time limit exceeded (3 seconds per test).";
            case MEMORY_LIMIT_EXCEEDED -> "Memory limit exceeded (128 MB container, 64 MB JVM heap).";
            case RUNTIME_ERROR -> timedOut ? "Execution timed out." : "Process exited with code " + exitCode + ".";
            default -> "";
        };
    }
}
