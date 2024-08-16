#!/bin/bash

# Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
echo "Starting frontend"
npm run dev &
cd ../

# Start backend
echo "Starting backend"
python3 -m backend.main
