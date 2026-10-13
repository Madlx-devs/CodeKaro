package com.example.dsa.api;

import at.favre.lib.crypto.bcrypt.BCrypt;
import com.example.dsa.auth.TokenService;
import com.example.dsa.domain.User;
import com.example.dsa.domain.UserRepository;
import org.springframework.http.HttpStatus;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.util.regex.Pattern;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private static final Pattern USERNAME = Pattern.compile("[A-Za-z0-9_-]{3,32}");

    private final UserRepository users;
    private final TokenService tokens;

    public AuthController(UserRepository users, TokenService tokens) {
        this.users = users;
        this.tokens = tokens;
    }

    public record AuthRequest(String username, String password) {}
    public record TokenResponse(String token) {}

    @PostMapping("/register")
    @Transactional
    public TokenResponse register(@RequestBody AuthRequest req) {
        String username = cleanUsername(req);
        String password = req == null ? null : req.password();
        if (username == null || !USERNAME.matcher(username).matches()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Username must be 3-32 characters: letters, digits, '_' or '-'.");
        }
        if (password == null || password.length() < 8 || password.length() > 128) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Password must be 8-128 characters.");
        }
        if (users.findByUsername(username).isPresent()) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username is taken.");
        }
        User u = new User();
        u.setUsername(username);
        u.setPasswordHash(BCrypt.withDefaults().hashToString(12, password.toCharArray()));
        u.setCreatedAt(Instant.now());
        users.save(u);
        return new TokenResponse(tokens.issue(u.getId()));
    }

    @PostMapping("/login")
    public TokenResponse login(@RequestBody AuthRequest req) {
        String username = cleanUsername(req);
        String password = req == null ? null : req.password();
        User u = username == null ? null : users.findByUsername(username).orElse(null);
        boolean ok = u != null && password != null
                && BCrypt.verifyer().verify(password.toCharArray(), u.getPasswordHash().toCharArray()).verified;
        if (!ok) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED, "Invalid username or password.");
        }
        return new TokenResponse(tokens.issue(u.getId()));
    }

    private static String cleanUsername(AuthRequest req) {
        if (req == null || req.username() == null) return null;
        String t = req.username().trim();
        return t.isEmpty() ? null : t;
    }
}
