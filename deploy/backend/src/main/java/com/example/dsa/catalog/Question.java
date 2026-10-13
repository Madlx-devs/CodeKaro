package com.example.dsa.catalog;

import java.util.List;

/** A single DSA question, exactly matching the CONTRACT's question JSON schema. */
public record Question(
        String id,
        String title,
        String pattern,
        String difficulty,
        String description,
        List<Example> examples,
        List<String> constraints,
        Signature signature,
        String starterCode,
        List<TestCase> sampleTests,
        List<TestCase> hiddenTests,
        List<String> tags,
        String timeComplexity,
        String spaceComplexity,
        List<String> hints) {

    public record Example(String input, String output, String explanation) {}

    public record Signature(String className, String methodName, String returnType, List<Param> params) {}

    public record Param(String name, String type) {}

    public record TestCase(String input, String expected) {}
}
