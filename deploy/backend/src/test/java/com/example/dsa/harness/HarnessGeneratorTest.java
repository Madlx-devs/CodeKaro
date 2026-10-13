package com.example.dsa.harness;

import com.example.dsa.catalog.Question;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class HarnessGeneratorTest {

    private static Question.Signature sig(String returnType, Question.Param... params) {
        return new Question.Signature("Solution", "solve", returnType, List.of(params));
    }

    private static Question.Param p(String name, String type) {
        return new Question.Param(name, type);
    }

    @Test
    void generatesCorrectParseCallsForEverySupportedType() {
        var s = sig("List<List<Integer>>",
                p("a", "int"), p("b", "long"), p("c", "double"), p("d", "boolean"),
                p("e", "char"), p("f", "String"),
                p("g", "int[]"), p("h", "long[]"), p("i", "double[]"),
                p("j", "boolean[]"), p("k", "char[]"), p("l", "String[]"),
                p("m", "int[][]"), p("n", "char[][]"),
                p("o", "ListNode"), p("q", "TreeNode"),
                p("r", "List<Integer>"), p("t", "List<String>"), p("u", "List<List<Integer>>"));
        String main = HarnessGenerator.generateMain(s);

        assertTrue(main.contains("public class Main"));
        assertTrue(main.contains("int a = Harness.parseInt(Harness.line(lines, 0));"));
        assertTrue(main.contains("long b = Harness.parseLong(Harness.line(lines, 1));"));
        assertTrue(main.contains("double c = Harness.parseDouble(Harness.line(lines, 2));"));
        assertTrue(main.contains("boolean d = Harness.parseBoolean(Harness.line(lines, 3));"));
        assertTrue(main.contains("char e = Harness.parseChar(Harness.line(lines, 4));"));
        assertTrue(main.contains("String f = Harness.parseString(Harness.line(lines, 5));"));
        assertTrue(main.contains("int[] g = Harness.parseIntArray(Harness.line(lines, 6));"));
        assertTrue(main.contains("long[] h = Harness.parseLongArray(Harness.line(lines, 7));"));
        assertTrue(main.contains("double[] i = Harness.parseDoubleArray(Harness.line(lines, 8));"));
        assertTrue(main.contains("boolean[] j = Harness.parseBooleanArray(Harness.line(lines, 9));"));
        assertTrue(main.contains("char[] k = Harness.parseCharArray(Harness.line(lines, 10));"));
        assertTrue(main.contains("String[] l = Harness.parseStringArray(Harness.line(lines, 11));"));
        assertTrue(main.contains("int[][] m = Harness.parseInt2DArray(Harness.line(lines, 12));"));
        assertTrue(main.contains("char[][] n = Harness.parseChar2DArray(Harness.line(lines, 13));"));
        assertTrue(main.contains("ListNode o = Harness.parseListNode(Harness.line(lines, 14));"));
        assertTrue(main.contains("TreeNode q = Harness.parseTreeNode(Harness.line(lines, 15));"));
        assertTrue(main.contains("List<Integer> r = Harness.parseIntList(Harness.line(lines, 16));"));
        assertTrue(main.contains("List<String> t = Harness.parseStringList(Harness.line(lines, 17));"));
        assertTrue(main.contains("List<List<Integer>> u = Harness.parseInt2DList(Harness.line(lines, 18));"));

        assertTrue(main.contains("List<List<Integer>> result = new Solution().solve("));
        assertTrue(main.contains("System.out.print(Harness.serialize(result));"));
    }

    @Test
    void voidReturnProducesNoOutput() {
        String main = HarnessGenerator.generateMain(sig("void", p("x", "int")));
        assertTrue(main.contains("new Solution().solve(x);"));
        assertFalse(main.contains("serialize"));
    }

    @Test
    void twoSumShapeMatchesContract() {
        var s = new Question.Signature("Solution", "twoSum", "int[]",
                List.of(p("nums", "int[]"), p("target", "int")));
        String main = HarnessGenerator.generateMain(s);
        assertTrue(main.contains("int[] nums = Harness.parseIntArray(Harness.line(lines, 0));"));
        assertTrue(main.contains("int target = Harness.parseInt(Harness.line(lines, 1));"));
        assertTrue(main.contains("int[] result = new Solution().twoSum(nums, target);"));
    }

    @Test
    void rejectsNullSignature() {
        assertThrows(IllegalArgumentException.class, () -> HarnessGenerator.generateMain(null));
    }

    @Test
    void rejectsUnsupportedType() {
        assertThrows(IllegalArgumentException.class, () -> HarnessGenerator.parseMethodFor("Map<String,Integer>"));
    }

    @Test
    void validateSignatureRejectsCodeInjection() {
        // A hostile client must not be able to smuggle code through signature identifiers.
        var evil = new Question.Signature("Solution", "x(); System.exit(0); //", "int",
                List.of(new Question.Param("a", "int")));
        assertThrows(IllegalArgumentException.class, () -> HarnessGenerator.validateSignature(evil));
        var evilParam = new Question.Signature("Solution", "solve", "int",
                List.of(new Question.Param("a\"; Runtime.getRuntime().exec(\"x", "int")));
        assertThrows(IllegalArgumentException.class, () -> HarnessGenerator.validateSignature(evilParam));
        var good = new Question.Signature("Solution", "twoSum", "int[]",
                List.of(new Question.Param("nums", "int[]"), new Question.Param("target", "int")));
        HarnessGenerator.validateSignature(good); // must not throw
    }

    @Test
    void harnessTemplateShipsWithRequiredHelpers() {
        String h = HarnessGenerator.harnessSource();
        assertTrue(h.contains("class ListNode"));
        assertTrue(h.contains("class TreeNode"));
        assertTrue(h.contains("class Harness"));
        for (String m : List.of("parseIntArray", "parseLongArray", "parseDoubleArray", "parseBooleanArray",
                "parseCharArray", "parseStringArray", "parseInt2DArray", "parseChar2DArray",
                "parseListNode", "parseTreeNode", "parseIntList", "parseStringList", "parseInt2DList",
                "parseChar", "parseString", "serialize", "readAllLines")) {
            assertTrue(h.contains(m), "harness template missing: " + m);
        }
    }
}
