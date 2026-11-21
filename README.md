# DevSecOps Pipeline

GitHub Actions pipeline that blocks vulnerable code and containers from being published.

## Gates

| Job | Tool | Fails the build when |
|---|---|---|
| secrets-scan | Gitleaks | Any secret exists in the git history |
| dependency-scan | Trivy (fs) | A fixable CRITICAL vulnerability exists in dependencies |
| sast | SonarQube | The quality gate fails |
| image-scan | Trivy (config, image) | HIGH misconfiguration in the Dockerfile, or a fixable CRITICAL CVE in the image |
| publish | Docker, GHCR | Never runs unless all four jobs above pass |

## Setup

1. Start SonarQube: `SONAR_DB_PASSWORD=<choose one> docker compose -f docker-compose.sonarqube.yml up -d`
2. In SonarQube create a project with key `devsecops-pipeline` and generate a token.
3. In GitHub, add repository secrets `SONAR_TOKEN` and `SONAR_HOST_URL`.
4. In GitHub, enable branch protection on `main` and require all four jobs to pass.

## Prove each gate works

| Gate | Test |
|---|---|
| Gitleaks | Commit a line containing an AWS key pattern such as `AKIA` followed by 16 uppercase characters |
| Trivy dependencies | Pin an old vulnerable version in `app/requirements.txt` |
| SonarQube | Add an obvious vulnerability such as `eval(user_input)` |
| Trivy image | Change the base image to an old tag such as `python:3.8` |
| Dockerfile policy | Remove the `USER` line |
