package com.example.dsa.complexity;

import org.springframework.stereotype.Component;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Heuristic source-pattern complexity analysis. This is NOT a formal static
 * analyzer: it reports structural signals found in the code and labels every
 * estimate as heuristic. The {@code explanation} field walks through the
 * reasoning in plain language.
 */
@Component
public class ComplexityAnalyzer {

    public record Analysis(String time, String space, String confidence,
                           List<String> signals, String explanation, String caveat) {}

    public Analysis analyze(String code) {
        String src = code == null ? "" : code;
        String stripped = src
                .replaceAll("(?s)/\\*.*?\\*/", " ")
                .replaceAll("//[^\\n]*", " ")
                .replaceAll("\"(?:\\\\.|[^\"\\\\])*\"", "\"\"")
                .replaceAll("'(?:\\\\.|[^'\\\\])*'", "''");

        int loops = count(stripped, "\\b(for|while|do)\\b");
        int nested = estimateNestedLoops(stripped);
        boolean recursion = Pattern.compile("\\b([A-Za-z_$][\\w$]*)\\s*\\([^;{}]*\\)\\s*\\{[^{}]*\\b\\1\\s*\\(")
                .matcher(stripped).find();
        boolean sort = Pattern.compile("\\.sort\\s*\\(|Arrays\\.sort\\s*\\(|Collections\\.sort\\s*\\(")
                .matcher(stripped).find();
        boolean mapLike = Pattern.compile("\\b(HashMap|HashSet|TreeMap|TreeSet|LinkedHashMap|LinkedHashSet|Map|Set|PriorityQueue|ArrayList|ArrayDeque|StringBuilder)\\b")
                .matcher(stripped).find();
        boolean streams = Pattern.compile("\\.stream\\s*\\(").matcher(stripped).find();

        List<String> signals = new ArrayList<>();
        String time;
        if (nested >= 2) {
            time = "Potentially O(n^" + nested + ")";
            signals.add("Detected loop nesting depth " + nested + "; confirm each level traverses input-sized data.");
        } else if (loops > 0 && nested == 1) {
            time = "Potentially O(n)";
            signals.add("Detected " + loops + " loop keyword(s) at a single nesting level; assumes linear iteration bounds.");
        } else if (sort) {
            time = "Potentially O(n log n)";
            signals.add("Detected a sorting call, which typically dominates at O(n log n).");
        } else if (recursion) {
            time = "Recursion detected; recurrence unknown";
            signals.add("A possible self-call was detected; branching factor and depth determine the real complexity.");
        } else {
            time = "Not confidently inferred";
            signals.add("No clear loop, recursion, or sorting signature was found; library calls and hidden work may dominate.");
        }
        if (streams) signals.add("Detected stream pipeline(s); terminal operations usually scan the source once per pipeline.");

        String space;
        if (mapLike) {
            space = "Potential O(n) auxiliary space";
            signals.add("Detected map/set/list/queue-like structures; actual stored element count determines space.");
        } else if (recursion) {
            space = "Call-stack space depends on recursion depth";
        } else {
            space = "Not confidently inferred";
        }

        String explanation = buildExplanation(loops, nested, recursion, sort, mapLike, streams, time, space);

        return new Analysis(time, space, "Low — heuristic only", signals, explanation,
                "This is a source-pattern heuristic, not a formal static analyzer. It can be wrong for "
                + "nested loops with bounded ranges, recursion, helper methods, library calls, or "
                + "input-dependent branches. Validate against the algorithm and the problem constraints.");
    }

    private String buildExplanation(int loops, int nested, boolean recursion, boolean sort,
                                    boolean mapLike, boolean streams, String time, String space) {
        StringBuilder sb = new StringBuilder();
        sb.append("I stripped comments and string literals, then scanned the code structure. ");
        if (loops == 0 && !recursion && !sort) {
            sb.append("I found no loop keywords, no self-recursive calls, and no sorting calls, so there is "
                    + "no structural evidence for a complexity claim — the real work may hide inside library "
                    + "calls (for example, a single `Collections.sort` or stream pipeline) or helper methods. ");
        } else {
            if (loops > 0) {
                sb.append("I found ").append(loops).append(loops == 1 ? " loop keyword" : " loop keywords")
                  .append(" (for/while/do)");
                if (nested >= 2) {
                    sb.append(" with a maximum nesting depth of ").append(nested)
                      .append(": each nesting level multiplies the work, which is the classic signature of an O(n^")
                      .append(nested).append(") approach — provided every level really iterates over input-sized data. ");
                } else {
                    sb.append(" at a single nesting level, which usually means each element is visited a constant "
                            + "number of times: the signature of linear O(n) work. ");
                }
            }
            if (sort) sb.append("A sorting call is present; sorting typically costs O(n log n) and dominates any linear scans around it. ");
            if (recursion) sb.append("I detected a method that appears to call itself. For recursion, count the branching factor "
                    + "(how many recursive calls per invocation) and the depth: e.g. two calls per level over depth d gives O(2^d). ");
            if (streams) sb.append("Stream pipelines usually scan their source once per terminal operation. ");
        }
        if (mapLike) {
            sb.append("For space: the code allocates map/set/list-like structures, so auxiliary space grows with the "
                    + "number of stored elements — typically O(n) in the worst case. ");
        } else if (recursion) {
            sb.append("For space: with recursion, the call stack holds one frame per active call, so space follows the recursion depth. ");
        } else {
            sb.append("For space: I saw no obvious auxiliary collections, so beyond the input itself there is no strong signal — "
                    + "a single scalar accumulator would be O(1). ");
        }
        sb.append("Bottom line: time ").append(time).append("; space ").append(space).append(".");
        return sb.toString();
    }

    private int count(String s, String regex) {
        Matcher m = Pattern.compile(regex).matcher(s);
        int n = 0;
        while (m.find()) n++;
        return n;
    }

    private int estimateNestedLoops(String s) {
        String[] lines = s.split("\\n");
        int depth = 0, max = 0;
        Deque<Integer> loopDepths = new ArrayDeque<>();
        for (String line : lines) {
            boolean loop = Pattern.compile("\\b(for|while)\\s*\\(").matcher(line).find();
            if (loop) {
                loopDepths.push(depth);
                max = Math.max(max, loopDepths.size());
            }
            for (char c : line.toCharArray()) {
                if (c == '{') depth++;
                else if (c == '}') {
                    depth = Math.max(0, depth - 1);
                    while (!loopDepths.isEmpty() && loopDepths.peek() > depth) loopDepths.pop();
                }
            }
        }
        return max;
    }
}
