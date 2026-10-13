package com.example.dsa.domain;

import java.io.Serializable;
import java.util.Objects;

public class BookmarkId implements Serializable {
    private Long userId;
    private String problemId;

    public BookmarkId() {}

    public BookmarkId(Long userId, String problemId) {
        this.userId = userId;
        this.problemId = problemId;
    }

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public String getProblemId() { return problemId; }
    public void setProblemId(String problemId) { this.problemId = problemId; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof BookmarkId other)) return false;
        return Objects.equals(userId, other.userId) && Objects.equals(problemId, other.problemId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(userId, problemId);
    }
}
