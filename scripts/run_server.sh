#!/bin/bash

# Navigate to the src directory
cd src/ui

# Run the Streamlit server
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0