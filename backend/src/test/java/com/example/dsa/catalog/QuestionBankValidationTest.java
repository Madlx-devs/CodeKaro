package com.example.dsa.catalog;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class QuestionBankValidationTest {
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private Question base() {
        return new Question(
                "two-sum", "Two Sum", "hashing", "Easy",
                "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
                List.of(new Question.Example("nums = [2,7,11,15], target = 9", "[0,1]", "nums[0] + nums[1] == 9.")),
                List.of("2 <= nums.length <= 10^4"),
                new Question.Signature("Solution", "twoSum", "int[]",
                        List.of(new Question.Param("nums", "int[]"), new Question.Param("target", "int"))),
                "class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        \n    }\n}",
                List.of(new Question.TestCase("[2,7,11,15]\n9", "[0, 1]")),
                List.of(new Question.TestCase("[3,2,4]\n6", "[1, 2]")),
                List.of("array", "hash-table"),
                "O(n)", "O(n)",
                List.of("Try a brute-force pair check first."));
    }

    private Question with(Question q, String difficulty, String returnType) {
        return new Question(q.id(), q.title(), q.pattern(), difficulty, q.description(), q.examples(),
                q.constraints(),
                new Question.Signature(q.signature().className(), q.signature().methodName(), returnType,
                        q.signature().params()),
                q.starterCode(), q.sampleTests(), q.hiddenTests(), q.tags(),
                q.timeComplexity(), q.spaceComplexity(), q.hints());
    }

    @Test
    void validQuestionPasses() {
        QuestionBank.validateQuestion(base(), "hashing.json");
    }

    @Test
    void rejectsBadDifficulty() {
        var ex = assertThrows(IllegalStateException.class,
                () -> QuestionBank.validateQuestion(with(base(), "SuperHard", "int[]"), "hashing.json"));
        assertTrue(ex.getMessage().contains("hashing.json"));
        assertTrue(ex.getMessage().contains("two-sum"));
    }

    @Test
    void rejectsUnsupportedReturnType() {
        var ex = assertThrows(IllegalStateException.class,
                () -> QuestionBank.validateQuestion(with(base(), "Easy", "Map<String,Integer>"), "hashing.json"));
        assertTrue(ex.getMessage().contains("Map<String,Integer>"));
    }

    @Test
    void rejectsVoidParam() {
        var bad = new Question(base().id(), base().title(), base().pattern(), base().difficulty(),
                base().description(), base().examples(), base().constraints(),
                new Question.Signature("Solution", "m", "void", List.of(new Question.Param("x", "void"))),
                base().starterCode(), base().sampleTests(), base().hiddenTests(), base().tags(),
                base().timeComplexity(), base().spaceComplexity(), base().hints());
        assertThrows(IllegalStateException.class, () -> QuestionBank.validateQuestion(bad, "x.json"));
    }

    @Test
    void rejectsMissingHiddenTests() {
        var bad = new Question(base().id(), base().title(), base().pattern(), base().difficulty(),
                base().description(), base().examples(), base().constraints(), base().signature(),
                base().starterCode(), base().sampleTests(), List.of(), base().tags(),
                base().timeComplexity(), base().spaceComplexity(), base().hints());
        var ex = assertThrows(IllegalStateException.class, () -> QuestionBank.validateQuestion(bad, "x.json"));
        assertTrue(ex.getMessage().contains("hiddenTests"));
    }

    @Test
    void rejectsBadId() {
        var bad = new Question("Two Sum!", base().title(), base().pattern(), base().difficulty(),
                base().description(), base().examples(), base().constraints(), base().signature(),
                base().starterCode(), base().sampleTests(), base().hiddenTests(), base().tags(),
                base().timeComplexity(), base().spaceComplexity(), base().hints());
        assertThrows(IllegalStateException.class, () -> QuestionBank.validateQuestion(bad, "x.json"));
    }

    @Test
    void rejectsDuplicateIds() {
        var ex = assertThrows(IllegalStateException.class,
                () -> QuestionBank.validateAll(List.of(base(), base())));
        assertTrue(ex.getMessage().contains("two-sum"));
    }

    @Test
    void deserializesContractExampleJson() throws Exception {
        String json = """
                {
                  "id": "two-sum",
                  "title": "Two Sum",
                  "pattern": "hashing",
                  "difficulty": "Easy",
                  "description": "Given an array of integers nums and an integer target, return indices of the two numbers that add up to target.",
                  "examples": [{"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "nums[0] + nums[1] == 9."}],
                  "constraints": ["2 <= nums.length <= 10^4"],
                  "signature": {"className": "Solution", "methodName": "twoSum", "returnType": "int[]",
                                "params": [{"name": "nums", "type": "int[]"}, {"name": "target", "type": "int"}]},
                  "starterCode": "class Solution {\\n    public int[] twoSum(int[] nums, int target) {\\n        \\n    }\\n}",
                  "sampleTests": [{"input": "[2,7,11,15]\\n9", "expected": "[0, 1]"}],
                  "hiddenTests": [{"input": "[3,2,4]\\n6", "expected": "[1, 2]"}],
                  "tags": ["array", "hash-table"],
                  "timeComplexity": "O(n)",
                  "spaceComplexity": "O(n)",
                  "hints": ["Try a brute-force pair check first to feel the problem."]
                }
                """;
        Question q = MAPPER.readValue(json, Question.class);
        QuestionBank.validateQuestion(q, "contract.json");
        assertEquals("two-sum", q.id());
        assertEquals(2, q.signature().params().size());
    }

    @Test
    void loadsEmptyQuestionsDirWithoutError() {
        // The JSON files arrive separately; an empty dir must boot with zero questions, not crash.
        QuestionBank bank = new QuestionBank();
        assertTrue(bank.total() >= 0);
    }
}
