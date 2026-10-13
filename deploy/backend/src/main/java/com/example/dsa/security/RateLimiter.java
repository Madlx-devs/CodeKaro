package com.example.dsa.security;

import org.springframework.stereotype.Component;

import java.util.concurrent.ConcurrentHashMap;
import java.util.function.LongSupplier;

/**
 * In-memory token-bucket rate limiter: 30 requests per IP per 60-second window.
 * Thread-safe; buckets are per key (client IP). A {@link LongSupplier} clock is
 * injected for deterministic unit tests.
 */
@Component
public class RateLimiter {
    static final int CAPACITY = 30;
    static final long WINDOW_MS = 60_000;

    private final LongSupplier clock;
    private final ConcurrentHashMap<String, Bucket> buckets = new ConcurrentHashMap<>();

    public RateLimiter() {
        this(System::currentTimeMillis);
    }

    RateLimiter(LongSupplier clock) {
        this.clock = clock;
    }

    public record Decision(boolean allowed, long retryAfterSeconds) {}

    public Decision tryAcquire(String key) {
        String k = key == null ? "unknown" : key;
        Bucket b = buckets.computeIfAbsent(k, ignored -> new Bucket(clock.getAsLong()));
        synchronized (b) {
            long now = clock.getAsLong();
            long elapsed = now - b.lastRefill;
            if (elapsed > 0) {
                b.tokens = Math.min(CAPACITY, b.tokens + elapsed * (double) CAPACITY / WINDOW_MS);
                b.lastRefill = now;
            }
            if (b.tokens >= 1.0) {
                b.tokens -= 1.0;
                return new Decision(true, 0);
            }
            double needed = 1.0 - b.tokens;
            long waitMs = (long) Math.ceil(needed * WINDOW_MS / CAPACITY);
            long retryAfter = Math.max(1, (waitMs + 999) / 1000);
            return new Decision(false, retryAfter);
        }
    }

    private static final class Bucket {
        double tokens = CAPACITY;
        long lastRefill;

        Bucket(long now) {
            this.lastRefill = now;
        }
    }
}
