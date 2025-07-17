#!/bin/bash

# TikTub Studio Frontend Runner Script

echo "🎬 TikTub Studio - Frontend Launcher"
echo "===================================="

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "❌ Java tidak ditemukan. Silakan install Java 11 atau lebih tinggi."
    exit 1
fi

# Check Java version
JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}' | awk -F '.' '{print $1}')
if [ "$JAVA_VERSION" -lt 11 ]; then
    echo "❌ Java 11 atau lebih tinggi diperlukan. Versi yang terdeteksi: $JAVA_VERSION"
    exit 1
fi

echo "✅ Java version: $(java -version 2>&1 | head -n 1)"

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven tidak ditemukan. Silakan install Apache Maven."
    exit 1
fi

echo "✅ Maven version: $(mvn -version | head -n 1)"

# Navigate to frontend directory
cd java_frontend

# Check if backend is running
echo "🔍 Checking backend connection..."
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo "✅ Backend server is running"
else
    echo "⚠️  Backend server tidak berjalan di localhost:5000"
    echo "   Silakan jalankan backend terlebih dahulu dengan: python run_backend.py"
    read -p "   Lanjutkan tanpa backend? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Build and run the application
echo "🔨 Building application..."
if ! mvn clean compile; then
    echo "❌ Build gagal!"
    exit 1
fi

echo "🚀 Starting TikTub Studio Frontend..."
mvn exec:java -Dexec.mainClass="com.tiktubstudio.TikTubStudioApp" -Dexec.args="$*"

echo "👋 TikTub Studio Frontend stopped."