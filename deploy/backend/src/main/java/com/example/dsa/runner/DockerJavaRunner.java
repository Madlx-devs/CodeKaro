package com.example.dsa.runner;

import java.io.IOException;
import java.nio.file.Path;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/**
 * Production runner: every compile and every test executes in a fresh, hardened
 * Docker container. Untrusted code never runs on the application host.
 *
 * Docker-out-of-Docker volume sharing: the app container reaches the HOST's
 * Docker daemon through /var/run/docker.sock, so a bind mount of a
 * container-local path would be resolved against the HOST's filesystem (where
 * it does not exist), leaving the sandbox with an empty /workspace. Instead,
 * per-run work dirs live on a shared NAMED volume (see docker-compose.yml),
 * which the daemon resolves by name; the whole volume is mounted at
 * /workspace and each run works in its own subdirectory.
 *
 * Hardening flags: --network none, 128 MB memory, 0.5 CPUs, 64 pids, read-only
 * root filesystem, no-new-privileges, cap-drop ALL, non-writable tmpdir redirect.
 */
public class DockerJavaRunner implements JavaRunner {
    private final String image;

    public DockerJavaRunner() {
        this(System.getenv().getOrDefault("JAVA_RUNNER_IMAGE", "eclipse-temurin:17-jdk"));
    }

    public DockerJavaRunner(String image) {
        this.image = image;
    }

    private record Sandbox(String dir, String tmpDir) {
    }

    /** Resolve the per-run sandbox dirs inside the shared named volume. */
    private static Sandbox sandbox(Path workDir) {
        Path workBase = Path.of(System.getenv().getOrDefault("DSA_WORK_DIR", "/opt/dsa-work"))
                .toAbsolutePath().normalize();
        String rel = workBase.relativize(workDir.toAbsolutePath().normalize())
                .toString().replace('\\', '/');
        String dir = "/workspace/" + rel;
        return new Sandbox(dir, dir + "/tmp");
    }

    private static String workVolume() {
        return System.getenv().getOrDefault("DSA_WORK_VOLUME", "dsa-work");
    }

    private List<String> dockerBase(Path dir) {
        Sandbox sb = sandbox(dir);
        return new ArrayList<>(List.of(
                "docker", "run", "--rm",
                "--network", "none",
                "--memory", "128m",
                "--cpus", "0.5",
                "--pids-limit", "64",
                "--security-opt", "no-new-privileges",
                "--read-only",
                "--cap-drop", "ALL",
                "-e", "JAVA_TOOL_OPTIONS=-Djava.io.tmpdir=" + sb.tmpDir(),
                "--mount", "type=volume,src=" + workVolume() + ",dst=/workspace",
                "-w", sb.dir(),
                image));
    }

    @Override
    public CompileResult compile(Path workDir, List<String> sources, Duration timeout) throws IOException {
        List<String> cmd = dockerBase(workDir);
        cmd.addAll(List.of("sh", "-lc", "javac -encoding UTF-8 " + String.join(" ", sources)));
        ProcessExec.ExecResult r = ProcessExec.exec(cmd, "", timeout);
        return new CompileResult(!r.timedOut() && r.exitCode() == 0, r.output(), r.timedOut());
    }

    @Override
    public RunResult run(Path workDir, String mainClass, String stdin, Duration timeout) throws IOException {
        Sandbox sb = sandbox(workDir);
        List<String> cmd = dockerBase(workDir);
        cmd.addAll(List.of("sh", "-lc",
                "java -Xms16m -Xmx64m -XX:MaxMetaspaceSize=64m -Djava.io.tmpdir=" + sb.tmpDir() + " " + mainClass));
        long start = System.nanoTime();
        ProcessExec.ExecResult r = ProcessExec.exec(cmd, stdin, timeout);
        long timeMs = (System.nanoTime() - start) / 1_000_000;
        return new RunResult(r.exitCode(), r.output(), timeMs, r.timedOut());
    }
}
