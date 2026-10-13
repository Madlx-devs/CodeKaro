package com.example.dsa.ai;

import com.example.dsa.catalog.Question;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * Server-side proxy to an OpenAI-compatible chat-completions endpoint.
 * The API key lives only in server env ({@code OPENAI_API_KEY}) and is never
 * sent to the client or written to logs. All prompts are built from the
 * ACTUAL problem data (description, examples, constraints, signature) plus
 * the user's code where relevant — nothing is templated per question.
 */
@Service
public class AiService {
    private static final Logger log = LoggerFactory.getLogger(AiService.class);

    private final String apiKey;
    private final String baseUrl;
    private final String model;
    private final HttpClient http;
    private final ObjectMapper mapper = new ObjectMapper();

    public AiService() {
        this.apiKey = trimToNull(System.getenv("OPENAI_API_KEY"));
        this.baseUrl = trimToDefault(System.getenv("OPENAI_BASE_URL"), "https://api.openai.com/v1");
        this.model = trimToDefault(System.getenv("OPENAI_MODEL"), "gpt-4o-mini");
        this.http = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();
    }

    /** True when an API key is configured; otherwise endpoints return 503. */
    public boolean configured() {
        return apiKey != null;
    }

    public String understand(Question q, String level) {
        return chat(
                "You are a patient DSA tutor. Explain clearly and concisely in Markdown. "
                + "Adapt vocabulary and depth to the learner's level.",
                problemBlock(q, level)
                + "Explain this problem in simple language for a " + level + " learner: what it asks, "
                + "the core idea, a small concrete walkthrough, and edge cases to watch for. "
                + "Do NOT write code or give away the solution approach in code.");
    }

    /** The 7-step analogy explanation: familiar analogy -> code mapping -> pattern -> walkthrough -> Java -> complexity -> check. */
    public String analogy(Question q, String level) {
        Question.Example first = q.examples().isEmpty() ? null : q.examples().get(0);
        return chat(
                "You are a DSA tutor who teaches through vivid everyday analogies. Use Markdown with "
                + "exactly the numbered sections requested, in order.",
                problemBlock(q, level)
                + "Write your explanation with EXACTLY these seven sections, in this order:\n"
                + "1. **The Analogy** — explain the core problem using a familiar everyday situation "
                + "(e.g. finding a book in a library, organizing queues, delivering packages, climbing stairs). Keep it vivid and concrete.\n"
                + "2. **Mapping to Code** — for each part of the analogy, state exactly what it represents "
                + "in the actual problem (the input, the variables, the key operations).\n"
                + "3. **Why This Pattern Works** — name the DSA pattern (" + q.pattern() + ") and explain why "
                + "it fits here, and why a simpler brute-force approach would be inefficient.\n"
                + "4. **Step-by-Step Walkthrough** — run the analogy over the first sample input "
                + "(" + (first == null ? "n/a" : first.input()) + " -> " + (first == null ? "n/a" : first.output()) + "), step by step.\n"
                + "5. **Connecting to Java** — relate the analogy to the actual Java pieces: the method signature "
                + "`" + signatureText(q) + "`, the loops, the variables, and the data structures involved.\n"
                + "6. **Complexity, Intuitively** — explain the time and space cost using the analogy first, "
                + "then give the Big-O (" + q.timeComplexity() + " time, " + q.spaceComplexity() + " space).\n"
                + "7. **Check Your Understanding** — ask one short question the learner can answer to verify they got it.\n"
                + "Do not dump a full code solution.");
    }

    public String hint(Question q, String code, int hintLevel) {
        String levelGuidance = switch (hintLevel) {
            case 1 -> "Give ONLY a gentle nudge: point at the pattern or observation to consider and ask one guiding question. Stay high-level.";
            case 2 -> "Describe the key insight and sketch a high-level plan of attack (no code, no pseudocode with real logic).";
            default -> "Give a detailed step-by-step strategy. You may include a pseudocode outline, but NEVER the complete Java solution.";
        };
        StringBuilder user = new StringBuilder(problemBlock(q, "intermediate"));
        user.append("This is hint ").append(hintLevel).append(" of 3 (progressive — the learner can ask for more). ");
        user.append(levelGuidance).append("\n");
        user.append("CRITICAL: never reveal the full solution and never write complete, compilable Java code for it.\n");
        if (code != null && !code.isBlank()) {
            user.append("The learner's current code (may be incomplete or buggy):\n```java\n")
                .append(truncate(code, 6000)).append("\n```\n");
            user.append("Tailor the hint to where they are stuck.\n");
        }
        return chat(
                "You are a Socratic DSA tutor. You guide with questions and partial insights; you never hand over full solutions. Use Markdown.",
                user.toString());
    }

    public String explainCode(Question q, String code, String level) {
        StringBuilder user = new StringBuilder();
        if (q != null) user.append(problemBlock(q, level));
        user.append("Review the following Java code. Explain what it does line by line where it matters, "
                + "point out any bugs or edge cases it mishandles, explain the time and space complexity with reasoning, "
                + "and suggest concrete improvements. If the code is broken, explain the fix rather than just rewriting it.\n");
        user.append("```java\n").append(truncate(code, 12000)).append("\n```");
        return chat(
                "You are an expert Java code reviewer and DSA tutor. Be precise, kind, and concrete. Use Markdown.",
                user.toString());
    }

    public String dryRun(Question q, String code, String input) {
        StringBuilder user = new StringBuilder();
        if (q != null) user.append(problemBlock(q, "intermediate"));
        user.append("Dry-run the following Java code line by line");
        if (input != null && !input.isBlank()) user.append(" using this input:\n```\n").append(truncate(input, 2000)).append("\n```\n");
        else user.append(" using the first sample input.\n");
        user.append("Show a trace table of the important variables as they change, state what gets printed, "
                + "and finish with what the code returns for this input.\n");
        user.append("```java\n").append(truncate(code, 12000)).append("\n```");
        return chat(
                "You are a precise program tracer. Simulate execution faithfully, step by step. Use Markdown with a trace table.",
                user.toString());
    }

    // ---- transport ----

    private String chat(String system, String user) {
        if (!configured()) throw new AiException("AI not configured");
        try {
            String body = mapper.writeValueAsString(Map.of(
                    "model", model,
                    "temperature", 0.7,
                    "messages", List.of(
                            Map.of("role", "system", "content", system),
                            Map.of("role", "user", "content", user))));
            HttpRequest req = HttpRequest.newBuilder(URI.create(baseUrl + "/chat/completions"))
                    .timeout(Duration.ofSeconds(60))
                    .header("Authorization", "Bearer " + apiKey)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build();
            HttpResponse<String> resp = http.send(req, HttpResponse.BodyHandlers.ofString());
            if (resp.statusCode() / 100 != 2) {
                log.warn("AI provider returned HTTP {}", resp.statusCode());
                throw new AiException("AI provider returned HTTP " + resp.statusCode());
            }
            JsonNode root = mapper.readTree(resp.body());
            JsonNode content = root.path("choices").path(0).path("message").path("content");
            if (content.isMissingNode() || content.asText().isBlank()) {
                throw new AiException("AI provider returned an empty response");
            }
            return content.asText().trim();
        } catch (AiException e) {
            throw e;
        } catch (Exception e) {
            log.warn("AI request failed: {}", e.toString());
            throw new AiException("AI request failed: " + e.getMessage(), e);
        }
    }

    // ---- prompt builders ----

    private static String problemBlock(Question q, String level) {
        StringBuilder sb = new StringBuilder();
        sb.append("Problem: ").append(q.title())
          .append(" [").append(q.difficulty()).append("]")
          .append(" (pattern: ").append(q.pattern()).append(")\n\n");
        sb.append("Description:\n").append(q.description()).append("\n\n");
        if (!q.examples().isEmpty()) {
            sb.append("Examples:\n");
            for (Question.Example e : q.examples()) {
                sb.append("- Input: ").append(e.input()).append(" | Output: ").append(e.output());
                if (e.explanation() != null && !e.explanation().isBlank())
                    sb.append(" | Explanation: ").append(e.explanation());
                sb.append("\n");
            }
            sb.append("\n");
        }
        if (!q.constraints().isEmpty()) {
            sb.append("Constraints:\n");
            for (String c : q.constraints()) sb.append("- ").append(c).append("\n");
            sb.append("\n");
        }
        sb.append("Method signature: `").append(signatureText(q)).append("`\n");
        if (level != null && !level.isBlank()) sb.append("Learner level: ").append(level).append("\n");
        sb.append("\n");
        return sb.toString();
    }

    private static String signatureText(Question q) {
        Question.Signature s = q.signature();
        String params = s.params().stream()
                .map(p -> p.type() + " " + p.name())
                .collect(Collectors.joining(", "));
        return "public " + s.returnType() + " " + s.methodName() + "(" + params + ")";
    }

    private static String truncate(String s, int max) {
        return s.length() > max ? s.substring(0, max) + "\n[... truncated]" : s;
    }

    private static String trimToNull(String s) {
        return s == null || s.isBlank() ? null : s.trim();
    }

    private static String trimToDefault(String s, String def) {
        return s == null || s.isBlank() ? def : s.trim();
    }
}
