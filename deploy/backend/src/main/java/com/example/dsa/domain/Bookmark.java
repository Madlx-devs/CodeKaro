package com.example.dsa.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.IdClass;
import jakarta.persistence.Table;

import java.time.Instant;

@Entity
@Table(name = "bookmarks")
@IdClass(BookmarkId.class)
public class Bookmark {
    @Id
    @Column(name = "user_id")
    private Long userId;

    @Id
    @Column(name = "problem_id", length = 64)
    private String problemId;

    @Column(name = "created_at", nullable = false)
    private Instant createdAt;

    public Long getUserId() { return userId; }
    public void setUserId(Long userId) { this.userId = userId; }
    public String getProblemId() { return problemId; }
    public void setProblemId(String problemId) { this.problemId = problemId; }
    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
