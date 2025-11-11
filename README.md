# AI-Agent-for-Disaster-Resource-and-Volunteer-Allocation

A Python + PuLP optimization agent with a Streamlit dashboard that allocates volunteers/resources across disaster zones based on severity and availability.

##Quick Start

```bash
# 0) (Recommended) Create/activate a virtual env
python -m venv .venv
# Windows PowerShell
. .venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# 1) Install deps
pip install -r requirements.txt  # if present
# or
pip install pandas pulp streamlit pydeck folium

# 2) (Optional) allow absolute imports from src/
# Windows PowerShell
$env:PYTHONPATH=(Get-Location).Path

# 3) Run the dashboard
streamlit run src/ui/dashboard.py
