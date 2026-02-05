import re
import pandas as pd
from datetime import datetime
import argparse
import os

# CLI
parser = argparse.ArgumentParser(description="SSH Brute Force Log Analyzer")
parser.add_argument("--logfile", required=True, help="Path to auth.log file")
args = parser.parse_args()
log_file = args.logfile

# Leer logs
with open(log_file, "r") as f:
    logs = f.readlines()

# Filtrar intentos fallidos
failed_logs = [l.rstrip("\n") for l in logs if "Failed password" in l]
print(f"Failed logs encontrados: {len(failed_logs)}")

if failed_logs:
    print(f"Ejemplo línea: {repr(failed_logs[0])}")

# Regex: 3 grupos -> timestamp completo, user, ip
pattern = re.compile(
    r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}) .*Failed password for (?:invalid user )?(\S+) from (\d+\.\d+\.\d+\.\d+)'
)

events = []
for line in failed_logs:
    m = pattern.search(line)
    if not m:
        continue
    time_str, user, ip = m.groups()

    # Parseamos la fecha (sin año, asumimos año actual)
    try:
        timestamp = datetime.strptime(time_str, "%b %d %H:%M:%S")
    except ValueError:
        # Por si hay formatos raros, saltamos la línea
        continue

    events.append({
        "timestamp": timestamp,
        "ip": ip,
        "user": user
    })

print(f"Eventos extraídos: {len(events)}")

if not events:
    print("❌ No se ha podido hacer match con el regex. Revisa el patrón o el formato del log.")
    exit(1)

# DataFrame principal
df = pd.DataFrame(events).sort_values("timestamp")
df["timestamp"] = pd.to_datetime(df["timestamp"])

print("Primeras filas del DataFrame:")
print(df.head())

# Ventana de 5 minutos usando resample (más estable que rolling en tu versión)
# Contamos intentos por IP en buckets de 5 minutos
grouped = (
    df.set_index("timestamp")
      .groupby("ip")
      .resample("5T")
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

# IPs sospechosas (MEDIUM o HIGH)
sospechosos = grouped[grouped["severity"].isin(["HIGH", "MEDIUM"])]

# Resumen
print("\n=== Analysis Summary ===")
print(f"Total failed attempts: {len(df)}")
print(f"Unique attacking IPs: {df['ip'].nunique()}")
print(f"High severity alerts: {len(sospechosos[sospechosos['severity'] == 'HIGH'])}")
print(f"Medium severity alerts: {len(sospechosos[sospechosos['severity'] == 'MEDIUM'])}")

if not user_stats.empty:
    top_user = user_stats.iloc[0]
    print(f"Most targeted user: {top_user['user']} ({top_user['failed_attempts']} attempts)")

# Guardar resultados
os.makedirs("results", exist_ok=True)
sospechosos.to_csv("results/sospechosos.csv", index=False)
df.to_csv("results/all_attempts.csv", index=False)
print("\nResults saved to:")
print("  results/sospechosos.csv")
print("  results/all_attempts.csv")
