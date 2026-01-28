# Agent Installation

The Datadog Agent collects metrics, traces, and logs from your infrastructure and applications.

## Docker Installation

**Basic Setup:**
```bash
docker run -d --name dd-agent \
  -e DD_API_KEY=<YOUR_API_KEY> \
  -e DD_SITE="datadoghq.com" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  gcr.io/datadoghq/agent:7
```

**With APM and Logs:**
```bash
docker run -d --name dd-agent \
  -e DD_API_KEY=<YOUR_API_KEY> \
  -e DD_SITE="datadoghq.com" \
  -e DD_APM_ENABLED=true \
  -e DD_APM_NON_LOCAL_TRAFFIC=true \
  -e DD_LOGS_ENABLED=true \
  -e DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
  -p 8126:8126/tcp \
  -p 8125:8125/udp \
  gcr.io/datadoghq/agent:7
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  datadog-agent:
    image: gcr.io/datadoghq/agent:7
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=datadoghq.com
      - DD_APM_ENABLED=true
      - DD_APM_NON_LOCAL_TRAFFIC=true
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
      - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    ports:
      - "8126:8126"  # APM traces
      - "8125:8125/udp"  # DogStatsD metrics
```

## Kubernetes Installation (Helm)

**Add Helm Repository:**
```bash
helm repo add datadog https://helm.datadoghq.com
helm repo update
```

**Basic Installation:**
```bash
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.site=datadoghq.com
```

**Full-Featured Installation:**
```bash
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.site=datadoghq.com \
  --set datadog.apm.portEnabled=true \
  --set datadog.logs.enabled=true \
  --set datadog.logs.containerCollectAll=true \
  --set datadog.processAgent.enabled=true \
  --set datadog.networkMonitoring.enabled=true \
  --set clusterAgent.enabled=true \
  --set clusterAgent.metricsProvider.enabled=true
```

**Using values.yaml:**
```yaml
# datadog-values.yaml
datadog:
  apiKey: <YOUR_API_KEY>
  site: datadoghq.com

  # APM
  apm:
    portEnabled: true
    socketEnabled: true

  # Logs
  logs:
    enabled: true
    containerCollectAll: true

  # Process monitoring
  processAgent:
    enabled: true
    processCollection: true

  # Network monitoring
  networkMonitoring:
    enabled: true

# Cluster Agent for Kubernetes metrics
clusterAgent:
  enabled: true
  metricsProvider:
    enabled: true

# Node Agent resources
agents:
  resources:
    requests:
      cpu: 200m
      memory: 256Mi
    limits:
      cpu: 200m
      memory: 256Mi
```

```bash
helm install datadog-agent datadog/datadog -f datadog-values.yaml
```

## Linux Package Installation

**Debian/Ubuntu:**
```bash
# Add Datadog repository
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"
```

**RHEL/CentOS/Amazon Linux:**
```bash
DD_API_KEY=<YOUR_API_KEY> DD_SITE="datadoghq.com" bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_script_agent7.sh)"
```

**Manual Installation (Debian):**
```bash
# Add repository
echo "deb [signed-by=/usr/share/keyrings/datadog-archive-keyring.gpg] https://apt.datadoghq.com/ stable 7" | sudo tee /etc/apt/sources.list.d/datadog.list

# Install
sudo apt-get update
sudo apt-get install datadog-agent

# Configure
sudo cp /etc/datadog-agent/datadog.yaml.example /etc/datadog-agent/datadog.yaml
sudo sed -i "s/api_key:.*/api_key: <YOUR_API_KEY>/" /etc/datadog-agent/datadog.yaml

# Start
sudo systemctl start datadog-agent
sudo systemctl enable datadog-agent
```

## Windows Installation

**PowerShell (Administrator):**
```powershell
$env:DD_API_KEY = "<YOUR_API_KEY>"
$env:DD_SITE = "datadoghq.com"

# Download and install
Start-Process -Wait msiexec -ArgumentList '/qn /i https://s3.amazonaws.com/ddagent-windows-stable/datadog-agent-7-latest.amd64.msi APIKEY="<YOUR_API_KEY>" SITE="datadoghq.com"'
```

## Cloud-Specific Installation

### AWS EKS

```bash
# Create secret for API key
kubectl create secret generic datadog-secret \
  --from-literal api-key=<YOUR_API_KEY>

# Install with EKS-specific settings
helm install datadog-agent datadog/datadog \
  --set datadog.apiKeyExistingSecret=datadog-secret \
  --set datadog.site=datadoghq.com \
  --set datadog.apm.portEnabled=true \
  --set datadog.logs.enabled=true \
  --set clusterAgent.enabled=true \
  --set clusterAgent.metricsProvider.enabled=true \
  --set clusterAgent.metricsProvider.useDatadogMetrics=true
```

### Google GKE

```bash
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.site=datadoghq.com \
  --set datadog.apm.portEnabled=true \
  --set datadog.logs.enabled=true \
  --set clusterAgent.enabled=true \
  --set providers.gke.autopilot=true  # For GKE Autopilot
```

### Azure AKS

```bash
helm install datadog-agent datadog/datadog \
  --set datadog.apiKey=<YOUR_API_KEY> \
  --set datadog.site=datadoghq.com \
  --set datadog.apm.portEnabled=true \
  --set datadog.logs.enabled=true \
  --set clusterAgent.enabled=true \
  --set agents.tolerations[0].operator=Exists
```

## Agent Configuration (datadog.yaml)

**Core Configuration:**
```yaml
# /etc/datadog-agent/datadog.yaml
api_key: <YOUR_API_KEY>
site: datadoghq.com

# Global tags applied to all telemetry
tags:
  - env:production
  - team:platform

# APM configuration
apm_config:
  enabled: true
  env: production
  # Sampling rules
  apm_dd_url: https://trace.agent.datadoghq.com

# Log collection
logs_enabled: true
logs_config:
  container_collect_all: true
  # Processing rules
  processing_rules:
    - type: exclude_at_match
      name: exclude_healthchecks
      pattern: '"path":"/health"'

# DogStatsD for custom metrics
dogstatsd_non_local_traffic: true
dogstatsd_port: 8125

# Process monitoring
process_config:
  enabled: true
  process_collection:
    enabled: true

# Network monitoring
network_config:
  enabled: true
```

## Verification

**Check Agent Status:**
```bash
# Linux
sudo datadog-agent status

# Docker
docker exec dd-agent agent status

# Kubernetes
kubectl exec -it <agent-pod> -- agent status
```

**Verify in Datadog UI:**
1. Infrastructure > Host Map: Agent should appear
2. Infrastructure > Containers: Container metrics visible
3. APM > Services: If APM enabled and instrumented

## Common Issues

**Agent not reporting:**
- Verify API key is correct
- Check network connectivity to `*.datadoghq.com`
- Review agent logs: `journalctl -u datadog-agent` or `docker logs dd-agent`

**Missing container metrics:**
- Ensure Docker socket is mounted
- Verify cgroup paths are mounted correctly

**APM traces not appearing:**
- Confirm port 8126 is accessible
- Check `DD_APM_ENABLED=true` is set
- Verify application is instrumented
