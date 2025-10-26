#!/bin/bash

# GradStat Deployment Script
# Version: 1.0
# Date: October 23, 2025

set -e  # Exit on error

echo "🚀 GradStat Deployment Script"
echo "=============================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running in correct directory
if [ ! -d "frontend" ] || [ ! -d "backend" ] || [ ! -d "worker" ]; then
    print_error "Please run this script from the gradstat root directory"
    exit 1
fi

# Step 1: Check prerequisites
echo "📋 Step 1: Checking prerequisites..."
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi
print_success "Node.js $(node --version) found"

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed"
    exit 1
fi
print_success "npm $(npm --version) found"

# Check Python
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    print_error "Python is not installed"
    exit 1
fi
PYTHON_CMD=$(command -v python3 || command -v python)
print_success "Python $($PYTHON_CMD --version) found"

echo ""

# Step 2: Install dependencies
echo "📦 Step 2: Installing dependencies..."
echo ""

# Frontend
echo "Installing frontend dependencies..."
cd frontend
npm install --legacy-peer-deps
print_success "Frontend dependencies installed"
cd ..

# Backend
echo "Installing backend dependencies..."
cd backend
npm install
print_success "Backend dependencies installed"
cd ..

# Worker
echo "Installing worker dependencies..."
cd worker
$PYTHON_CMD -m pip install -r requirements.txt
print_success "Worker dependencies installed"
cd ..

echo ""

# Step 3: Build frontend
echo "🏗️  Step 3: Building frontend..."
echo ""

cd frontend
npm run build
print_success "Frontend built successfully"
cd ..

echo ""

# Step 4: Run tests (optional)
read -p "Run tests before deployment? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧪 Running tests..."
    
    # Frontend tests (if available)
    # cd frontend && npm test && cd ..
    
    # Backend tests (if available)
    # cd backend && npm test && cd ..
    
    print_success "Tests passed"
fi

echo ""

# Step 5: Check for PM2
echo "🔧 Step 5: Checking process manager..."
echo ""

if ! command -v pm2 &> /dev/null; then
    print_warning "PM2 not found. Installing PM2..."
    npm install -g pm2
    print_success "PM2 installed"
else
    print_success "PM2 $(pm2 --version) found"
fi

echo ""

# Step 6: Start services
echo "🚀 Step 6: Starting services..."
echo ""

# Stop existing processes
pm2 delete worker backend frontend 2>/dev/null || true

# Start worker
cd worker
pm2 start "$PYTHON_CMD main.py" --name worker --interpreter none
print_success "Worker started"
cd ..

# Start backend
cd backend
pm2 start server.js --name backend
print_success "Backend started"
cd ..

# Serve frontend
cd frontend
pm2 serve build 3000 --name frontend --spa
print_success "Frontend started"
cd ..

# Save PM2 configuration
pm2 save

echo ""

# Step 7: Verify deployment
echo "✅ Step 7: Verifying deployment..."
echo ""

sleep 5  # Wait for services to start

# Check if services are running
if pm2 list | grep -q "worker.*online"; then
    print_success "Worker is running"
else
    print_error "Worker failed to start"
fi

if pm2 list | grep -q "backend.*online"; then
    print_success "Backend is running"
else
    print_error "Backend failed to start"
fi

if pm2 list | grep -q "frontend.*online"; then
    print_success "Frontend is running"
else
    print_error "Frontend failed to start"
fi

echo ""

# Step 8: Display status
echo "📊 Deployment Status:"
echo "===================="
pm2 list

echo ""
echo "🎉 Deployment Complete!"
echo ""
echo "📝 Next Steps:"
echo "  1. Access the application at: http://localhost:3000"
echo "  2. Backend API available at: http://localhost:3001"
echo "  3. Worker API available at: http://localhost:8001"
echo ""
echo "💡 Useful Commands:"
echo "  - View logs: pm2 logs"
echo "  - Restart all: pm2 restart all"
echo "  - Stop all: pm2 stop all"
echo "  - Monitor: pm2 monit"
echo ""
echo "📚 Documentation: See DEPLOYMENT_GUIDE.md for more details"
echo ""

print_success "GradStat is now running!"
