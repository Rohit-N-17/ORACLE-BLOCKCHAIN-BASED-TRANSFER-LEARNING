from flask import Flask, request, jsonify
from hfc.fabric import Client


curl -X POST http://localhost:8501/\
-H "Content-Type: application/json" \
-d '{
      "chaincode": "blockchain.json",
      "function": "CreateAsset",
      "args": ["asset1", "blue", "5", "Tom", "300"]
    }'
curl -X POST http://localhost:8501/\
-H "Content-Type: application/json" \
-d '{
      "chaincode": "insurance_blockchain.json",
      "function": "ReadAsset",
      "args": ["asset1"]
    }'

app = Flask(__name__)

import pandas as pd
import streamlit as st
import ast  # To parse the blockchain data from text file

# Function to get patient details by Name
def get_patient_details(name):
    patient_data = pd.read_csv("patient_details.csv")
    # Filter by Name, case insensitive
    patient = patient_data[patient_data["Name"].str.contains(name, case=False)]
    if not patient.empty:
        return patient
    return None

# Function to get insurance details by Name
def get_insurance_details(name):
    insurance_data = pd.read_csv("insurance_details.csv")
    # Filter by Name, case insensitive
    insurance = insurance_data[insurance_data["Name"].str.contains(name, case=False)]
    if not insurance.empty:
        return insurance
    return None

# Function to retrieve patient blockchain hash key
def get_patient_blockchain_hash(name):
    with open("blockchain.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            record = ast.literal_eval(line.strip())
            if record.get("name").lower() == name.lower():
                return record.get("block_hash")
    return "No blockchain hash found for this patient."

# Function to retrieve insurance blockchain hash key
def get_insurance_blockchain_hash(name):
    with open("insurance_blockchain.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            record = ast.literal_eval(line.strip())
            if record.get("name").lower() == name.lower():
                return record.get("block_hash")
    return "No blockchain hash found for this insurance."

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

        # Fetch and display blockchain hash keys
        patient_hash = get_patient_blockchain_hash(name=patient_name_to_retrieve)
        insurance_hash = get_insurance_blockchain_hash(name=patient_name_to_retrieve)

        st.subheader("Blockchain Hashes:")
        st.write(f"Patient Blockchain Hash: {patient_hash}")
        st.write(f"Insurance Blockchain Hash: {insurance_hash}")
    else:
        st.error("No patient found with the provided name.")


# Initialize Hyperledger Fabric client
def init_fabric_client():
    c = Client(net_profile="connection-org1.json")  # Load the connection profile
    c.new_channel('mychannel')  # Set the channel name
    return c

fabric_client = init_fabric_client()

@app.route('/invoke', methods=['POST'])
def invoke_chaincode():
    data = request.json
    try:
        # Extract parameters from the request
        chaincode_name = data.get("chaincode")
        function_name = data.get("function")
        args = data.get("args")

        # Ensure all required fields are provided
        if not all([chaincode_name, function_name, args]):
            return jsonify({"error": "Missing parameters: chaincode, function, args"}), 400

        # Invoke the chaincode
        response = fabric_client.chaincode_invoke(
            requestor='Admin',
            channel_name='mychannel',
            peers=['peer0.org1.example.com'],
            args=args,
            cc_name=chaincode_name,
            fcn=function_name
        )
        return jsonify({"result": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def query_chaincode():
    data = request.json
    try:
        # Extract parameters from the request
        chaincode_name = data.get("chaincode")
        function_name = data.get("function")
        args = data.get("args")

        # Ensure all required fields are provided
        if not all([chaincode_name, function_name, args]):
            return jsonify({"error": "Missing parameters: chaincode, function, args"}), 400

        # Query the chaincode
        response = fabric_client.chaincode_query(
            requestor='Admin',
            channel_name='mychannel',
            peers=['peer0.org1.example.com'],
            args=args,
            cc_name=chaincode_name,
            fcn=function_name
        )
        return jsonify({"result": response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

