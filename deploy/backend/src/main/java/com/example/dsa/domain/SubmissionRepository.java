package com.example.dsa.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.time.Instant;
import java.util.List;

public interface SubmissionRepository extends JpaRepository<Submission, Long> {
    List<Submission> findByUserIdOrderByCreatedAtDesc(Long userId);

    List<Submission> findByUserIdAndProblemIdOrderByCreatedAtDesc(Long userId, String problemId);

    @Query("select distinct s.problemId from Submission s where s.userId = :userId and s.verdict = 'Accepted'")
    List<String> solvedProblemIds(Long userId);

    @Query("select distinct s.problemId from Submission s where s.userId = :userId")
    List<String> attemptedProblemIds(Long userId);

    @Query("select s.createdAt from Submission s where s.userId = :userId and s.verdict = 'Accepted'")
    List<Instant> acceptedTimestamps(Long userId);
}
