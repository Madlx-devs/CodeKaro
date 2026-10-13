package com.example.dsa.ai;

/** Thrown when the AI provider call fails; never carries the API key. */
public class AiException extends RuntimeException {
    public AiException(String message) {
        super(message);
    }

    public AiException(String message, Throwable cause) {
        super(message, cause);
    }
}
