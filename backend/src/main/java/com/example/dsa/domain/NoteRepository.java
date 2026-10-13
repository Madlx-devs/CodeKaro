package com.example.dsa.domain;

import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface NoteRepository extends JpaRepository<Note, Long> {
    Optional<Note> findByUserIdAndProblemId(Long userId, String problemId);
}
