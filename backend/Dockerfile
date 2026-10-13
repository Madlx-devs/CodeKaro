# syntax=docker/dockerfile:1
# Build context is the REPO ROOT (see docker-compose.yml): docker build -f backend/Dockerfile .
FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /build
COPY backend/pom.xml backend/pom.xml
COPY backend/src backend/src
COPY questions questions
WORKDIR /build/backend
RUN mvn -q -DskipTests package

FROM eclipse-temurin:17-jre
# docker CLI so the app can launch sibling sandbox containers through the mounted socket
RUN apt-get update && apt-get install -y --no-install-recommends docker.io && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=build /build/backend/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
