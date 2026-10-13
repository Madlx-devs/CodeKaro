package com.example.dsa.exec;

import org.junit.jupiter.api.Test;

import static com.example.dsa.exec.VerdictMapper.ACCEPTED;
import static com.example.dsa.exec.VerdictMapper.MEMORY_LIMIT_EXCEEDED;
import static com.example.dsa.exec.VerdictMapper.RUNTIME_ERROR;
import static com.example.dsa.exec.VerdictMapper.TIME_LIMIT_EXCEEDED;
import static com.example.dsa.exec.VerdictMapper.WRONG_ANSWER;
import static org.junit.jupiter.api.Assertions.assertEquals;

class VerdictMapperTest {

    @Test
    void acceptedOnExactMatch() {
        assertEquals(ACCEPTED, VerdictMapper.decide(false, 0, "", "[0, 1]", "[0, 1]"));
    }

    @Test
    void acceptedIgnoresTrailingWhitespaceAndCrlf() {
        assertEquals(ACCEPTED, VerdictMapper.decide(false, 0, "", "[0, 1]\r\n  ", "[0, 1]"));
    }

    @Test
    void wrongAnswerOnMismatch() {
        assertEquals(WRONG_ANSWER, VerdictMapper.decide(false, 0, "", "[0, 2]", "[0, 1]"));
    }

    @Test
    void wrongAnswerOnEmptyOutput() {
        assertEquals(WRONG_ANSWER, VerdictMapper.decide(false, 0, "", "", "[0, 1]"));
    }

    @Test
    void timeLimitExceededOnTimeout() {
        assertEquals(TIME_LIMIT_EXCEEDED, VerdictMapper.decide(true, -1, "partial", "", ""));
    }

    @Test
    void timeoutBeatsOtherSignals() {
        assertEquals(TIME_LIMIT_EXCEEDED,
                VerdictMapper.decide(true, 1, "java.lang.OutOfMemoryError: Java heap space", "", ""));
    }

    @Test
    void runtimeErrorOnNonZeroExit() {
        assertEquals(RUNTIME_ERROR,
                VerdictMapper.decide(false, 1, "Exception in thread \"main\" java.lang.NullPointerException", "", ""));
    }

    @Test
    void memoryLimitOnOutOfMemoryErrorText() {
        assertEquals(MEMORY_LIMIT_EXCEEDED,
                VerdictMapper.decide(false, 1, "Exception in thread \"main\" java.lang.OutOfMemoryError: Java heap space", "", ""));
    }

    @Test
    void memoryLimitOnExit137() {
        assertEquals(MEMORY_LIMIT_EXCEEDED, VerdictMapper.decide(false, 137, "", "", ""));
    }

    @Test
    void normalizeHandlesNullAndCrlf() {
        assertEquals("", VerdictMapper.normalize(null));
        assertEquals("[1, 2]", VerdictMapper.normalize("[1, 2]\r\n"));
    }

    @Test
    void errorMessagesAreHumanReadable() {
        assertTrueContains(VerdictMapper.errorFor(TIME_LIMIT_EXCEEDED, true, -1), "3 seconds");
        assertTrueContains(VerdictMapper.errorFor(MEMORY_LIMIT_EXCEEDED, false, 137), "Memory");
        assertTrueContains(VerdictMapper.errorFor(RUNTIME_ERROR, false, 1), "code 1");
        assertEquals("", VerdictMapper.errorFor(ACCEPTED, false, 0));
    }

    private static void assertTrueContains(String actual, String fragment) {
        if (actual == null || !actual.contains(fragment)) {
            throw new AssertionError("Expected <" + actual + "> to contain <" + fragment + ">");
        }
    }
}
