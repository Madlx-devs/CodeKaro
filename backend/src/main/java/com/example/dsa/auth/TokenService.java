package com.example.dsa.auth;

import com.example.dsa.domain.AuthToken;
import com.example.dsa.domain.TokenRepository;
import org.springframework.stereotype.Service;

import java.security.SecureRandom;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.HexFormat;
import java.util.Optional;

/** Issues and validates opaque 256-bit bearer tokens stored server-side. */
@Service
public class TokenService {
    private static final long TTL_DAYS = 30;

    private final TokenRepository tokens;
    private final SecureRandom random = new SecureRandom();

    public TokenService(TokenRepository tokens) {
        this.tokens = tokens;
    }

    public String issue(Long userId) {
        byte[] bytes = new byte[32];
        random.nextBytes(bytes);
        String token = HexFormat.of().formatHex(bytes);
        AuthToken t = new AuthToken();
        t.setToken(token);
        t.setUserId(userId);
        t.setExpiresAt(Instant.now().plus(TTL_DAYS, ChronoUnit.DAYS));
        tokens.save(t);
        return token;
    }

    public Optional<Long> userIdFor(String token) {
        if (token == null || token.isBlank()) return Optional.empty();
        return tokens.findById(token.trim())
                .filter(t -> t.getExpiresAt().isAfter(Instant.now()))
                .map(AuthToken::getUserId);
    }
}
