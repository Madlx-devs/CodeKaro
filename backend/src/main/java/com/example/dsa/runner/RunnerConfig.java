package com.example.dsa.runner;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Selects the JavaRunner. Docker sandboxing is the only production path.
 * Local host execution is a dev convenience that requires BOTH
 * JAVA_RUNNER_MODE=local AND ALLOW_LOCAL_EXECUTION=true; otherwise the
 * application refuses to start rather than silently running untrusted
 * code on the host.
 */
@Configuration
public class RunnerConfig {

    @Bean
    public JavaRunner javaRunner() {
        String mode = System.getenv().getOrDefault("JAVA_RUNNER_MODE", "docker").trim();
        if ("local".equalsIgnoreCase(mode)) {
            boolean allowed = "true".equalsIgnoreCase(
                    System.getenv().getOrDefault("ALLOW_LOCAL_EXECUTION", "false").trim());
            if (!allowed) {
                throw new IllegalStateException(
                        "Refusing to start: JAVA_RUNNER_MODE=local requires ALLOW_LOCAL_EXECUTION=true. "
                        + "Running untrusted code on the application host is never the default; "
                        + "use the Docker sandbox runner instead.");
            }
            return new LocalJavaRunner();
        }
        return new DockerJavaRunner();
    }
}
