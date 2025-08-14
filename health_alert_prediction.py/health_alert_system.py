
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# ---------------- 1. Simulated Sensor Data ----------------
np.random.seed(42)

data = {
    "Reading_Index": list(range(1, 51)),
    "Heart_Rate": np.random.normal(75, 10, 50),    # bpm
    "Oxygen_Level": np.random.normal(98, 1, 50),   # %
    "Temperature": np.random.normal(37, 0.5, 50)   # °C
}

# Inject anomalies to simulate emergencies
data["Heart_Rate"][5] = 140
data["Oxygen_Level"][10] = 85
data["Temperature"][15] = 40

df = pd.DataFrame(data)

# ---------------- 2. Anomaly Detection ----------------
model = IsolationForest(contamination=0.1, random_state=42)
df["Anomaly"] = model.fit_predict(df)   # -1 = anomaly, 1 = normal
df["Status"] = df["Anomaly"].apply(lambda x: "Emergency" if x == -1 else "Normal")

# ---------------- 3. Generate Alerts ----------------
def generate_alerts(row):
    if row["Status"] == "Emergency":
        alert_msg = (f"EMERGENCY ALERT!\n"
                     f"Reading Index: {row['Reading_Index']}\n"
                     f"Heart Rate: {row['Heart_Rate']} bpm\n"
                     f"Oxygen Level: {row['Oxygen_Level']}%\n"
                     f"Temperature: {row['Temperature']}°C\n"
                     f"Sending notifications to: Family, Doctor, Hospital\n")
        return alert_msg
    else:
        return ""

df["Alert_Message"] = df.apply(generate_alerts, axis=1)

# ---------------- 4. Display Dashboard ----------------
dashboard_columns = ["Reading_Index", "Heart_Rate", "Oxygen_Level", "Temperature", "Status", "Alert_Message"]
dashboard = df[dashboard_columns]

print("=== Patient Health Dashboard ===")
print(dashboard.to_string(index=False))

# ---------------- 5. Visualization ----------------
plt.figure(figsize=(12,5))
plt.plot(df["Reading_Index"], df["Heart_Rate"], marker='o', label="Heart Rate")
plt.plot(df["Reading_Index"], df["Oxygen_Level"], marker='s', label="Oxygen Level")
plt.plot(df["Reading_Index"], df["Temperature"], marker='^', label="Temperature")

# Highlight anomalies
anomalies = df[df["Anomaly"] == -1]
plt.scatter(anomalies["Reading_Index"], anomalies["Heart_Rate"], color='red', s=100, label="Anomaly")
plt.xlabel("Reading Index")
plt.ylabel("Sensor Values")
plt.title("Patient Sensor Data with Detected Anomalies")
plt.legend()
plt.grid(True)
plt.show()

# ---------------- 6. Optional: Save Dashboard as CSV ----------------
dashboard.to_csv("Patient_Health_Dashboard_with_Alerts.csv", index=False)
print("\nDashboard with alerts saved as 'Patient_Health_Dashboard_with_Alerts.csv'.")