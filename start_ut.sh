#!bash
# Start UT Script
if [ ! -d "venv" ]; then
    py -3.14 -m venv venv
fi
source venv/Scripts/activate
pip install -r requirements.txt
pip install -r tests/requirements-dev.txt
python -m pytest tests
