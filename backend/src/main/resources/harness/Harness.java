// Harness support code compiled alongside the user's Solution in the sandbox.
// Provides ListNode/TreeNode definitions, stdin parsing for every harness-supported
// type, and canonical serialization of return values. Do NOT redefine ListNode or
// TreeNode in your Solution — these definitions are already on the classpath.
import java.util.*;

class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) { this.val = val; this.left = left; this.right = right; }
}

final class Harness {
    private Harness() {}

    /** Read all of stdin, split into lines, drop trailing empty lines. */
    static List<String> readAllLines() {
        try {
            byte[] bytes = System.in.readAllBytes();
            String text = new String(bytes, java.nio.charset.StandardCharsets.UTF_8);
            List<String> lines = new ArrayList<>(Arrays.asList(text.split("\n", -1)));
            for (int i = 0; i < lines.size(); i++) {
                String l = lines.get(i);
                if (l.endsWith("\r")) lines.set(i, l.substring(0, l.length() - 1));
            }
            for (int i = lines.size() - 1; i >= 0; i--) {
                if (lines.get(i).isEmpty()) lines.remove(i);
                else break;
            }
            return lines;
        } catch (Exception e) {
            throw new RuntimeException("Failed to read stdin", e);
        }
    }

    static String line(List<String> lines, int i) {
        return i < lines.size() ? lines.get(i) : "";
    }

    /** Split on top-level commas, respecting nested brackets and quoted strings. */
    static List<String> splitTopLevel(String s) {
        List<String> out = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        int depth = 0;
        boolean inStr = false;
        boolean esc = false;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (inStr) {
                cur.append(c);
                if (esc) esc = false;
                else if (c == '\\') esc = true;
                else if (c == '"') inStr = false;
            } else if (c == '"') {
                inStr = true;
                cur.append(c);
            } else if (c == '[') {
                depth++;
                cur.append(c);
            } else if (c == ']') {
                depth--;
                cur.append(c);
            } else if (c == ',' && depth == 0) {
                out.add(cur.toString().trim());
                cur.setLength(0);
            } else {
                cur.append(c);
            }
        }
        out.add(cur.toString().trim());
        return out;
    }

    static String inner(String s) {
        String t = s.trim();
        if (t.length() >= 2 && t.charAt(0) == '[' && t.charAt(t.length() - 1) == ']') {
            return t.substring(1, t.length() - 1);
        }
        throw new IllegalArgumentException("Expected a bracketed list like [1, 2], got: " + s);
    }

    /** Elements of a bracketed list; empty list yields no elements. */
    static List<String> elems(String s) {
        String in = inner(s).trim();
        if (in.isEmpty()) return new ArrayList<>();
        return splitTopLevel(in);
    }

    /** Remove surrounding double quotes and process backslash escapes, if present. */
    static String unquote(String s) {
        String t = s.trim();
        if (t.length() >= 2 && t.charAt(0) == '"' && t.charAt(t.length() - 1) == '"') {
            String body = t.substring(1, t.length() - 1);
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < body.length(); i++) {
                char c = body.charAt(i);
                if (c == '\\' && i + 1 < body.length()) {
                    char n = body.charAt(i + 1);
                    if (n == 'n') sb.append('\n');
                    else if (n == 't') sb.append('\t');
                    else if (n == 'r') sb.append('\r');
                    else sb.append(n);
                    i++;
                } else {
                    sb.append(c);
                }
            }
            return sb.toString();
        }
        return t;
    }

    static int parseInt(String s) { return Integer.parseInt(s.trim()); }
    static long parseLong(String s) { return Long.parseLong(s.trim()); }
    static double parseDouble(String s) { return Double.parseDouble(s.trim()); }
    static boolean parseBoolean(String s) { return Boolean.parseBoolean(s.trim()); }
    static char parseChar(String s) {
        String t = unquote(s);
        if (t.length() != 1) throw new IllegalArgumentException("Expected a single character, got: " + s);
        return t.charAt(0);
    }
    static String parseString(String s) { return unquote(s); }

    static int[] parseIntArray(String s) {
        List<String> e = elems(s);
        int[] a = new int[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseInt(e.get(i));
        return a;
    }
    static long[] parseLongArray(String s) {
        List<String> e = elems(s);
        long[] a = new long[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseLong(e.get(i));
        return a;
    }
    static double[] parseDoubleArray(String s) {
        List<String> e = elems(s);
        double[] a = new double[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseDouble(e.get(i));
        return a;
    }
    static boolean[] parseBooleanArray(String s) {
        List<String> e = elems(s);
        boolean[] a = new boolean[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseBoolean(e.get(i));
        return a;
    }
    static char[] parseCharArray(String s) {
        List<String> e = elems(s);
        char[] a = new char[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseChar(e.get(i));
        return a;
    }
    static String[] parseStringArray(String s) {
        List<String> e = elems(s);
        String[] a = new String[e.size()];
        for (int i = 0; i < e.size(); i++) a[i] = parseString(e.get(i));
        return a;
    }
    static int[][] parseInt2DArray(String s) {
        List<String> e = elems(s);
        int[][] a = new int[e.size()][];
        for (int i = 0; i < e.size(); i++) a[i] = parseIntArray(e.get(i));
        return a;
    }
    static char[][] parseChar2DArray(String s) {
        List<String> e = elems(s);
        char[][] a = new char[e.size()][];
        for (int i = 0; i < e.size(); i++) a[i] = parseCharArray(e.get(i));
        return a;
    }

    static ListNode parseListNode(String s) {
        int[] a = parseIntArray(s);
        ListNode dummy = new ListNode(0);
        ListNode cur = dummy;
        for (int v : a) {
            cur.next = new ListNode(v);
            cur = cur.next;
        }
        return dummy.next;
    }

    static TreeNode parseTreeNode(String s) {
        List<String> toks = elems(s);
        if (toks.isEmpty()) return null;
        List<TreeNode> nodes = new ArrayList<>();
        for (String t : toks) nodes.add(t.equalsIgnoreCase("null") ? null : new TreeNode(parseInt(t)));
        TreeNode root = nodes.get(0);
        if (root == null) return null;
        Queue<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < nodes.size()) {
            TreeNode n = q.poll();
            TreeNode left = i < nodes.size() ? nodes.get(i++) : null;
            TreeNode right = i < nodes.size() ? nodes.get(i++) : null;
            n.left = left;
            n.right = right;
            if (left != null) q.add(left);
            if (right != null) q.add(right);
        }
        return root;
    }

    static List<Integer> parseIntList(String s) {
        List<String> e = elems(s);
        List<Integer> l = new ArrayList<>();
        for (String x : e) l.add(parseInt(x));
        return l;
    }
    static List<String> parseStringList(String s) {
        List<String> e = elems(s);
        List<String> l = new ArrayList<>();
        for (String x : e) l.add(parseString(x));
        return l;
    }
    static List<List<Integer>> parseInt2DList(String s) {
        List<String> e = elems(s);
        List<List<Integer>> l = new ArrayList<>();
        for (String x : e) l.add(parseIntList(x));
        return l;
    }

    // ---- Canonical serialization (must match the CONTRACT exactly) ----

    static String serialize(Object o) {
        if (o == null) return "null";
        if (o instanceof Double) return Double.toString((Double) o);
        if (o instanceof Float) return Float.toString((Float) o);
        if (o instanceof int[]) return join((int[]) o);
        if (o instanceof long[]) return join((long[]) o);
        if (o instanceof double[]) return join((double[]) o);
        if (o instanceof boolean[]) return join((boolean[]) o);
        if (o instanceof char[]) return join((char[]) o);
        if (o instanceof String[]) return join((String[]) o);
        if (o instanceof int[][]) return join((int[][]) o);
        if (o instanceof char[][]) return join((char[][]) o);
        if (o instanceof ListNode) return serializeListNode((ListNode) o);
        if (o instanceof TreeNode) return serializeTree((TreeNode) o);
        if (o instanceof List) {
            List<?> l = (List<?>) o;
            StringBuilder sb = new StringBuilder("[");
            for (int i = 0; i < l.size(); i++) {
                if (i > 0) sb.append(", ");
                sb.append(serialize(l.get(i)));
            }
            return sb.append("]").toString();
        }
        return o.toString();
    }

    static String join(int[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        return sb.append("]").toString();
    }
    static String join(long[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        return sb.append("]").toString();
    }
    static String join(double[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(Double.toString(a[i]));
        }
        return sb.append("]").toString();
    }
    static String join(boolean[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        return sb.append("]").toString();
    }
    static String join(char[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        return sb.append("]").toString();
    }
    static String join(String[] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        return sb.append("]").toString();
    }
    static String join(int[][] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(join(a[i]));
        }
        return sb.append("]").toString();
    }
    static String join(char[][] a) {
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(join(a[i]));
        }
        return sb.append("]").toString();
    }

    static String serializeListNode(ListNode head) {
        StringBuilder sb = new StringBuilder("[");
        boolean first = true;
        for (ListNode n = head; n != null; n = n.next) {
            if (!first) sb.append(", ");
            sb.append(n.val);
            first = false;
        }
        return sb.append("]").toString();
    }

    static String serializeTree(TreeNode root) {
        if (root == null) return "null";
        List<String> vals = new ArrayList<>();
        Queue<TreeNode> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            TreeNode n = q.poll();
            if (n == null) {
                vals.add("null");
            } else {
                vals.add(String.valueOf(n.val));
                q.add(n.left);
                q.add(n.right);
            }
        }
        int end = vals.size();
        while (end > 0 && vals.get(end - 1).equals("null")) end--;
        return "[" + String.join(", ", vals.subList(0, end)) + "]";
    }
}
