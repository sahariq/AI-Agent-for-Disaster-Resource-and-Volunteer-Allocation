from streamlit import st

def create_controls():
    st.sidebar.header("Control Panel")
    
    # User input for resource allocation
    total_resources = st.sidebar.number_input("Total Resources Available", min_value=0, value=100)
    st.sidebar.write("Total Resources:", total_resources)
    
    # User input for volunteer allocation
    total_volunteers = st.sidebar.number_input("Total Volunteers Available", min_value=0, value=50)
    st.sidebar.write("Total Volunteers:", total_volunteers)
    
    # User input for severity levels
    severity_level = st.sidebar.selectbox("Select Severity Level", options=["Low", "Medium", "High"])
    st.sidebar.write("Selected Severity Level:", severity_level)
    
    # Button to submit the inputs
    if st.sidebar.button("Allocate Resources"):
        st.sidebar.success("Resources allocated based on the inputs.")
    
    return total_resources, total_volunteers, severity_level