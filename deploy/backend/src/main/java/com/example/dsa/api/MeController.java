package com.example.dsa.api;

import com.example.dsa.catalog.QuestionBank;
import com.example.dsa.domain.Bookmark;
import com.example.dsa.domain.BookmarkId;
import com.example.dsa.domain.BookmarkRepository;
import com.example.dsa.domain.Note;
import com.example.dsa.domain.NoteRepository;
import com.example.dsa.domain.Submission;
import com.example.dsa.domain.SubmissionRepository;
import com.example.dsa.security.AuthSupport;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneOffset;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

/** Authenticated user endpoints: progress dashboard, bookmarks, notes, submission history. */
@RestController
@RequestMapping("/api")
public class MeController {
    private final QuestionBank bank;
    private final SubmissionRepository submissions;
    private final BookmarkRepository bookmarks;
    private final NoteRepository notes;

    public MeController(QuestionBank bank, SubmissionRepository submissions,
                        BookmarkRepository bookmarks, NoteRepository notes) {
        this.bank = bank;
        this.submissions = submissions;
        this.bookmarks = bookmarks;
        this.notes = notes;
    }

    public record PatternProgress(int solved, int total) {}
    public record RecentSubmission(Long id, String problemId, String verdict, int passed, int total,
                                   Instant createdAt) {}
    public record ProgressResponse(int solved, int attempted, long streakDays,
                                   Map<String, PatternProgress> byPattern,
                                   Map<String, PatternProgress> byDifficulty,
                                   List<RecentSubmission> recentSubmissions) {}
    public record SubmissionDTO(Long id, String problemId, String code, String verdict, int passed,
                                int total, Instant createdAt) {}
    public record SubmissionListResponse(List<SubmissionDTO> submissions) {}
    public record BookmarkRequest(Boolean bookmarked) {}
    public record BookmarkResponse(String problemId, boolean bookmarked) {}
    public record NoteRequest(String note) {}
    public record NoteResponse(String problemId, String note, Instant updatedAt) {}

    @GetMapping("/me/progress")
    public ProgressResponse progress(HttpServletRequest req) {
        Long uid = AuthSupport.requireUserId(req);
        Set<String> solvedIds = new HashSet<>(submissions.solvedProblemIds(uid));
        Set<String> attemptedIds = new HashSet<>(submissions.attemptedProblemIds(uid));

        // streakDays: distinct UTC days with at least one Accepted submission.
        long streakDays = submissions.acceptedTimestamps(uid).stream()
                .map(t -> LocalDate.ofInstant(t, ZoneOffset.UTC))
                .distinct()
                .count();

        Map<String, PatternProgress> byPattern = new LinkedHashMap<>();
        for (String pattern : bank.patterns()) {
            long total = bank.countByPattern(pattern);
            long solved = solvedIds.stream()
                    .filter(id -> bank.findById(id).map(q -> q.pattern().equals(pattern)).orElse(false))
                    .count();
            byPattern.put(pattern, new PatternProgress((int) solved, (int) total));
        }

        Map<String, PatternProgress> byDifficulty = new LinkedHashMap<>();
        for (String difficulty : List.of("Easy", "Medium", "Hard")) {
            long total = bank.countByDifficulty(difficulty);
            long solved = solvedIds.stream()
                    .filter(id -> bank.findById(id).map(q -> q.difficulty().equals(difficulty)).orElse(false))
                    .count();
            byDifficulty.put(difficulty, new PatternProgress((int) solved, (int) total));
        }

        List<RecentSubmission> recent = submissions.findByUserIdOrderByCreatedAtDesc(uid).stream()
                .limit(10)
                .map(s -> new RecentSubmission(s.getId(), s.getProblemId(), s.getVerdict(),
                        s.getPassed(), s.getTotal(), s.getCreatedAt()))
                .toList();

        return new ProgressResponse(solvedIds.size(), attemptedIds.size(), streakDays,
                byPattern, byDifficulty, recent);
    }

    @GetMapping("/submissions")
    public SubmissionListResponse submissionHistory(
            @RequestParam(required = false) String problemId, HttpServletRequest req) {
        Long uid = AuthSupport.requireUserId(req);
        List<Submission> list = problemId == null || problemId.isBlank()
                ? submissions.findByUserIdOrderByCreatedAtDesc(uid)
                : submissions.findByUserIdAndProblemIdOrderByCreatedAtDesc(uid, problemId);
        List<SubmissionDTO> dtos = list.stream().limit(100)
                .map(s -> new SubmissionDTO(s.getId(), s.getProblemId(), s.getCode(), s.getVerdict(),
                        s.getPassed(), s.getTotal(), s.getCreatedAt()))
                .toList();
        return new SubmissionListResponse(dtos);
    }

    @PostMapping("/problems/{id}/bookmark")
    public BookmarkResponse bookmark(@PathVariable String id,
                                     @RequestBody BookmarkRequest req,
                                     HttpServletRequest http) {
        Long uid = AuthSupport.requireUserId(http);
        requireProblem(id);
        boolean want = req != null && Boolean.TRUE.equals(req.bookmarked());
        BookmarkId key = new BookmarkId(uid, id);
        if (want) {
            if (!bookmarks.existsById(key)) {
                Bookmark b = new Bookmark();
                b.setUserId(uid);
                b.setProblemId(id);
                b.setCreatedAt(Instant.now());
                bookmarks.save(b);
            }
        } else if (bookmarks.existsById(key)) {
            bookmarks.deleteById(key);
        }
        return new BookmarkResponse(id, want);
    }

    @PostMapping("/problems/{id}/note")
    public NoteResponse note(@PathVariable String id,
                             @RequestBody NoteRequest req,
                             HttpServletRequest http) {
        Long uid = AuthSupport.requireUserId(http);
        requireProblem(id);
        String text = req == null ? null : req.note();
        if (text == null || text.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Note text is required.");
        }
        if (text.length() > 10000) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Note must be at most 10,000 characters.");
        }
        Note n = notes.findByUserIdAndProblemId(uid, id).orElseGet(Note::new);
        n.setUserId(uid);
        n.setProblemId(id);
        n.setNote(text);
        n.setUpdatedAt(Instant.now());
        notes.save(n);
        return new NoteResponse(id, text, n.getUpdatedAt());
    }

    private void requireProblem(String id) {
        if (bank.findById(id).isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Unknown problem: " + id);
        }
    }
}
