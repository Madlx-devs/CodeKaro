package com.example.dsa.domain;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

public interface BookmarkRepository extends JpaRepository<Bookmark, BookmarkId> {
    boolean existsByUserIdAndProblemId(Long userId, String problemId);

    @Query("select b.problemId from Bookmark b where b.userId = :userId")
    List<String> problemIdsByUser(Long userId);
}
