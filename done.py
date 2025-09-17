import pandas as pd
import streamlit as st

# Function to get patient details by Name
def get_patient_details(name):
    patient_data = pd.read_csv("patient_details.csv")
    
    # Filter by Name, case insensitive
    patient = patient_data[patient_data["Name"].str.contains(name, case=False)]
    
    if not patient.empty:
        return patient
    return None

# Function to get insurance details by Patient Name
def get_insurance_details(name):
    insurance_data = pd.read_csv("insurance_details.csv")
    
    # Filter by Patient Name, case insensitive
    insurance = insurance_data[insurance_data["Name"].str.contains(name, case=False)]
    
    if not insurance.empty:
        return insurance
    return None

# Streamlit interface
st.title("Patient and Insurance Details Retrieval")

# Input option to fetch data by Patient Name
patient_name_to_retrieve = st.text_input("Enter Patient Name to retrieve details:")

# Retrieve patient details based on Name
if patient_name_to_retrieve:
    patient_details = get_patient_details(name=patient_name_to_retrieve)

    # If patient details are found, display them
    if patient_details is not None:
        st.subheader("Patient Details:")
        st.write(patient_details)

        # Retrieve the corresponding insurance details based on Name
        insurance_details = get_insurance_details(name=patient_name_to_retrieve)

        if insurance_details is not None:
            st.subheader("Insurance Details:")
            st.write(insurance_details)
        else:
            st.error("No insurance details found for this patient.")
    else:
        st.error("No patient found with the provided name.")
