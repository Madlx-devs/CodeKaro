package com.example.dsa.api;

import com.example.dsa.catalog.Question;
import com.example.dsa.catalog.QuestionBank;
import com.example.dsa.domain.BookmarkRepository;
import com.example.dsa.domain.SubmissionRepository;
import com.example.dsa.security.AuthSupport;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

/**
 * Question catalog endpoints. {@code hiddenTests} are never serialized —
 * see {@link QuestionPublic}, which deliberately omits that field.
 */
@RestController
@RequestMapping("/api")
public class ProblemsController {
    private final QuestionBank bank;
    private final SubmissionRepository submissions;
    private final BookmarkRepository bookmarks;

    public ProblemsController(QuestionBank bank, SubmissionRepository submissions, BookmarkRepository bookmarks) {
        this.bank = bank;
        this.submissions = submissions;
        this.bookmarks = bookmarks;
    }

    public record ProblemSummary(String id, String title, String pattern, String difficulty,
                                 List<String> tags, boolean solved, boolean attempted, boolean bookmarked) {}

    public record ProblemListResponse(List<ProblemSummary> problems) {}

    public record QuestionPublic(String id, String title, String pattern, String difficulty,
                                 String description, List<Question.Example> examples,
                                 List<String> constraints, Question.Signature signature,
                                 String starterCode, List<Question.TestCase> sampleTests,
                                 List<String> tags, String timeComplexity, String spaceComplexity,
                                 List<String> hints) {
        static QuestionPublic from(Question q) {
            return new QuestionPublic(q.id(), q.title(), q.pattern(), q.difficulty(), q.description(),
                    q.examples(), q.constraints(), q.signature(), q.starterCode(), q.sampleTests(),
                    q.tags(), q.timeComplexity(), q.spaceComplexity(), q.hints());
        }
    }

    @GetMapping("/problems")
    public ProblemListResponse list(
            @RequestParam(required = false) String pattern,
            @RequestParam(required = false) String difficulty,
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String status,
            @RequestParam(required = false) String sort,
            HttpServletRequest req) {
        if (status != null && !Set.of("solved", "attempted", "unsolved", "bookmarked").contains(status)) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "status must be one of solved|attempted|unsolved|bookmarked");
        }

        var userId = AuthSupport.userId(req);
        Set<String> solved = Set.of(), attempted = Set.of(), bookmarked = Set.of();
        if (userId.isPresent()) {
            solved = new HashSet<>(submissions.solvedProblemIds(userId.get()));
            attempted = new HashSet<>(submissions.attemptedProblemIds(userId.get()));
            bookmarked = new HashSet<>(bookmarks.problemIdsByUser(userId.get()));
        } else if (status != null) {
            throw new ResponseStatusException(HttpStatus.UNAUTHORIZED,
                    "Sign in to filter problems by completion status.");
        }

        String searchLower = search == null ? null : search.toLowerCase(Locale.ROOT).trim();
        List<ProblemSummary> out = new ArrayList<>();
        for (Question q : bank.all()) {
            if (pattern != null && !q.pattern().equals(pattern)) continue;
            if (difficulty != null && !q.difficulty().equalsIgnoreCase(difficulty)) continue;
            if (searchLower != null && !searchLower.isEmpty()
                    && !q.title().toLowerCase(Locale.ROOT).contains(searchLower)
                    && !q.id().toLowerCase(Locale.ROOT).contains(searchLower)
                    && q.tags().stream().noneMatch(t -> t.toLowerCase(Locale.ROOT).contains(searchLower))) continue;
            boolean isSolved = solved.contains(q.id());
            boolean isAttempted = attempted.contains(q.id());
            boolean isBookmarked = bookmarked.contains(q.id());
            if ("solved".equals(status) && !isSolved) continue;
            if ("attempted".equals(status) && !isAttempted) continue;
            if ("unsolved".equals(status) && (isSolved || isAttempted)) continue;
            if ("bookmarked".equals(status) && !isBookmarked) continue;
            out.add(new ProblemSummary(q.id(), q.title(), q.pattern(), q.difficulty(), q.tags(),
                    isSolved, isAttempted, isBookmarked));
        }

        if ("difficulty".equalsIgnoreCase(sort)) {
            Map<String, Integer> order = Map.of("Easy", 0, "Medium", 1, "Hard", 2);
            out.sort(Comparator.comparingInt((ProblemSummary p) -> order.getOrDefault(p.difficulty(), 9))
                    .thenComparing(ProblemSummary::title));
        } else if ("title".equalsIgnoreCase(sort)) {
            out.sort(Comparator.comparing(ProblemSummary::title));
        }
        return new ProblemListResponse(out);
    }

    @GetMapping("/problems/{id}")
    public QuestionPublic get(@PathVariable String id) {
        return bank.findById(id)
                .map(QuestionPublic::from)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Unknown problem: " + id));
    }
}
