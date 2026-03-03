#!/bin/bash
# Command Tower Recovery Script
# Usage: ./scripts/recovery.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "  🚀 Command Tower Recovery Script"
echo "=============================================="
echo ""

cd "$PROJECT_DIR"

# Step 1: Check Docker
echo "[1/6] Checking Docker..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi
echo "✅ Docker is running"
echo ""

# Step 2: Stop all containers
echo "[2/6] Stopping all containers..."
docker-compose down 2>/dev/null || true
echo "✅ Containers stopped"
echo ""

# Step 3: Kill port 3003 process
echo "[3/6] Freeing port 3003..."
if lsof -i :3003 > /dev/null 2>&1; then
    echo "   Killing process on port 3003..."
    lsof -ti :3003 | xargs kill -9 2>/dev/null || true
    echo "✅ Port 3003 freed"
else
    echo "✅ Port 3003 is already free"
fi
echo ""

# Step 4: Clean up zombie containers
echo "[4/6] Cleaning up zombie containers..."
docker rm -f $(docker ps -a -q --filter "name=command-tower") 2>/dev/null || true
docker rm -f $(docker ps -a -q --filter "name=haven") 2>/dev/null || true
docker rm -f $(docker ps -a -q --filter "name=dojo") 2>/dev/null || true
echo "✅ Zombie containers removed"
echo ""

# Step 5: Start fresh
echo "[5/6] Starting all services..."
docker-compose up -d
echo "✅ Services starting..."
echo ""

# Step 6: Wait and verify
echo "[6/6] Waiting for services to be healthy..."
sleep 10

echo ""
echo "=============================================="
echo "  📊 Service Status"
echo "=============================================="
docker-compose ps

echo ""
echo "=============================================="
echo "  🔍 Redis Connectivity Test"
echo "=============================================="
if docker-compose exec -T command-tower-redis redis-cli PING 2>/dev/null | grep -q "PONG"; then
    echo "✅ Redis is responding"
else
    echo "⚠️  Redis not responding yet. May need more time to start."
fi

echo ""
echo "=============================================="
echo "  🌐 Quick Links"
echo "=============================================="
echo "  UI Dashboard:    http://localhost:5173"
echo "  Haven API:       http://localhost:3003"
echo "  Ranck AI:        http://localhost:3004"
echo "  Ads Manager:     http://localhost:3005"
echo "  Dojo Training:   http://localhost:3007"
echo "  Evolution API:   http://localhost:8080"
echo ""
echo "=============================================="
echo "  📝 Next Steps"
echo "=============================================="
echo "  1. Open http://localhost:5173 in your browser"
echo "  2. Check logs: docker-compose logs -f"
echo "  3. View errors: docker-compose logs haven-receptionist-api | grep -i error"
echo ""
echo "  If issues persist, see ERROR-DIAGNOSIS.md"
echo "=============================================="
