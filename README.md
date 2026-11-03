
# Automated CI/CD Pipeline on AWS

## Overview

An automated CI/CD pipeline that tests, builds,
scans, publishes, and deploys a containerized
FastAPI application to AWS EC2.

## Architecture

Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +--> Automated Testing (Pytest)
   |
   +--> Docker Image Build
   |
   +--> Vulnerability Scanning (Trivy)
   |
   +--> GitHub Container Registry
   |
   v
AWS EC2 (Ubuntu)
   |
   v
Docker Compose Deployment
   |
   v
Live FastAPI Application

## Technology Stack

- Python / FastAPI
- Git and GitHub
- GitHub Actions
- Docker
- Docker Compose
- GitHub Container Registry
- Trivy
- AWS EC2
- Ubuntu Linux

## Features

- Automated testing on every push and pull request.
- Docker image creation.
- Container vulnerability scanning.
- Automated image publishing.
- SSH-based EC2 deployment.
- Container health checks.
- Automated application updates.

## API Endpoints

GET /
GET /health
GET /version
GET /docs

## Deployment

The main branch triggers the CI/CD workflow.
After successful testing and security scanning,
the image is published to GHCR and deployed
to the AWS EC2 instance.

## Future Improvements

- HTTPS using Nginx and Let's Encrypt.
- Infrastructure provisioning using Terraform.
- Monitoring using Prometheus and Grafana.
- Deployment rollback strategy.
- Automated dependency scanning.
