import pandas as pd
import random
from datetime import datetime, timedelta

# Generate synthetic data
patients = [f'P{str(i).zfill(3)}' for i in range(1, 21)]
start_time = datetime(2025, 6, 1, 0, 0)

# List of common medications with dosages
medications = [
    "Aspirin 100mg",
    "Metformin 500mg",
    "Lisinopril 10mg",
    "Atorvastatin 20mg",
    "Levothyroxine 50mcg",
    "Amlodipine 5mg",
    "Ibuprofen 200mg",
    "Omeprazole 20mg",
    "None"  # Option for no medication
]

data = []

for patient in patients:
    for hour in range(24):
        timestamp = start_time + timedelta(hours=hour)

        heart_rate = random.randint(60, 120)
        bp_sys = random.randint(100, 140)
        bp_dia = random.randint(60, 90)
        oxygen = random.randint(92, 100)
        temp = round(random.uniform(97.0, 102.0), 1)
        med = random.choice(medications)

        # Basic logic for condition
        if heart_rate > 110 or oxygen < 94 or temp > 101.0:
            condition = 'Critical'
        elif heart_rate < 65 or temp < 97.5:
            condition = 'At Risk'
        else:
            condition = 'Normal'

        data.append([
            patient, timestamp, heart_rate, bp_sys, bp_dia,
            oxygen, temp, med, condition
        ])

# Create dataframe and save
df = pd.DataFrame(data, columns=[
    'Patient_ID', 'DateTime', 'Heart_Rate', 'BP_Systolic',
    'BP_Diastolic', 'Oxygen_Saturation', 'Temperature',
    'Medication', 'Condition'
])

# Save to synthetic_data directory
df.to_csv('synthetic_data/patient_vitals.csv', index=False)
print("✅ Synthetic data saved as 'synthetic_data/patient_vitals.csv'")