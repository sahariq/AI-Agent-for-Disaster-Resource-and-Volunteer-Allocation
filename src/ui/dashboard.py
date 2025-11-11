import streamlit as st
import pandas as pd
from src.data.loader import load_data
from src.optimization.solver import allocate_resources

def main():
    st.title("Disaster Resource Allocation Dashboard")

    st.sidebar.header("Data Upload")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.write("Data Loaded Successfully")

        st.subheader("Data Preview")
        st.dataframe(data.head())

        st.sidebar.header("Parameters")
        available_volunteers = st.sidebar.number_input("Available Volunteers", min_value=0, value=100)

        if st.button("Optimize Allocation"):
            allocation_results, status, objective_value = allocate_resources(data, available_volunteers)
            st.subheader("Optimization Results")
            st.write(f"Status: {status}")
            st.write(f"Objective Value: {objective_value}")
            results_df = pd.DataFrame(list(allocation_results.items()), columns=['Zone', 'Allocated Volunteers'])
            st.dataframe(results_df)

    st.sidebar.header("About")
    st.sidebar.info("This dashboard helps in allocating resources and volunteers during disasters.")

if __name__ == "__main__":
    main()
