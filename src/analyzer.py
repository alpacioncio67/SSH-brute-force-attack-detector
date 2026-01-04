import re
import pandas as pd
from datetime import datetime
import argparse
import os

# Argumentos CLI
#Una CLI permite que el archivo deje de ser un script de python y pase a ser una herramienta, para que no dependa de un archivo fijo y analicer cualquier log
parser = argparse.ArgumentParser(description="SSH Brute Force Log Analyzer")
parser.add_argument(
    "--logfile",
    required=True,
    help="Path to auth.log file"
)
#Parseamos los argumentos necesarios en la variable utilizada por el código
args = parser.parse_args()
log_file = args.logfile


# Leer logs
with open(log_file, "r") as file:
    logs = file.readlines()


# Filtrar intentos fallidos
failed_logs = [l for l in logs if "Failed password" in l]


# Extraer eventos (Buscamos IP,hora y usuario)
pattern = r"^(\w+ \d+ \d+:\d+:\d+).*Failed password for (\S+) from (\d+\.\d+\.\d+\.\d+)"
events = []

for line in failed_logs:
    match = re.search(pattern, line)
    if match:
        time_str, user, ip = match.groups()
        timestamp = datetime.strptime(time_str, "%b %d %H:%M:%S")
        events.append({
            "timestamp": timestamp,
            "ip": ip,
            "user": user
        })

# DataFrame principal
df = pd.DataFrame(events).sort_values("timestamp")

# Ventana temporal
window = "5min"
grouped = (
    df.set_index("timestamp")
      .groupby("ip")
      .rolling(window)
      .size()
      .reset_index(name="attempts")
)

# Severidad
def classify_severity(attempts):
    if attempts >= 20:
        return "HIGH"
    elif attempts >= 10:
        return "MEDIUM"
    else:
        return "LOW"

grouped["severity"] = grouped["attempts"].apply(classify_severity)

# Análisis por usuario
user_stats = (
    df.groupby("user")
      .size()
      .reset_index(name="failed_attempts")
      .sort_values("failed_attempts", ascending=False)
)

# IPs sospechosas
sospechosos = grouped[grouped["severity"].isin(["HIGH", "MEDIUM"])]

# Resumen SOC (Security Operations Center)
# Transformamos datos en inteligencia de seguridad 
print("\n=== Analysis Summary ===")
print(f"Total failed attempts: {len(df)}")
print(f"Unique attacking IPs: {df['ip'].nunique()}")
print(f"High severity alerts: {len(sospechosos[sospechosos['severity'] == 'HIGH'])}")

top_user = user_stats.iloc[0]
print(f"Most targeted user: {top_user['user']} ({top_user['failed_attempts']} attempts)")

# Guardar resultados
output_path = "results/sospechosos.csv"
os.makedirs("results", exist_ok=True)
sospechosos.to_csv(output_path, index=False)

print(f"\nResults saved to {output_path}")
