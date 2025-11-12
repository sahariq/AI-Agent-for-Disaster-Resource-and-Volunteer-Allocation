import os
import sys
import pandas as pd
import streamlit as st

# Ensure repo root is on sys.path (so absolute imports work when Streamlit runs)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.append(REPO_ROOT)

# ✅ Use the correct package name (underscore, not hyphen)
from multi_agent_system.agents.supervisor.main import run_task


def main():
    st.title("Disaster Resource Allocation Dashboard")

    st.sidebar.header("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        # Save uploaded file temporarily
        tmp_path = os.path.join(REPO_ROOT, "temp_data.csv")
        with open(tmp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success("Data loaded successfully.")

        st.subheader("Data Preview")
        df = pd.read_csv(tmp_path)
        st.dataframe(df.head())

        st.sidebar.header("Parameters")
        available_volunteers = st.sidebar.number_input(
            "Available Volunteers", min_value=0, value=100
        )

        if st.button("Optimize Allocation"):
            # Call the supervisor API with sample params (adjust as needed)
            params = {
                "data_source": tmp_path,          # pass the saved file
                "output_format": "json",
                "available_volunteers": int(available_volunteers),
            }
            result = run_task("process_dataset_A", params)

            if result:
                st.subheader("Optimization Results")
                st.json(result)
            else:
                st.error("Optimization failed.")


    st.sidebar.header("About")
    st.sidebar.info(
        "This dashboard helps allocate resources and volunteers during disasters."
    )


if __name__ == "__main__":
    main()
