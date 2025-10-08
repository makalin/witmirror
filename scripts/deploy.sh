#!/bin/bash

# WitMirror Pro Deployment Script
echo "🚀 Deploying WitMirror Pro..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
npm run build

# Check if build was successful
if [ ! -d "build" ]; then
    echo "❌ Frontend build failed"
    exit 1
fi

# Deploy to Vercel (frontend)
if command -v vercel &> /dev/null; then
    echo "🌐 Deploying frontend to Vercel..."
    vercel --prod
else
    echo "⚠️  Vercel CLI not found. Please install it: npm i -g vercel"
fi

# Deploy backend to Fly.io
if command -v fly &> /dev/null; then
    echo "☁️  Deploying backend to Fly.io..."
    cd api
    fly deploy
    cd ..
else
    echo "⚠️  Fly CLI not found. Please install it: https://fly.io/docs/hands-on/install-flyctl/"
fi

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your app should be available at:"
echo "  Frontend: https://witmirror.vercel.app"
echo "  Backend:  https://witmirror-pro.fly.dev"
echo "  API Docs: https://witmirror-pro.fly.dev/docs"
