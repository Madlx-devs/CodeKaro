package com.example.dsa.api;

import com.example.dsa.ai.AiException;
import com.example.dsa.ai.AiService;
import com.example.dsa.catalog.Question;
import com.example.dsa.catalog.QuestionBank;
import com.example.dsa.exec.ExecutionService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.Set;

/**
 * AI learning assistant. Every endpoint builds its prompt from the ACTUAL problem
 * data plus the user's code where relevant, and calls the configured OpenAI-compatible
 * endpoint server-side. Returns 503 when no API key is configured; the key is never
 * exposed to the client.
 */
@RestController
@RequestMapping("/api/ai")
public class AiController {
    private final AiService ai;
    private final QuestionBank bank;

    public AiController(AiService ai, QuestionBank bank) {
        this.ai = ai;
        this.bank = bank;
    }

    public record AiRequest(String problemId, String code, Integer hintLevel, String level, String input) {}
    public record AiResponse(String content) {}
    public record AiError(String error) {}

    private static final Set<String> LEVELS = Set.of("beginner", "intermediate", "advanced");

    @PostMapping("/understand")
    public ResponseEntity<?> understand(@RequestBody AiRequest req) {
        Question q = needProblem(req);
        String level = needLevel(req);
        return call(() -> ai.understand(q, level));
    }

    @PostMapping("/analogy")
    public ResponseEntity<?> analogy(@RequestBody AiRequest req) {
        Question q = needProblem(req);
        String level = needLevel(req);
        return call(() -> ai.analogy(q, level));
    }

    @PostMapping("/hint")
    public ResponseEntity<?> hint(@RequestBody AiRequest req) {
        Question q = needProblem(req);
        int hintLevel = req != null && req.hintLevel() != null ? req.hintLevel() : 1;
        if (hintLevel < 1 || hintLevel > 3) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "hintLevel must be 1, 2, or 3.");
        }
        String code = req == null ? null : req.code();
        return call(() -> ai.hint(q, code, hintLevel));
    }

    @PostMapping("/explain-code")
    public ResponseEntity<?> explainCode(@RequestBody AiRequest req) {
        String code = needCode(req);
        String level = levelOrDefault(req);
        Question q = optionalProblem(req);
        return call(() -> ai.explainCode(q, code, level));
    }

    @PostMapping("/dry-run")
    public ResponseEntity<?> dryRun(@RequestBody AiRequest req) {
        String code = needCode(req);
        Question q = optionalProblem(req);
        String input = req == null ? null : req.input();
        return call(() -> ai.dryRun(q, code, input));
    }

    // ---- helpers ----

    private interface AiCall {
        String run();
    }

    private ResponseEntity<?> call(AiCall c) {
        if (!ai.configured()) {
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE)
                    .body(new AiError("AI not configured"));
        }
        try {
            return ResponseEntity.ok(new AiResponse(c.run()));
        } catch (AiException e) {
            return ResponseEntity.status(HttpStatus.BAD_GATEWAY).body(new AiError("AI request failed"));
        }
    }

    private Question needProblem(AiRequest req) {
        String id = req == null ? null : req.problemId();
        if (id == null || id.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "problemId is required.");
        }
        return bank.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Unknown problem: " + id));
    }

    private Question optionalProblem(AiRequest req) {
        String id = req == null ? null : req.problemId();
        if (id == null || id.isBlank()) return null;
        return bank.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Unknown problem: " + id));
    }

    private String needLevel(AiRequest req) {
        String level = levelOrDefault(req);
        if (!LEVELS.contains(level)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "level must be one of beginner|intermediate|advanced.");
        }
        return level;
    }

    private String levelOrDefault(AiRequest req) {
        String level = req == null || req.level() == null ? "intermediate" : req.level().trim().toLowerCase();
        return level.isEmpty() ? "intermediate" : level;
    }

    private String needCode(AiRequest req) {
        String code = req == null ? null : req.code();
        if (code == null || code.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "code is required.");
        }
        if (code.length() > ExecutionService.MAX_CODE) {
            throw new ResponseStatusException(HttpStatus.PAYLOAD_TOO_LARGE, "Code exceeds 30,000 characters.");
        }
        return code;
    }
}
