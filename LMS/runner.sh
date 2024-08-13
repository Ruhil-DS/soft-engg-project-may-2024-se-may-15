cd frontend
npm install
echo "Starting frontend"
npm run dev &
cd ../backend
pip install -r requirements.txt
cd ../
echo "Starting backend"
python3 -m backend.main