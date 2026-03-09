#!/bin/bash
# Setup script for Business MCP Server

set -e

echo "🚀 Setting up Business MCP Server..."

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3.10+ required"; exit 1; }

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Check for .env file
if [ ! -f "../../.env" ]; then
    echo "⚠️  Warning: .env file not found in project root"
    echo "📝 Please create .env file with required credentials:"
    echo ""
    echo "EMAIL_ADDRESS=your-email@gmail.com"
    echo "EMAIL_PASSWORD=your-app-password"
    echo "LINKEDIN_EMAIL=your-linkedin@email.com"
    echo "LINKEDIN_PASSWORD=your-linkedin-password"
    echo ""
else
    echo "✅ .env file found"
fi

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p ../../AI_Employee_Vault/Logs

# Test import
echo "🧪 Testing server import..."
python3 -c "from server import BusinessMCPServer; print('✅ Server import successful')"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure credentials in .env file"
echo "2. Add server to .claude/mcp-config.json"
echo "3. Test with: python3 server.py"
echo ""
