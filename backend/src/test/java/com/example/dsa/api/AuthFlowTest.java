package com.example.dsa.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.transaction.annotation.Transactional;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.http.MediaType.APPLICATION_JSON;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
class AuthFlowTest {
    @Autowired
    MockMvc mvc;

    private final ObjectMapper mapper = new ObjectMapper();

    private String authBody(String username, String password) {
        return "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}";
    }

    private String register(String username, String password) throws Exception {
        String body = mvc.perform(post("/api/auth/register")
                        .contentType(APPLICATION_JSON)
                        .content(authBody(username, password)))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").exists())
                .andReturn().getResponse().getContentAsString();
        JsonNode token = mapper.readTree(body).get("token");
        assertTrue(token != null && !token.asText().isBlank());
        return token.asText();
    }

    @Test
    void registerThenLoginThenAuthedRequest() throws Exception {
        String token = register("alice123", "password123");

        // duplicate username -> 409
        mvc.perform(post("/api/auth/register")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("alice123", "password123")))
                .andExpect(status().isConflict());

        // login with correct credentials -> 200 + token
        String loginBody = mvc.perform(post("/api/auth/login")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("alice123", "password123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.token").exists())
                .andReturn().getResponse().getContentAsString();
        assertFalse(mapper.readTree(loginBody).get("token").asText().isBlank());

        // login with wrong password -> 401
        mvc.perform(post("/api/auth/login")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("alice123", "wrongpassword")))
                .andExpect(status().isUnauthorized());

        // authed progress -> 200 with zeroed stats
        mvc.perform(get("/api/me/progress").header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.solved").value(0))
                .andExpect(jsonPath("$.attempted").value(0))
                .andExpect(jsonPath("$.streakDays").value(0));

        // anonymous progress -> 401
        mvc.perform(get("/api/me/progress")).andExpect(status().isUnauthorized());

        // invalid token -> treated as anonymous -> 401
        mvc.perform(get("/api/me/progress").header("Authorization", "Bearer deadbeef"))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void registerValidation() throws Exception {
        // username too short
        mvc.perform(post("/api/auth/register")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("ab", "password123")))
                .andExpect(status().isBadRequest());
        // password too short
        mvc.perform(post("/api/auth/register")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("bob123", "short")))
                .andExpect(status().isBadRequest());
        // bad username characters
        mvc.perform(post("/api/auth/register")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("bob smith!", "password123")))
                .andExpect(status().isBadRequest());
    }

    @Test
    void loginUnknownUserIsUnauthorized() throws Exception {
        mvc.perform(post("/api/auth/login")
                        .contentType(APPLICATION_JSON)
                        .content(authBody("nobody-here", "password123")))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void anonymousProblemListHasFalseStatusFlags() throws Exception {
        mvc.perform(get("/api/problems"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.problems").isArray());
        // status filter without auth -> 401
        mvc.perform(get("/api/problems").param("status", "solved"))
                .andExpect(status().isUnauthorized());
    }
}
