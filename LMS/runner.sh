#!/bin/bash

# Create and activate the virtual environment and install backend dependencies
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
cd ..

# Install packages and run frontend
cd frontend
npm install
echo "Starting frontend"
npm run dev &
cd ../

# Start backend
cd backend 
echo "Starting backend"
python3 main.py
