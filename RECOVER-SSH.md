# SSH is dead on the 1GB VPS — recovery path (no SSH needed)

Situation (2026-10-13 ~13:48 IST): after the Caddy/gnupg fix, the third `deploy.sh`
run got far enough to start the Docker **build**, and now SSH won't connect at all.
This is expected on a 1GB box: the Dockerfile compiles the Spring Boot app inside a
`maven:3.9-eclipse-temurin-17` image (`mvn -DskipTests package`), and Maven + javac
+ dependency downloads can blow past 1GB. With no swap configured, the kernel
thrashes / OOM-kills, and sshd is usually the first thing to go quiet — the
instance still shows **Running** in the console.

## Get back in without SSH (Oracle Cloud Console)

1. Oracle Cloud Console → Compute → Instances → open **instance-20260623-0359**.
2. Under **Resources** (or the instance details page), find **Console connection** →
   **Create console connection** if none exists → **Launch Cloud Shell connection**.
   This is a serial console: it works even when sshd is dead.
3. Log in as `ubuntu`, then `sudo -i`.

If even the console is unresponsive: instance **More actions → Reboot**, wait 2–3
minutes, then try SSH again before touching anything else.

## Once you're in

```bash
# confirm the diagnosis (OOM kills during the build)
dmesg | grep -i -m5 -i "oom\|out of memory" ; free -h

# 1. Add 2GB swap BEFORE running deploy.sh again — this is the actual fix.
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile \
  && sudo mkswap /swapfile && sudo swapon /swapfile \
  && echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 2. Re-run the same deploy (Docker install + Caddy steps are idempotent;
#    deploy.sh already stops nginx itself in step 5/5 — no manual nginx step needed)
cd <wherever-you-unzipped> && sudo bash deploy.sh
```

## What to expect on 1GB

- The Maven build is slow on 1GB + swap: **10–20 minutes is normal**. Do not kill
  it because it looks stuck — watch with `docker compose logs -f app` from a
  second console session instead.
- The step-4 health loop waits ~3.5 min (`40 × 5s`); Spring Boot + Flyway on a
  small box can take longer. If it exits "did not start in time", the app is
  probably still starting — check `docker compose logs app`, not a failure.
- Steady state fits fine in 1GB: Postgres ~100MB, app ~250MB (JVM defaults to
  ~25% of RAM), Caddy negligible, each code-run sandbox capped at 128MB.

## If the box dies again mid-build

Run the build in the console (not over SSH, so a dropped connection can't kill
it): the deploy is already `nohup`-safe once started, but prefer the console
session for step 4 on this box.
