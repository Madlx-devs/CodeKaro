package com.example.dsa.harness;

import com.example.dsa.catalog.Question;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

/**
 * Real end-to-end verification of the generated harness: writes the Harness
 * template + generated Main + a sample Solution to a temp dir, compiles with
 * javac and runs with java. Skipped when no JDK is on PATH.
 */
class HarnessRoundTripTest {
    @TempDir
    Path tmp;

    private static boolean jdkAvailable() {
        try {
            Process p = new ProcessBuilder("javac", "-version").redirectErrorStream(true).start();
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            try (InputStream in = p.getInputStream()) {
                in.transferTo(out);
            }
            return p.waitFor(10, TimeUnit.SECONDS) && p.exitValue() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    private String compileAndRun(String solutionSrc, Question.Signature sig, String stdin) throws Exception {
        Files.writeString(tmp.resolve("Harness.java"), HarnessGenerator.harnessSource(), StandardCharsets.UTF_8);
        Files.writeString(tmp.resolve("Main.java"), HarnessGenerator.generateMain(sig), StandardCharsets.UTF_8);
        Files.writeString(tmp.resolve("Solution.java"), solutionSrc, StandardCharsets.UTF_8);

        Process compile = new ProcessBuilder("javac", "-encoding", "UTF-8",
                "Harness.java", "Main.java", "Solution.java")
                .directory(tmp.toFile()).redirectErrorStream(true).start();
        String compileOut = readAll(compile.getInputStream());
        assertTrue(compile.waitFor(30, TimeUnit.SECONDS), "javac hung");
        assertEquals(0, compile.exitValue(), "javac failed:\n" + compileOut);

        Process run = new ProcessBuilder("java", "Main")
                .directory(tmp.toFile()).redirectErrorStream(true).start();
        try (OutputStream os = run.getOutputStream()) {
            os.write(stdin.getBytes(StandardCharsets.UTF_8));
        }
        String stdout = readAll(run.getInputStream());
        assertTrue(run.waitFor(15, TimeUnit.SECONDS), "java hung");
        assertEquals(0, run.exitValue(), "java failed:\n" + stdout);
        return stdout;
    }

    private static String readAll(InputStream in) throws Exception {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        in.transferTo(out);
        return out.toString(StandardCharsets.UTF_8);
    }

    @Test
    void twoSumEndToEnd() throws Exception {
        assumeTrue(jdkAvailable(), "JDK not on PATH; skipping harness execution test");
        var sig = new Question.Signature("Solution", "twoSum", "int[]",
                List.of(new Question.Param("nums", "int[]"), new Question.Param("target", "int")));
        String solution = """
                class Solution {
                    public int[] twoSum(int[] nums, int target) {
                        java.util.Map<Integer, Integer> seen = new java.util.HashMap<>();
                        for (int i = 0; i < nums.length; i++) {
                            int need = target - nums[i];
                            if (seen.containsKey(need)) return new int[]{seen.get(need), i};
                            seen.put(nums[i], i);
                        }
                        return new int[0];
                    }
                }
                """;
        assertEquals("[0, 1]", compileAndRun(solution, sig, "[2,7,11,15]\n9\n"));
    }

    @Test
    void allTypesParseAndSerializeRoundTrip() throws Exception {
        assumeTrue(jdkAvailable(), "JDK not on PATH; skipping harness execution test");
        var sig = new Question.Signature("Solution", "probe", "String", List.of(
                new Question.Param("a", "int"),
                new Question.Param("b", "long"),
                new Question.Param("c", "double"),
                new Question.Param("d", "boolean"),
                new Question.Param("e", "char"),
                new Question.Param("f", "String"),
                new Question.Param("g", "int[]"),
                new Question.Param("h", "String[]"),
                new Question.Param("i", "int[][]"),
                new Question.Param("j", "ListNode"),
                new Question.Param("k", "TreeNode"),
                new Question.Param("l", "List<Integer>"),
                new Question.Param("m", "List<String>"),
                new Question.Param("n", "List<List<Integer>>")));
        String solution = """
                class Solution {
                    public String probe(int a, long b, double c, boolean d, char e, String f,
                                        int[] g, String[] h, int[][] i, ListNode j, TreeNode k,
                                        java.util.List<Integer> l, java.util.List<String> m,
                                        java.util.List<java.util.List<Integer>> n) {
                        return a + "|" + b + "|" + c + "|" + d + "|" + e + "|" + f + "|"
                                + Harness.serialize(g) + "|" + Harness.serialize(h) + "|"
                                + Harness.serialize(i) + "|" + Harness.serialize(j) + "|"
                                + Harness.serialize(k) + "|" + Harness.serialize(l) + "|"
                                + Harness.serialize(m) + "|" + Harness.serialize(n);
                    }
                }
                """;
        String stdin = String.join("\n",
                "42",
                "1234567890123",
                "2.5",
                "true",
                "x",
                "hello world",
                "[1, 2, 3]",
                "[\"a\", \"b\"]",
                "[[1, 2], [3]]",
                "[7, 8]",
                "[3, 5, 1, null, null, 6]",
                "[9, 8]",
                "[\"p\", \"q\"]",
                "[[1], [2, 3]]") + "\n";
        String expected = "42|1234567890123|2.5|true|x|hello world"
                + "|[1, 2, 3]|[a, b]|[[1, 2], [3]]|[7, 8]|[3, 5, 1, null, null, 6]"
                + "|[9, 8]|[p, q]|[[1], [2, 3]]";
        assertEquals(expected, compileAndRun(solution, sig, stdin));
    }

    @Test
    void voidMethodProducesNoSerializedOutput() throws Exception {
        assumeTrue(jdkAvailable(), "JDK not on PATH; skipping harness execution test");
        var sig = new Question.Signature("Solution", "greet", "void",
                List.of(new Question.Param("name", "String")));
        String solution = """
                class Solution {
                    public void greet(String name) {
                        System.out.print("hi " + name);
                    }
                }
                """;
        assertEquals("hi bob", compileAndRun(solution, sig, "bob\n"));
    }
}
