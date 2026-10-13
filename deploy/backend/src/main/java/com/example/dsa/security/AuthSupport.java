package com.example.dsa.security;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.util.Optional;

/** Helpers for the request-scoped user id populated by {@link AuthInterceptor}. */
public final class AuthSupport {
    public static final String USER_ID_ATTR = "userId";

    private AuthSupport() {}

    public static Optional<Long> userId(HttpServletRequest req) {
        Object v = req.getAttribute(USER_ID_ATTR);
        return v instanceof Long l ? Optional.of(l) : Optional.empty();
    }

    public static Long requireUserId(HttpServletRequest req) {
        return userId(req).orElseThrow(() -> new ResponseStatusException(HttpStatus.UNAUTHORIZED,
                "Authentication required. Send Authorization: Bearer <token>."));
    }
}
