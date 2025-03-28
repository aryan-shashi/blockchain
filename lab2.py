import streamlit as st
import hashlib
import json

# Initialize an empty hospital ledger (dictionary)
if 'hospital_ledger' not in st.session_state:
    st.session_state.hospital_ledger = {}

# Function to generate a unique hash for each visit
def generate_hash(patient_name, treatment, cost, date_of_visit):
    data_string = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(data_string.encode()).hexdigest()

# Function to add or update patient visits
def add_patient_visit():
    st.subheader("Add Patient Visit")
    patient_name = st.text_input("Enter the patient's name:").strip().lower()
    treatment = st.text_input("Enter the treatment received:")
    cost = st.number_input("Enter the cost of the treatment ($):", min_value=0.0, format="%.2f")
    date_of_visit = st.date_input("Enter the date of visit:")
    
    if st.button("Add Visit") and patient_name and treatment and cost:
        visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)
        visit = {
            "treatment": treatment,
            "cost": cost,
            "date_of_visit": str(date_of_visit),
            "visit_hash": visit_hash
        }
        
        if patient_name not in st.session_state.hospital_ledger:
            st.session_state.hospital_ledger[patient_name] = []
        
        st.session_state.hospital_ledger[patient_name].append(visit)
        st.success(f"Visit added for {patient_name} on {date_of_visit}.")

# Function to search for a patient
def search_patient():
    st.subheader("Search Patient Records")
    search_name = st.text_input("Enter patient name to search:").strip().lower()
    
    if st.button("Search"):
        if search_name in st.session_state.hospital_ledger:
            st.write(f"### Visit records for {search_name}:")
            visits = st.session_state.hospital_ledger[search_name]
            for visit in visits:
                st.json(visit, expanded=False)
        else:
            st.warning(f"Patient {search_name} not found in the ledger.")

# Streamlit App
st.title("🏥 Hospital Ledger System")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Add Patient Visit", "Search Patient Records"])

if page == "Add Patient Visit":
    add_patient_visit()
elif page == "Search Patient Records":
    search_patient()
