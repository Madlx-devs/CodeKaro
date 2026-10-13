# DSA Practice Platform — Backend

Java 17 + Spring Boot 3.4 REST API. See the repo-root `README.md` for full setup,
environment variables, API docs, and security notes.

## Run (dev)

```bash
mvn spring-boot:run
```

Dev profile: file-based H2 database at `./data/dsa` (Flyway migrations run automatically),
Docker-sandboxed code runner. Requires Docker running and the runner image:

```bash
docker pull eclipse-temurin:17-jdk
```

Run without Docker (dev machines only — both vars required):

```bash
JAVA_RUNNER_MODE=local ALLOW_LOCAL_EXECUTION=true mvn spring-boot:run
```

## Tests

```bash
mvn test
```
