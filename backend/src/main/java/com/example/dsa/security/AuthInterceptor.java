package com.example.dsa.security;

import com.example.dsa.auth.TokenService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

/**
 * Reads {@code Authorization: Bearer <token>} on every /api request and, when the
 * token is valid, stores the user id as a request attribute. It never rejects:
 * endpoints that need auth call {@link AuthSupport#requireUserId}, endpoints with
 * optional auth degrade gracefully for anonymous callers.
 */
@Component
public class AuthInterceptor implements HandlerInterceptor {
    private final TokenService tokens;

    public AuthInterceptor(TokenService tokens) {
        this.tokens = tokens;
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        String auth = request.getHeader("Authorization");
        if (auth != null && auth.regionMatches(true, 0, "Bearer ", 0, 7)) {
            tokens.userIdFor(auth.substring(7)).ifPresent(id -> request.setAttribute(AuthSupport.USER_ID_ATTR, id));
        }
        return true;
    }
}
