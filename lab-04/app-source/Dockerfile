# -----------------------------------------------------------------
# Stage 1: Build
# -----------------------------------------------------------------
FROM maven:3.9.9-eclipse-temurin-21 AS build

WORKDIR /app

COPY pom.xml .

RUN mvn dependency:go-offline -B

COPY src ./src

RUN mvn clean package -DskipTests && \
    mv target/*.jar target/app.jar

# -----------------------------------------------------------------
# Stage 2: Runtime
# -----------------------------------------------------------------
FROM eclipse-temurin:21-jre-alpine

# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -u 1001 -S appuser -G appuser

WORKDIR /app

COPY --from=build --chown=appuser:appuser /app/target/app.jar ./app.jar

USER appuser:appuser

EXPOSE 8080

CMD [ "java", "-jar", "app.jar"]
