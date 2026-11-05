<div align="center">

# Auto-Healing Docker Application

<p>High-availability self-healing container architecture with automated Docker health checks, process crash recovery, and GitHub Actions CI/CD</p>

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" />
<img src="https://img.shields.io/badge/License-MIT-8b5cf6?style=flat-square" />
<img src="https://img.shields.io/github/last-commit/tejas-coder28/auto-healing-docker-app?style=flat-square&color=8b5cf6" />

</div>

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=🎓%20ABOUT&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

Production cloud environments frequently encounter service degradation, unhandled thread panics, and silent deadlock states where processes appear running but fail to serve client requests. While native container restart policies handle hard process crashes, they cannot identify or remediate silent application failures that cause services to become unresponsive. This project solves silent container failures by implementing a dual-layer self-healing architecture: native Docker restart policies recover from fatal process terminations, while a decoupled autoheal sidecar monitors HTTP health check endpoints and restarts degraded containers before outages impact end users.

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=✨%20FEATURES&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

- **Dual-Layer Auto-Recovery**: Combines Docker daemon restart policies (`restart: unless-stopped`) for hard crashes with an autoheal sidecar monitor for silent application failures.
- **Automated Health Probes**: Configures Docker engine `HEALTHCHECK` with calibrated intervals, timeouts, retries, and start periods querying `/health`.
- **Fault-Injection Test Harness**: Interactive REST control routes (`POST /crash` and `POST /break`) enabling instant simulation of fatal process exits and 503 service degradation.
- **Least-Privilege Security Hardening**: Non-root container runtime execution (`appuser`) adhering to Docker security best practices and minimal footprint `python:3.12-slim` base image.
- **Automated CI/CD Pipeline**: GitHub Actions automation testing Python logic with `pytest`, validating containerized build health via smoke tests, and publishing multi-tag images to Docker Hub.

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=⚡%20TECH%20STACK&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

| Layer | Technology |
|---|---|
| **Application Runtime** | Python 3.12, Flask 3.1 |
| **Containerization & Orchestration** | Docker Engine, Docker Compose v2 |
| **Supervision & Self-Healing** | Native Docker Healthcheck, Will Farrell Autoheal Sidecar |
| **Testing & Quality Assurance** | Pytest 8.3 |
| **CI/CD & Automation** | GitHub Actions (Ubuntu Runners, Docker Hub Integration) |
| **Container Registry** | Docker Hub (`tejas2345/auto-healing-app`) |

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=🏗️%20ARCHITECTURE&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

```mermaid
flowchart TD
    subgraph ClientLayer ["Client & Traffic Layer"]
        U["End User / Browser / Curl"] -->|Port 5000| W["Flask Web App (Container: auto-healing-app)"]
    end

    subgraph HealthSupervision ["Dual-Layer Self-Healing Supervision"]
        W -->|Self-Test: Every 10s| H["Docker HEALTHCHECK (/health)"]
        H -->|Status: Healthy 200| OK["Normal Operation"]
        H -->|Status: Unhealthy 503| AH["Autoheal Sidecar (willfarrell/autoheal)"]
        AH -->|Inspects Docker Socket| DK["/var/run/docker.sock"]
        DK -->|docker restart| W
        
        W -->|Fatal Crash: Process Exit| RP["Docker Daemon Restart Policy (unless-stopped)"]
        RP -->|Immediate Restart| W
    end

    subgraph DeliveryPipeline ["CI/CD Delivery Pipeline"]
        DEV["Developer (git push)"] --> GHA["GitHub Actions CI"]
        GHA -->|1. Unit Tests| PYT["pytest -v"]
        PYT -->|2. Container Build| DKB["docker build"]
        DKB -->|3. Smoke Test| SMK["curl --fail http://localhost:5000/health"]
        SMK -->|4. Push to Registry| DH["Docker Hub (tejas2345/auto-healing-app)"]
    end
```

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=🚀%20GETTING%20STARTED&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose v2](https://docs.docker.com/compose/) installed
- Python 3.12+ (optional, only for running local tests without Docker)
- Git installed on your system

### 1. Clone the Repository
```bash
git clone https://github.com/tejas-coder28/auto-healing-docker-app.git
cd auto-healing-docker-app
```

### 2. Environment Configuration
Copy the sample environment variables:
```bash
cp .env.example .env
```

### 3. Launch with Docker Compose
Start both the web application and the autoheal sidecar supervisor in detached mode:
```bash
docker compose up --build -d
```
Access the application dashboard at `http://localhost:5000`.

### 4. Verify Active Container Health
```bash
docker ps
```
The `auto-healing-app` container will show `(health: starting)` during initial startup, transitioning to `(healthy)` within 10 seconds.

### 5. Simulate Failure Scenarios & Verify Self-Healing

#### Scenario A: Process Crash Simulation (Immediate Exit)
```bash
# Trigger an abrupt process termination (os._exit)
curl -X POST http://localhost:5000/crash

# Check container status
docker ps
```
*Result: Docker's native `restart: unless-stopped` policy detects the non-zero exit code and reboots the container within seconds. The restart counter increments.*

#### Scenario B: Silent Failure Simulation (Unhealthy State)
```bash
# Trigger an internal application error (sets healthy=False)
curl -X POST http://localhost:5000/break

# Verify the health endpoint returns HTTP 503
curl http://localhost:5000/health

# Inspect autoheal monitoring logs
docker logs -f autoheal
```
*Result: Docker marks the container `(unhealthy)` after 3 failed health probes (~30 seconds). The `autoheal` sidecar detects the status and automatically issues a container reboot, restoring HTTP 200 health.*

### 6. Run Unit Tests (Without Docker)
```bash
# Create and activate virtual environment
python -m venv venv

# Windows (PowerShell / Command Prompt)
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies and execute test suite
pip install -r requirements-dev.txt
pytest -v
```

### 7. Teardown
```bash
docker compose down
```

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=📁%20PROJECT%20STRUCTURE&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

```
auto-healing-docker-app/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD test, build & Docker Hub push
├── app/
│   ├── templates/
│   │   └── index.html           # Web status dashboard and failure simulation UI
│   └── app.py                   # Flask server, health check endpoints & fault triggers
├── docs/
│   └── assets/                  # Proof-of-recovery logs and CI/CD verification screenshots
├── tests/
│   └── test_app.py              # Pytest unit tests for status codes & endpoints
├── .dockerignore                # Excluded build artifacts and virtual environments
├── .env.example                 # Environment variable template
├── .gitignore                   # Git exclusion rules
├── docker-compose.yml           # Multi-container orchestration (web + autoheal)
├── Dockerfile                   # Non-root multi-stage Python 3.12 slim container
├── LICENSE                      # MIT License
├── pytest.ini                   # Pytest test discovery settings
├── requirements.txt             # Production Flask runtime dependencies
├── requirements-dev.txt         # Development & testing packages (pytest)
└── README.md                    # Project documentation
```

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=📸%20SCREENSHOTS&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

### 1. Healthy Container Status
*Docker container running with active healthcheck reporting healthy status.*

![Healthy Container](/docs/assets/01-healthy.png)

### 2. Process Crash Recovery
*Process termination triggered via `/crash` route, instantly revived by Docker restart policy.*

![Crash Recovery](/docs/assets/02-crash-recovery.png)

### 3. Autoheal Sidecar Log Output
*Autoheal sidecar detecting consecutive 503 health check failures and rebooting container.*

![Autoheal Log](/docs/assets/03-autoheal-log.png)

### 4. GitHub Actions CI/CD Pipeline
*Automated pipeline successfully running pytest, container smoke testing, and Docker Hub image build.*

![CI/CD Pipeline](/docs/assets/04-actions-green.png)

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=🔮%20FUTURE%20IMPROVEMENTS&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

- **Prometheus & Grafana Telemetry**: Implement Prometheus metrics exporter to track request latencies, failure frequencies, and container restart counters in real time.
- **Webhook Alert Notifications**: Connect autoheal restart events to Discord or Slack webhooks for immediate incident alerting.
- **Kubernetes Liveness & Readiness Probes**: Port Docker Compose health checks into Kubernetes manifests using native liveness and readiness probe specifications.

---

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:0a1428,50:8b5cf6,100:0a1428&height=48&section=header&text=👤%20AUTHOR&fontSize=22&fontColor=ffffff&fontAlignY=50" width="100%" />

**Tejas Muralidhar**
- GitHub: [@tejas-coder28](https://github.com/tejas-coder28)
- LinkedIn: [Tejas Muralidhar](https://www.linkedin.com/in/tejasmuralidhar)
