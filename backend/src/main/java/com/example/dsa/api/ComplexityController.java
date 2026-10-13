package com.example.dsa.api;

import com.example.dsa.complexity.ComplexityAnalyzer;
import com.example.dsa.exec.ExecutionService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@RestController
@RequestMapping("/api")
public class ComplexityController {
    private final ComplexityAnalyzer analyzer;

    public ComplexityController(ComplexityAnalyzer analyzer) {
        this.analyzer = analyzer;
    }

    public record ComplexityRequest(String code) {}
    public record ComplexityResponse(String time, String space, String confidence,
                                     List<String> signals, String explanation, String caveat) {}

    @PostMapping("/complexity")
    public ComplexityResponse complexity(@RequestBody ComplexityRequest request) {
        String code = request == null ? null : request.code();
        if (code == null || code.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Java source code is required.");
        }
        if (code.length() > ExecutionService.MAX_CODE) {
            throw new ResponseStatusException(HttpStatus.PAYLOAD_TOO_LARGE, "Code exceeds 30,000 characters.");
        }
        ComplexityAnalyzer.Analysis a = analyzer.analyze(code);
        return new ComplexityResponse(a.time(), a.space(), a.confidence(), a.signals(), a.explanation(), a.caveat());
    }
}
