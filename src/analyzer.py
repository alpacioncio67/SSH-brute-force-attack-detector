import re
import pandas

#Primero, leemos el archivo de logs
logs = "Analizador/data/auth.log"
ips = []
pattern = r"from (\d+\.\d+\.\d+\.\d+)"

with open(logs,"r") as file:
    logs = file.readlines()

#Ahora vamos a filtrar aquellos intentos fallidos
logs_fallidos = [l for l in logs if "Failed password" in l]

#Ahora vamos a extraer las IPs de dichos logs fallidos, para analizarlas posteriormente
for line in logs_fallidos:
    match = re.search(pattern,line)
    if match:
        ips.append(match.group(1))

#Ahora vamos a realizar el análisis con pandas

#Transformamos los datos en una tabla
df = pandas.DataFrame(ips,columns=["ip"])
counts = df["ip"].value_counts()

limite = 5
sospechosos = counts[counts>=limite]

#Esto también podría hacerse con un Counter importado de collections, en lugar de usar pandas

print(sospechosos)

#Por último, guardamos los resultados
sospechosos.to_csv("Analizador/results/sospechosos.csv")

