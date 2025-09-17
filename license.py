import os
import hashlib
import pandas as pd
import streamlit as st
import time

# File paths
insurance_data_file = "insurance_details.csv"
blockchain_file = "insurance_blockchain.txt"

# Function to generate blockchain hash
def generate_block_hash(name, age, contact_number, insurance_number, amount, claimed, previous_hash=""):
    block_data = f"{name}{age}{contact_number}{insurance_number}{amount}{claimed}{previous_hash}"
    return hashlib.sha256(block_data.encode('utf-8')).hexdigest()

# Function to append a new block to the blockchain
def append_to_blockchain(name, age, contact_number, insurance_number, amount, claimed, previous_hash=""):
    block_hash = generate_block_hash(name, age, contact_number, insurance_number, amount, claimed, previous_hash)
    timestamp = time.time()
    
    block = {
        "timestamp": timestamp,
        "name": name,
        "age": age,
        "contact_number": contact_number,
        "insurance_number": insurance_number,
        "amount": amount,
        "claimed": claimed,
        "block_hash": block_hash,
        "previous_hash": previous_hash,
    }
    
    with open(blockchain_file, "a") as f:
        f.write(str(block) + "\n")
    
    return block_hash  # Return the current block's hash

# Function to get the previous block's hash
def get_previous_hash():
    if os.path.exists(blockchain_file):
        with open(blockchain_file, "r") as f:
            lines = f.readlines()
            if lines:
                last_block = eval(lines[-1])  # Read the last block
                return last_block.get("block_hash", "")
    return ""

# Function to save insurance data
def save_insurance_data(data):
    # Save data to CSV
    if os.path.exists(insurance_data_file):
        existing_data = pd.read_csv(insurance_data_file)
        updated_data = pd.concat([existing_data, pd.DataFrame([data])], ignore_index=True)
    else:
        updated_data = pd.DataFrame([data])
    updated_data.to_csv(insurance_data_file, index=False)

# Streamlit App
st.title("Insurance Claim with Blockchain")

# Form to input insurance details
with st.form("insurance_form"):
    name = st.text_input("Name", "")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    contact_number = st.text_input("Contact Number", "")
    insurance_number = st.text_input("Insurance Number", "")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    claimed = st.selectbox("Claimed?", ["Yes", "No"])
    
    # Submit button
    submit = st.form_submit_button("Submit")

    if submit:
        # Validation
        if not name:
            st.error("Name cannot be empty.")
        elif len(contact_number) != 10 or not contact_number.isdigit():
            st.error("Please enter a valid 10-digit contact number.")
        elif not insurance_number:
            st.error("Insurance number cannot be empty.")
        else:
            # Save insurance data
            insurance_data = {
                "Name": name,
                "Age": age,
                "Contact Number": contact_number,
                "Insurance Number": insurance_number,
                "Amount": amount,
                "Claimed": claimed,
            }
            save_insurance_data(insurance_data)
            
            # Append to blockchain
            previous_hash = get_previous_hash()
            append_to_blockchain(name, age, contact_number, insurance_number, amount, claimed, previous_hash)
            
            st.success(f"Insurance details for {name} have been saved and added to the blockchain!")

# Display saved insurance details
if os.path.exists(insurance_data_file):
    st.subheader("Saved Insurance Details")
    insurance_df = pd.read_csv(insurance_data_file)
    st.dataframe(insurance_df)
else:
    st.warning("No insurance details found. Please add some entries.")

# Display blockchain
if os.path.exists(blockchain_file):
    st.subheader("Blockchain Ledger")
    with open(blockchain_file, "r") as f:
        blockchain_data = f.readlines()
        for block in blockchain_data:
            st.write(eval(block))
else:
    st.warning("No blockchain data found.")
