package com.example.dsa.catalog;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.regex.Pattern;

/**
 * Loads the question bank from classpath:/questions/*.json at startup.
 * Fails fast with a clear message naming the offending file when any question
 * violates the schema — a bad bank must never boot silently.
 */
@Component
public class QuestionBank {
    private static final Logger log = LoggerFactory.getLogger(QuestionBank.class);

    static final Set<String> TYPES = Set.of(
            "int", "long", "double", "boolean", "char", "String",
            "int[]", "long[]", "double[]", "boolean[]", "char[]", "String[]",
            "int[][]", "char[][]",
            "ListNode", "TreeNode",
            "List<Integer>", "List<String>", "List<List<Integer>>",
            "void");
    static final Set<String> DIFFICULTIES = Set.of("Easy", "Medium", "Hard");
    private static final Pattern KEBAB_ID = Pattern.compile("[a-z0-9]+(-[a-z0-9]+)*");
    private static final Pattern JAVA_IDENT = Pattern.compile("[A-Za-z_$][A-Za-z0-9_$]*");

    private final List<Question> questions = new ArrayList<>();
    private final Map<String, Question> byId = new LinkedHashMap<>();

    public QuestionBank() {
        try {
            Resource[] resources =
                    new PathMatchingResourcePatternResolver().getResources("classpath:/questions/*.json");
            ObjectMapper mapper = new ObjectMapper();
            List<Question> loaded = new ArrayList<>();
            for (Resource r : resources) {
                String name = r.getFilename() == null ? r.getDescription() : r.getFilename();
                List<Question> batch;
                try (InputStream in = r.getInputStream()) {
                    batch = mapper.readValue(in, new TypeReference<List<Question>>() {});
                } catch (Exception e) {
                    throw new IllegalStateException(
                            "Invalid question file '" + name + "': " + rootMessage(e), e);
                }
                if (batch == null || batch.isEmpty()) {
                    throw new IllegalStateException(
                            "Question file '" + name + "' is empty; expected a JSON array of questions.");
                }
                for (Question q : batch) validateQuestion(q, name);
                loaded.addAll(batch);
            }
            validateAll(loaded);
            loaded.sort(Comparator.comparing(Question::pattern).thenComparing(Question::id));
            for (Question q : loaded) {
                questions.add(q);
                byId.put(q.id(), q);
            }
            Map<String, Integer> perPattern = new LinkedHashMap<>();
            for (Question q : questions) perPattern.merge(q.pattern(), 1, Integer::sum);
            log.info("Loaded {} questions across {} patterns: {}", questions.size(), perPattern.size(), perPattern);
        } catch (IllegalStateException e) {
            throw e;
        } catch (Exception e) {
            throw new IllegalStateException("Failed to load the question bank: " + rootMessage(e), e);
        }
    }

    public List<Question> all() {
        return List.copyOf(questions);
    }

    public Optional<Question> findById(String id) {
        return Optional.ofNullable(byId.get(id));
    }

    /** Distinct patterns in catalog order. */
    public List<String> patterns() {
        LinkedHashSet<String> set = new LinkedHashSet<>();
        for (Question q : questions) set.add(q.pattern());
        return List.copyOf(set);
    }

    public int total() {
        return questions.size();
    }

    public long countByPattern(String pattern) {
        return questions.stream().filter(q -> q.pattern().equals(pattern)).count();
    }

    public long countByDifficulty(String difficulty) {
        return questions.stream().filter(q -> q.difficulty().equals(difficulty)).count();
    }

    /** Validates the whole bank: schema per question plus global id uniqueness. */
    static void validateAll(List<Question> loaded) {
        Set<String> seen = new java.util.HashSet<>();
        for (Question q : loaded) {
            if (q == null || q.id() == null || !seen.add(q.id())) {
                throw new IllegalStateException(
                        "Duplicate or missing question id: '" + (q == null ? "null" : q.id()) + "'. Ids must be unique kebab-case.");
            }
        }
    }

    /** Validates one question against the CONTRACT schema; throws IllegalStateException naming the problem. */
    static void validateQuestion(Question q, String source) {
        if (q == null) fail(source, "<null>", "question object is null");
        if (q.id() == null || !KEBAB_ID.matcher(q.id()).matches())
            fail(source, String.valueOf(q.id()), "id must be kebab-case (e.g. 'two-sum')");
        if (blank(q.title())) fail(source, q.id(), "title is required");
        if (blank(q.pattern())) fail(source, q.id(), "pattern is required");
        if (!DIFFICULTIES.contains(q.difficulty()))
            fail(source, q.id(), "difficulty must be one of " + DIFFICULTIES + ", got '" + q.difficulty() + "'");
        if (blank(q.description())) fail(source, q.id(), "description is required");
        if (blank(q.starterCode())) fail(source, q.id(), "starterCode is required");
        if (blank(q.timeComplexity())) fail(source, q.id(), "timeComplexity is required");
        if (blank(q.spaceComplexity())) fail(source, q.id(), "spaceComplexity is required");
        if (q.tags() == null || q.tags().isEmpty()) fail(source, q.id(), "tags must be non-empty");
        if (q.examples() == null || q.examples().isEmpty()) fail(source, q.id(), "examples must be non-empty");
        if (q.constraints() == null) fail(source, q.id(), "constraints must be present (may be empty)");
        if (q.hints() == null) fail(source, q.id(), "hints must be present (may be empty)");

        Question.Signature sig = q.signature();
        if (sig == null) fail(source, q.id(), "signature is required");
        if (sig.className() == null || !JAVA_IDENT.matcher(sig.className()).matches())
            fail(source, q.id(), "signature.className must be a valid Java identifier");
        if (sig.methodName() == null || !JAVA_IDENT.matcher(sig.methodName()).matches())
            fail(source, q.id(), "signature.methodName must be a valid Java identifier");
        if (!TYPES.contains(sig.returnType()))
            fail(source, q.id(), "unsupported return type '" + sig.returnType() + "'; allowed: " + TYPES);
        if (sig.params() == null) fail(source, q.id(), "signature.params must be present (may be empty)");
        for (Question.Param p : sig.params()) {
            if (p.name() == null || !JAVA_IDENT.matcher(p.name()).matches())
                fail(source, q.id(), "param name '" + p.name() + "' is not a valid Java identifier");
            if (!TYPES.contains(p.type()) || "void".equals(p.type()))
                fail(source, q.id(), "unsupported param type '" + p.type() + "'; allowed: " + TYPES + " (void not allowed as a param)");
        }

        if (q.sampleTests() == null || q.sampleTests().isEmpty())
            fail(source, q.id(), "sampleTests must contain at least one test");
        if (q.hiddenTests() == null || q.hiddenTests().isEmpty())
            fail(source, q.id(), "hiddenTests must contain at least one test");
        checkTests(q.sampleTests(), "sampleTests", source, q.id());
        checkTests(q.hiddenTests(), "hiddenTests", source, q.id());
    }

    private static void checkTests(List<Question.TestCase> tests, String field, String source, String id) {
        for (int i = 0; i < tests.size(); i++) {
            Question.TestCase t = tests.get(i);
            if (t == null || t.input() == null)
                fail(source, id, field + "[" + i + "].input is required");
            if (t.expected() == null)
                fail(source, id, field + "[" + i + "].expected is required (use \"\" for void methods)");
        }
    }

    private static void fail(String source, String id, String reason) {
        throw new IllegalStateException("Invalid question '" + id + "' in file '" + source + "': " + reason + ".");
    }

    private static boolean blank(String s) {
        return s == null || s.isBlank();
    }

    private static String rootMessage(Throwable t) {
        Throwable cur = t;
        while (cur.getCause() != null && cur.getCause() != cur) cur = cur.getCause();
        return cur.getMessage() == null ? cur.toString() : cur.getMessage();
    }
}
