#!/bin/bash
# DSA Practice Platform — one-command VPS deploy (Ubuntu 22.04/24.04).
# Run as root or with sudo:  sudo bash deploy.sh
set -euo pipefail

if [ "$(id -u)" -ne 0 ]; then echo "Please run with sudo: sudo bash deploy.sh"; exit 1; fi
cd "$(dirname "$0")"

echo "==> 1/5 Installing Docker..."
if ! docker compose version >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq ca-certificates curl gnupg unzip openssl
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  chmod a+r /etc/apt/keyrings/docker.asc
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    | tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get update -qq
  # docker-ce replaces any docker.io from Ubuntu's repos
  apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
  systemctl enable --now docker
  docker compose version
else
  echo "    docker + compose already installed: $(docker compose version --short)"
fi

echo "==> 2/5 Configuring environment..."
if [ ! -f .env ]; then
  cp .env.example .env
  sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$(openssl rand -hex 16)/" .env
  echo "    generated random DB password in .env"
fi
# Optional: export OPENAI_API_KEY=sk-... before running to enable the AI tutor.

echo "==> 3/5 Pulling Java runner image..."
docker pull eclipse-temurin:17-jdk

echo "==> 4/5 Building and starting app + Postgres..."
docker compose up --build -d
echo "    waiting for the app to become healthy..."
for i in $(seq 1 40); do
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/api/problems 2>/dev/null | grep -q 200; then
    echo "    app is UP"
    break
  fi
  sleep 5
  if [ "$i" -eq 40 ]; then echo "    app did not start in time; check: docker compose logs app"; exit 1; fi
done
QCOUNT=$(curl -s http://localhost:8080/api/problems | grep -o '"id"' | wc -l)
echo "    questions served: $QCOUNT"

echo "==> 5/5 Installing Caddy reverse proxy (port 80 -> app)..."
# The VPS image ships with nginx holding port 80 (default welcome page).
# Stop and disable it so Caddy can bind :80; harmless if nginx is absent.
if command -v nginx >/dev/null 2>&1 || systemctl is-active --quiet nginx 2>/dev/null; then
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
  echo "    stopped+disabled nginx to free port 80 for Caddy"
fi
if ! command -v caddy >/dev/null 2>&1; then
  apt-get install -y -qq debian-keyring debian-archive-keyring apt-transport-https gnupg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
  curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list >/dev/null
  apt-get update -qq && apt-get install -y -qq caddy
fi
cp Caddyfile /etc/caddy/Caddyfile
systemctl enable --now caddy
systemctl reload caddy
if command -v ufw >/dev/null 2>&1 && ufw status | grep -q "Status: active"; then
  ufw allow 80,443/tcp >/dev/null && echo "    ufw: opened 80/443"
fi

echo ""
echo "================================================================"
echo " DEPLOYED. Open:  http://$(curl -s -m 5 ifconfig.me 2>/dev/null || echo '<your-vps-ip>')/"
echo "================================================================"
echo "Useful commands:"
echo "  docker compose logs -f app     # app logs"
echo "  docker compose ps              # container status"
echo "  docker compose down            # stop everything"
echo "AI tutor: add OPENAI_API_KEY=sk-... to .env, then: docker compose up -d"
echo "HTTPS: point a domain at this VPS, then set the domain in /etc/caddy/Caddyfile"
echo "       and run: systemctl reload caddy   (Caddy gets a free cert automatically)"
