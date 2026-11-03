
# Automated CI/CD Pipeline on AWS

## Overview

An automated CI/CD pipeline that tests, builds,
scans, publishes, and deploys a containerized
FastAPI application to AWS EC2.

## Architecture

Developer

↓ Git Push / Pull Request

GitHub Repository

↓ Trigger CI/CD workflow

GitHub Actions – Continuous Integration
1. Checkout source code
2. Setup Python and install dependencies
3. Run automated tests using Pytest
4. Build Docker image
5. Scan image for vulnerabilities using Trivy
↓ Successful validation

GitHub Container Registry (GHCR)
6. Authenticate with GHCR
7. Push Docker image to registry
↓

GitHub Actions – Continuous Deployment
8. Establish SSH connection to AWS EC2
9. Verify SSH host fingerprint
10. Transfer Docker Compose configuration
11. Authenticate with GHCR
12. Pull Docker image
13. Deploy using Docker Compose
↓

AWS Cloud Infrastructure
14. Ubuntu EC2 instance
15. Docker container
16. FastAPI application
17. Health check endpoint (/health)
↓
Application successfully deployed

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

## Troubleshooting & Issues Resolved

During the implementation of this CI/CD pipeline, several deployment and configuration issues were encountered. The following section documents the problems, their root causes, and the solutions implemented.

### 1. SSH Connection Timeout

**Error:**
```text
dial tcp <EC2_PUBLIC_IP>:22: i/o timeout
```

**Root Cause:**

GitHub-hosted runners were initially unable to establish an SSH connection with the AWS EC2 instance on port 22.

**Investigation:**
- Verified that the EC2 instance was running.
- Confirmed that the `EC2_HOST` GitHub Actions secret contained the correct public IPv4 address.
- Checked the EC2 Security Group inbound rules and confirmed SSH access on TCP port 22.
- Verified outbound Security Group rules and the subnet's Internet Gateway route.
- Checked the Ubuntu firewall using `sudo ufw status`; UFW was inactive.

**Resolution:**

Verified the EC2 network configuration and SSH accessibility. The initial timeout was subsequently replaced by an SSH host-key fingerprint verification error, indicating that the connection had progressed to the SSH handshake stage.

### 2. SSH Host-Key Fingerprint Mismatch

**Error:**
```text
ssh: handshake failed: ssh: host key fingerprint mismatch
```

**Root Cause:**

The `EC2_HOST_FINGERPRINT` GitHub Actions secret contained a fingerprint that did not match the host key presented during the SSH handshake.

The initial fingerprint was obtained from the ED25519 host key, but the SSH connection was presenting a different host-key algorithm.

**Investigation:**

Inspected the available SSH host-key fingerprints directly on the Ubuntu EC2 instance.

ED25519 fingerprint:
```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256
```

ECDSA fingerprint:
```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ecdsa_key.pub -E sha256
```

**Resolution:**

Identified the ECDSA fingerprint as the matching fingerprint for the SSH connection and updated the `EC2_HOST_FINGERPRINT` secret in:

`GitHub Repository → Settings → Secrets and variables → Actions`

The workflow was configured to use the secret for SSH and SCP connections:

```yaml
fingerprint: ${{ secrets.EC2_HOST_FINGERPRINT }}
```

After updating the secret, SSH host verification succeeded and the deployment workflow proceeded.

### 3. GitHub Actions Workflow Configuration

**Issues encountered:**
- YAML syntax and indentation errors.
- An unavailable Trivy action version.
- Deprecation warnings associated with older GitHub Actions runtime versions.
- Ubuntu runner image migration warnings.

**Resolution:**
- Corrected YAML syntax and indentation.
- Updated the Trivy action reference to `aquasecurity/trivy-action@v0.36.0`.
- Updated checkout and Python setup actions to newer versions.
- Pinned the runner to `ubuntu-24.04` to avoid unexpected runner image changes.

### Key Lessons Learned

This troubleshooting process provided practical experience with:

- Debugging SSH connectivity between GitHub-hosted runners and AWS EC2.
- Understanding Security Groups, Network ACLs, Internet Gateways, and Linux firewalls.
- SSH host-key verification and fingerprint-based server authentication.
- Managing GitHub Actions secrets securely.
- Troubleshooting YAML-based CI/CD workflows.
- Diagnosing failures across multiple stages of an automated deployment pipeline.

**Outcome:** Resolved the SSH connectivity and host-key verification issues, allowing the GitHub Actions deployment workflow to establish a verified SSH connection to the AWS EC2 instance.
