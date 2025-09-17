// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientContract {
    // Struct to hold patient details
    struct Patient {
        uint256 id;
        string name;
        uint256 age;
        string gender;
        string contact;
        string symptoms;
        string hash; // Stores the blockchain hash
    }

    // Mapping to store patients by ID
    mapping(uint256 => Patient) private patients;
    uint256 private patientCount;

    // Event to log new patients
    event PatientAdded(uint256 id, string name, string hash);

    // Function to add or update patient details
    function addOrUpdatePatient(
        uint256 id,
        string memory name,
        uint256 age,
        string memory gender,
        string memory contact,
        string memory symptoms
    ) public returns (string memory) {
        string memory hash = generateHash(id, name, age, gender, contact, symptoms);

        if (patients[id].id == id) {
            // Update existing patient
            patients[id] = Patient(id, name, age, gender, contact, symptoms, hash);
        } else {
            // Add new patient
            patientCount++;
            patients[id] = Patient(id, name, age, gender, contact, symptoms, hash);
            emit PatientAdded(id, name, hash);
        }

        return hash;
    }

    // Function to retrieve patient details
    function getPatient(uint256 id) public view returns (
        uint256,
        string memory,
        uint256,
        string memory,
        string memory,
        string memory,
        string memory
    ) {
        require(patients[id].id == id, "Patient not found.");
        Patient memory patient = patients[id];
        return (patient.id, patient.name, patient.age, patient.gender, patient.contact, patient.symptoms, patient.hash);
    }

    // Helper function to generate a unique hash
    function generateHash(
        uint256 id,
        string memory name,
        uint256 age,
        string memory gender,
        string memory contact,
        string memory symptoms
    ) private pure returns (string memory) {
        return string(
            abi.encodePacked(keccak256(abi.encodePacked(id, name, age, gender, contact, symptoms)))
        );
    }

    // Function to get the total number of patients
    function getPatientCount() public view returns (uint256) {
        return patientCount;
    }
}
