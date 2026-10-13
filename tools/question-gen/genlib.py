"""Shared generator library for DSA question-bank JSON files.

Every question's test inputs are expressed as native Python values; expected
outputs are COMPUTED by running a reference solution (never hand-computed).
Input strings and expected strings follow the harness I/O format in CONTRACT.md.
"""
import json
import os

OUT_DIR = os.path.expanduser("~/workspace/dsa-platform/questions")

SCALAR = {"int", "long", "double", "boolean", "char", "String"}


def fmt_double(v):
    s = repr(float(v))
    assert "e" not in s and "E" not in s and "inf" not in s.lower(), f"unsafe double: {v!r}"
    return s


def fmt_scalar(v, t):
    if t == "double":
        return fmt_double(v)
    if t == "boolean":
        return "true" if v else "false"
    return str(v)  # int, long, char, String -> raw


def fmt_param(v, t):
    """Format one parameter value as a harness stdin line."""
    if t in SCALAR:
        return fmt_scalar(v, t)
    if t == "int[]":
        return "[" + ", ".join(str(x) for x in v) + "]"
    if t == "String[]":
        # contract: String[] elements may be quoted
        return "[" + ", ".join('"%s"' % x for x in v) + "]"
    if t == "int[][]":
        return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in v) + "]"
    if t == "List<Integer>":
        return "[" + ", ".join(str(x) for x in v) + "]"
    if t == "List<List<Integer>>":
        return "[" + ", ".join("[" + ", ".join(str(x) for x in row) + "]" for row in v) + "]"
    raise ValueError(f"unsupported param type: {t}")


def ser(v):
    """Canonical serialization of a return value (mirrors harness output)."""
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return fmt_double(v)
    if isinstance(v, int):
        return str(v)
    if isinstance(v, str):
        return v
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(ser(x) for x in v) + "]"
    raise ValueError(f"cannot serialize: {v!r}")


def starter_code(return_type, method_name, params):
    """Build valid Java starter code matching the signature."""
    ps = ", ".join(f"{t} {n}" for n, t in params)
    body = (
        "class Solution {\n"
        f"    public {return_type} {method_name}({ps}) {{\n"
        "        \n"
        "    }\n"
        "}"
    )
    needs_import = any("List" in t or "Map" in t or "Set" in t
                       for t in [return_type] + [t for _, t in params])
    return ("import java.util.*;\n\n" + body) if needs_import else body


REQUIRED_FIELDS = {"id", "title", "pattern", "difficulty", "description", "examples",
                   "constraints", "signature", "starterCode", "sampleTests",
                   "hiddenTests", "tags", "timeComplexity", "spaceComplexity", "hints"}


def make_question(*, id, title, pattern, difficulty, description, examples,
                  constraints, method_name, return_type, params,
                  sample_args, hidden_args, ref, tags,
                  time_complexity, space_complexity, hints):
    param_types = [t for _, t in params]
    tests = []
    for args in sample_args + hidden_args:
        assert len(args) == len(params), f"{id}: arg count mismatch"
        inp = "\n".join(fmt_param(a, t) for a, t in zip(args, param_types))
        exp = ser(ref(*args))
        tests.append({"input": inp, "expected": exp})
    n_s, n_h = len(sample_args), len(hidden_args)
    assert 2 <= n_s <= 3, f"{id}: need 2-3 sample tests"
    assert 5 <= n_h <= 10, f"{id}: need 5-10 hidden tests"
    assert all(h["input"] for h in tests), f"{id}: empty test input"
    assert len(hints) in (2, 3), f"{id}: need 2-3 hints"
    return {
        "id": id,
        "title": title,
        "pattern": pattern,
        "difficulty": difficulty,
        "description": description,
        "examples": [{"input": i, "output": o, "explanation": e} for i, o, e in examples],
        "constraints": constraints,
        "signature": {
            "className": "Solution",
            "methodName": method_name,
            "returnType": return_type,
            "params": [{"name": n, "type": t} for n, t in params],
        },
        "starterCode": starter_code(return_type, method_name, params),
        "sampleTests": tests[:n_s],
        "hiddenTests": tests[n_s:],
        "tags": tags,
        "timeComplexity": time_complexity,
        "spaceComplexity": space_complexity,
        "hints": hints,
    }


def write_bank(pattern, questions):
    assert len(questions) == 20, f"{pattern}: need exactly 20 questions, got {len(questions)}"
    counts = {"Easy": 0, "Medium": 0, "Hard": 0}
    seen = set()
    for qd in questions:
        assert set(qd.keys()) == REQUIRED_FIELDS, f"{qd.get('id')}: field mismatch {set(qd.keys()) ^ REQUIRED_FIELDS}"
        assert qd["id"] not in seen, f"duplicate id {qd['id']}"
        seen.add(qd["id"])
        assert qd["pattern"] == pattern
        counts[qd["difficulty"]] += 1
    assert counts == {"Easy": 8, "Medium": 8, "Hard": 4}, f"{pattern}: bad mix {counts}"
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{pattern}.json")
    with open(path, "w") as f:
        json.dump(questions, f, indent=2)
        f.write("\n")
    # validate the file round-trips as a JSON array
    with open(path) as f:
        data = json.load(f)
    assert isinstance(data, list) and len(data) == 20
    print(f"wrote {path}  (Easy {counts['Easy']}, Medium {counts['Medium']}, Hard {counts['Hard']})")
    return path
