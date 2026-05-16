#!/bin/bash

# ORVION Setup Script
# Automated setup for development and production

set -e

echo "🚀 ORVION Setup Script"
echo "====================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please edit .env with your configuration${NC}"
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"

# Install Python dependencies
echo -e "\n${YELLOW}📦 Installing Python dependencies...${NC}"
pip install -r requirements.txt

# Install Node dependencies
echo -e "\n${YELLOW}📦 Installing Node dependencies...${NC}"
npm install

# Create logs directory
echo -e "\n${YELLOW}📁 Creating logs directory...${NC}"
mkdir -p logs

# Initialize database
echo -e "\n${YELLOW}🗄️  Initializing database...${NC}"
python scripts/init_db.py

# Compile smart contract
echo -e "\n${YELLOW}🔨 Compiling smart contract...${NC}"
npx hardhat compile

echo -e "\n${GREEN}✅ Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Deploy smart contract: npm run deploy:arc"
echo "2. Start backend: python main.py"
echo "3. Start frontend: cd frontend && npm start"
echo ""
