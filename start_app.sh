#!bash
# Start Application Script
if [ ! -d "venv" ]; then
    py -3.14 -m venv venv
fi
source venv/Scripts/activate
pip install -r requirements.txt
python main.py
