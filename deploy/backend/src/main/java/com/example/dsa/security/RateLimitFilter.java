package com.example.dsa.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.nio.charset.StandardCharsets;

/** Enforces the 30 req/min/IP budget on the expensive endpoints; 429 + Retry-After beyond it. */
@Component
public class RateLimitFilter extends OncePerRequestFilter {
    private final RateLimiter limiter;

    public RateLimitFilter(RateLimiter limiter) {
        this.limiter = limiter;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String path = request.getRequestURI();
        if ("/api/run".equals(path) || "/api/submit".equals(path)) {
            RateLimiter.Decision d = limiter.tryAcquire(clientIp(request));
            if (!d.allowed()) {
                response.setStatus(429);
                response.setHeader("Retry-After", String.valueOf(d.retryAfterSeconds()));
                response.setContentType(MediaType.APPLICATION_JSON_VALUE);
                String body = "{\"error\":\"Rate limit exceeded: 30 run/submit requests per minute per IP. Retry in "
                        + d.retryAfterSeconds() + "s.\",\"retryAfterSeconds\":" + d.retryAfterSeconds() + "}";
                response.getOutputStream().write(body.getBytes(StandardCharsets.UTF_8));
                return;
            }
        }
        chain.doFilter(request, response);
    }

    private static String clientIp(HttpServletRequest request) {
        String forwarded = request.getHeader("X-Forwarded-For");
        if (forwarded != null && !forwarded.isBlank()) {
            String first = forwarded.split(",")[0].trim();
            if (!first.isEmpty()) return first.length() > 64 ? first.substring(0, 64) : first;
        }
        String remote = request.getRemoteAddr();
        return remote == null ? "unknown" : remote;
    }
}
