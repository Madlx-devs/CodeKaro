package com.example.dsa.harness;

import com.example.dsa.catalog.Question;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 * Generates the sandbox {@code Main.java} that wraps a user's LeetCode-style
 * {@code Solution} class: it reads all stdin lines, parses line <i>i</i> as
 * parameter <i>i</i> per the question's signature, invokes the method, and
 * prints the canonical serialization of the return value.
 *
 * The generated Main is compiled together with the user's Solution.java and
 * the shared Harness.java template (classpath:/harness/Harness.java).
 */
public final class HarnessGenerator {
    private HarnessGenerator() {}

    private static volatile String harnessSource;

    /** The shared Harness.java template compiled alongside user code in the sandbox. */
    public static String harnessSource() {
        String cached = harnessSource;
        if (cached != null) return cached;
        try (InputStream in = HarnessGenerator.class.getResourceAsStream("/harness/Harness.java")) {
            if (in == null) throw new IllegalStateException("Harness template not found at classpath:/harness/Harness.java");
            cached = new String(in.readAllBytes(), StandardCharsets.UTF_8);
            harnessSource = cached;
            return cached;
        } catch (IOException e) {
            throw new IllegalStateException("Failed to read harness template", e);
        }
    }

    /** Generates Main.java source for the given method signature. */
    public static String generateMain(Question.Signature sig) {        validateSignature(sig);
        List<Question.Param> params = sig.params() == null ? List.of() : sig.params();
        String args = params.stream().map(Question.Param::name).collect(Collectors.joining(", "));

        StringBuilder sb = new StringBuilder();
        sb.append("import java.util.*;\n");
        sb.append("public class Main {\n");
        sb.append("    public static void main(String[] args) throws Exception {\n");
        sb.append("        List<String> lines = Harness.readAllLines();\n");
        for (int i = 0; i < params.size(); i++) {
            Question.Param p = params.get(i);
            sb.append("        ").append(p.type()).append(' ').append(p.name())
              .append(" = Harness.").append(parseMethodFor(p.type()))
              .append("(Harness.line(lines, ").append(i).append("));\n");
        }
        String call = "new " + sig.className() + "()." + sig.methodName() + "(" + args + ")";
        if ("void".equals(sig.returnType())) {
            sb.append("        ").append(call).append(";\n");
        } else {
            sb.append("        ").append(sig.returnType()).append(" result = ").append(call).append(";\n");
            sb.append("        System.out.print(Harness.serialize(result));\n");
        }
        sb.append("    }\n");
        sb.append("}\n");
        return sb.toString();
    }

    /**
     * Generates Main.java for a catalog question, applying documented per-question
     * input conventions. Currently only {@code linked-list-cycle} needs one: a cycle
     * cannot be expressed in the plain {@code [1,2,3]} ListNode format, so that
     * question defines the single input line as an int array whose LAST element is
     * {@code pos} (the 0-based index the tail links to, -1 = no cycle) and the list
     * is built from the preceding elements.
     */
    public static String generateMainForQuestion(Question question) {
        if ("linked-list-cycle".equals(question.id())) {
            return generateLinkedListCycleMain(question.signature());
        }
        return generateMain(question.signature());
    }

    private static String generateLinkedListCycleMain(Question.Signature sig) {
        validateSignature(sig);
        StringBuilder sb = new StringBuilder();
        sb.append("import java.util.*;\n");
        sb.append("public class Main {\n");
        sb.append("    public static void main(String[] args) throws Exception {\n");
        sb.append("        List<String> lines = Harness.readAllLines();\n");
        sb.append("        int[] arr = Harness.parseIntArray(Harness.line(lines, 0));\n");
        sb.append("        int pos = arr.length == 0 ? -1 : arr[arr.length - 1];\n");
        sb.append("        List<ListNode> nodes = new ArrayList<>();\n");
        sb.append("        ListNode head = null, tail = null;\n");
        sb.append("        for (int i = 0; i + 1 < arr.length; i++) {\n");
        sb.append("            ListNode n = new ListNode(arr[i]);\n");
        sb.append("            nodes.add(n);\n");
        sb.append("            if (head == null) head = n; else tail.next = n;\n");
        sb.append("            tail = n;\n");
        sb.append("        }\n");
        sb.append("        if (pos >= 0 && tail != null && pos < nodes.size()) tail.next = nodes.get(pos);\n");
        sb.append("        boolean result = new ").append(sig.className()).append("().").append(sig.methodName()).append("(head);\n");
        sb.append("        System.out.print(Harness.serialize(result));\n");
        sb.append("    }\n");
        sb.append("}\n");
        return sb.toString();
    }

    private static final Pattern JAVA_IDENT = Pattern.compile("[A-Za-z_$][A-Za-z0-9_$]*");

    /**
     * Validates a signature before it is interpolated into generated Java source.
     * The catalog is validated at startup, but ad-hoc signatures arrive from the
     * client (/api/run), so this is a code-injection guard: identifiers must be
     * plain Java identifiers and types must be harness-supported.
     */
    public static void validateSignature(Question.Signature sig) {
        if (sig == null) throw new IllegalArgumentException("Signature is required for method mode.");
        if (sig.className() == null || !JAVA_IDENT.matcher(sig.className()).matches())
            throw new IllegalArgumentException("Invalid className in signature: " + sig.className());
        if (sig.methodName() == null || !JAVA_IDENT.matcher(sig.methodName()).matches())
            throw new IllegalArgumentException("Invalid methodName in signature: " + sig.methodName());
        if (sig.returnType() == null)
            throw new IllegalArgumentException("returnType is required in signature.");
        if (!"void".equals(sig.returnType())) parseMethodFor(sig.returnType());
        List<Question.Param> params = sig.params() == null ? List.of() : sig.params();
        for (Question.Param p : params) {
            if (p.name() == null || !JAVA_IDENT.matcher(p.name()).matches())
                throw new IllegalArgumentException("Invalid param name in signature: " + p.name());
            if ("void".equals(p.type()))
                throw new IllegalArgumentException("void is not allowed as a param type.");
            parseMethodFor(p.type());
        }
    }

    /** Maps a CONTRACT signature type to the Harness parse method for it. */
    public static String parseMethodFor(String type) {
        return switch (type) {
            case "int" -> "parseInt";
            case "long" -> "parseLong";
            case "double" -> "parseDouble";
            case "boolean" -> "parseBoolean";
            case "char" -> "parseChar";
            case "String" -> "parseString";
            case "int[]" -> "parseIntArray";
            case "long[]" -> "parseLongArray";
            case "double[]" -> "parseDoubleArray";
            case "boolean[]" -> "parseBooleanArray";
            case "char[]" -> "parseCharArray";
            case "String[]" -> "parseStringArray";
            case "int[][]" -> "parseInt2DArray";
            case "char[][]" -> "parseChar2DArray";
            case "ListNode" -> "parseListNode";
            case "TreeNode" -> "parseTreeNode";
            case "List<Integer>" -> "parseIntList";
            case "List<String>" -> "parseStringList";
            case "List<List<Integer>>" -> "parseInt2DList";
            default -> throw new IllegalArgumentException("Unsupported harness type: " + type);
        };
    }
}
