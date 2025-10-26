# GradStat Deployment Guide

This guide covers deploying GradStat to various cloud platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
- [Environment Variables](#environment-variables)
- [Monitoring & Scaling](#monitoring--scaling)

## Prerequisites

- Docker and Docker Compose
- kubectl (for Kubernetes)
- Cloud provider CLI (AWS CLI, gcloud, or az)
- Domain name (for production)
- SSL certificate (for HTTPS)

## Local Development

### Running with Docker Compose

```bash
# Clone the repository
git clone https://github.com/your-org/gradstat.git
cd gradstat

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:3001
# Worker: http://localhost:8001
```

### Running Services Individually

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Backend:**
```bash
cd backend
npm install
cp .env.example .env
# Edit .env with your configuration
npm start
```

**Worker:**
```bash
cd worker
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Docker Deployment

### Building Images

```bash
# Build all images
docker-compose build

# Build individual services
docker build -t gradstat-frontend:latest ./frontend
docker build -t gradstat-backend:latest ./backend
docker build -t gradstat-worker:latest ./worker
```

### Pushing to Docker Registry

```bash
# Tag images
docker tag gradstat-frontend:latest your-registry/gradstat-frontend:latest
docker tag gradstat-backend:latest your-registry/gradstat-backend:latest
docker tag gradstat-worker:latest your-registry/gradstat-worker:latest

# Push to registry
docker push your-registry/gradstat-frontend:latest
docker push your-registry/gradstat-backend:latest
docker push your-registry/gradstat-worker:latest
```

## Kubernetes Deployment

### Create Kubernetes Manifests

Create `k8s/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gradstat-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: gradstat-frontend
  template:
    metadata:
      labels:
        app: gradstat-frontend
    spec:
      containers:
      - name: frontend
        image: your-registry/gradstat-frontend:latest
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gradstat-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gradstat-backend
  template:
    metadata:
      labels:
        app: gradstat-backend
    spec:
      containers:
      - name: backend
        image: your-registry/gradstat-backend:latest
        ports:
        - containerPort: 3001
        env:
        - name: WORKER_URL
          value: "http://gradstat-worker:8001"
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: gradstat-worker
spec:
  replicas: 3
  selector:
    matchLabels:
      app: gradstat-worker
  template:
    metadata:
      labels:
        app: gradstat-worker
    spec:
      containers:
      - name: worker
        image: your-registry/gradstat-worker:latest
        ports:
        - containerPort: 8001
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

Create `k8s/service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: gradstat-frontend
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: gradstat-frontend
---
apiVersion: v1
kind: Service
metadata:
  name: gradstat-backend
spec:
  type: ClusterIP
  ports:
  - port: 3001
    targetPort: 3001
  selector:
    app: gradstat-backend
---
apiVersion: v1
kind: Service
metadata:
  name: gradstat-worker
spec:
  type: ClusterIP
  ports:
  - port: 8001
    targetPort: 8001
  selector:
    app: gradstat-worker
```

### Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/gradstat-backend
```

## Cloud Platform Deployment

### AWS (ECS/EKS)

**Using ECS:**

1. Create ECR repositories:
```bash
aws ecr create-repository --repository-name gradstat-frontend
aws ecr create-repository --repository-name gradstat-backend
aws ecr create-repository --repository-name gradstat-worker
```

2. Push images to ECR
3. Create ECS task definitions
4. Create ECS services
5. Configure Application Load Balancer

**Using EKS:**

```bash
# Create EKS cluster
eksctl create cluster --name gradstat-cluster --region us-east-1

# Deploy using kubectl
kubectl apply -f k8s/
```

### Google Cloud Platform (Cloud Run / GKE)

**Using Cloud Run:**

```bash
# Build and push images
gcloud builds submit --tag gcr.io/PROJECT_ID/gradstat-frontend ./frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/gradstat-backend ./backend
gcloud builds submit --tag gcr.io/PROJECT_ID/gradstat-worker ./worker

# Deploy services
gcloud run deploy gradstat-frontend --image gcr.io/PROJECT_ID/gradstat-frontend --platform managed
gcloud run deploy gradstat-backend --image gcr.io/PROJECT_ID/gradstat-backend --platform managed
gcloud run deploy gradstat-worker --image gcr.io/PROJECT_ID/gradstat-worker --platform managed
```

**Using GKE:**

```bash
# Create cluster
gcloud container clusters create gradstat-cluster --num-nodes=3

# Deploy
kubectl apply -f k8s/
```

### Azure (Container Instances / AKS)

**Using Container Instances:**

```bash
# Create resource group
az group create --name gradstat-rg --location eastus

# Create container instances
az container create --resource-group gradstat-rg --name gradstat-frontend \
  --image your-registry/gradstat-frontend:latest --ports 3000
```

**Using AKS:**

```bash
# Create AKS cluster
az aks create --resource-group gradstat-rg --name gradstat-cluster --node-count 3

# Get credentials
az aks get-credentials --resource-group gradstat-rg --name gradstat-cluster

# Deploy
kubectl apply -f k8s/
```

## Environment Variables

### Frontend
- `NODE_ENV`: production
- `REACT_APP_API_URL`: Backend API URL

### Backend
- `NODE_ENV`: production
- `PORT`: 3001
- `WORKER_URL`: Worker service URL
- `ALLOWED_ORIGINS`: Frontend URL
- `JWT_SECRET`: Secret for JWT tokens
- `MAX_FILE_SIZE`: Maximum upload size (bytes)
- `RATE_LIMIT_WINDOW_MS`: Rate limit window
- `RATE_LIMIT_MAX_REQUESTS`: Max requests per window

### Worker
- `WORKER_PORT`: 8001
- `LOG_LEVEL`: info
- `MAX_WORKERS`: Number of concurrent workers

## Monitoring & Scaling

### Health Checks

All services expose `/health` endpoints:
- Frontend: `http://frontend:3000/health`
- Backend: `http://backend:3001/health`
- Worker: `http://worker:8001/health`

### Horizontal Pod Autoscaling (Kubernetes)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: gradstat-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: gradstat-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Logging

Use centralized logging solutions:
- **AWS**: CloudWatch Logs
- **GCP**: Cloud Logging
- **Azure**: Azure Monitor
- **Self-hosted**: ELK Stack or Grafana Loki

### Metrics

Monitor key metrics:
- Request rate and latency
- Error rates
- CPU and memory usage
- Job queue length
- Analysis completion time

### Recommended Tools

- **Prometheus + Grafana**: Metrics and dashboards
- **Sentry**: Error tracking
- **DataDog**: Full observability platform
- **New Relic**: Application performance monitoring

## Security Considerations

1. **HTTPS**: Always use SSL/TLS in production
2. **Authentication**: Implement JWT-based auth
3. **File Scanning**: Add virus scanning for uploads
4. **Rate Limiting**: Prevent abuse
5. **CORS**: Configure allowed origins
6. **Secrets Management**: Use vault services (AWS Secrets Manager, etc.)
7. **Network Policies**: Restrict inter-service communication
8. **Regular Updates**: Keep dependencies updated

## Backup & Disaster Recovery

1. **Database Backups**: If using persistent storage
2. **Configuration Backups**: Store in version control
3. **Disaster Recovery Plan**: Document recovery procedures
4. **Multi-region Deployment**: For high availability

## Cost Optimization

1. **Auto-scaling**: Scale down during low usage
2. **Spot Instances**: Use for worker nodes
3. **Resource Limits**: Set appropriate CPU/memory limits
4. **Caching**: Implement Redis for job status
5. **CDN**: Use for static assets

## Support

For deployment issues, please:
1. Check logs: `kubectl logs <pod-name>`
2. Verify environment variables
3. Test health endpoints
4. Review resource limits
5. Open an issue on GitHub

## License

MIT License - see LICENSE file
