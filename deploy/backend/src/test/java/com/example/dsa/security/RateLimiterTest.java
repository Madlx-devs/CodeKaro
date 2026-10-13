package com.example.dsa.security;

import org.junit.jupiter.api.Test;

import java.util.concurrent.atomic.AtomicLong;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RateLimiterTest {

    @Test
    void allowsThirtyThenDeniesWithRetryAfter() {
        AtomicLong now = new AtomicLong(1_000_000L);
        RateLimiter rl = new RateLimiter(now::get);
        for (int i = 0; i < 30; i++) {
            assertTrue(rl.tryAcquire("1.2.3.4").allowed(), "request " + (i + 1) + " should be allowed");
        }
        RateLimiter.Decision denied = rl.tryAcquire("1.2.3.4");
        assertFalse(denied.allowed());
        assertTrue(denied.retryAfterSeconds() >= 1, "Retry-After must be positive");
    }

    @Test
    void refillsFullyAfterWindow() {
        AtomicLong now = new AtomicLong(0);
        RateLimiter rl = new RateLimiter(now::get);
        for (int i = 0; i < 30; i++) rl.tryAcquire("ip");
        assertFalse(rl.tryAcquire("ip").allowed());
        now.addAndGet(60_000);
        assertTrue(rl.tryAcquire("ip").allowed());
    }

    @Test
    void partialRefillGrantsProportionalTokens() {
        AtomicLong now = new AtomicLong(0);
        RateLimiter rl = new RateLimiter(now::get);
        for (int i = 0; i < 30; i++) rl.tryAcquire("ip");
        now.addAndGet(2_000); // 2s of 60s window -> 1 token
        assertTrue(rl.tryAcquire("ip").allowed());
        assertFalse(rl.tryAcquire("ip").allowed());
    }

    @Test
    void bucketsAreIndependentPerKey() {
        AtomicLong now = new AtomicLong(0);
        RateLimiter rl = new RateLimiter(now::get);
        for (int i = 0; i < 30; i++) rl.tryAcquire("a");
        assertFalse(rl.tryAcquire("a").allowed());
        assertTrue(rl.tryAcquire("b").allowed());
    }

    @Test
    void allowedDecisionsCarryZeroRetryAfter() {
        RateLimiter rl = new RateLimiter(() -> 0L);
        RateLimiter.Decision d = rl.tryAcquire("x");
        assertTrue(d.allowed());
        assertTrue(d.retryAfterSeconds() == 0);
    }
}
