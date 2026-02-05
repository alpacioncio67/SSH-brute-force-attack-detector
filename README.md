# SSH Brute Force Log Analyzer
Pequeño script en Python que analiza logs de autenticación SSH (auth.log) para detectar posibles ataques de fuerza bruta usando ventanas temporales, niveles de severidad y un resumen tipo SOC.

# ¿Qué hace la herramienta?
El analizador:

Busca intentos fallidos de autenticación SSH (Failed password) en los logs.

Extrae de cada línea: timestamp, IP atacante y usuario objetivo.

Agrupa los eventos por IP en una ventana de 5 minutos para detectar patrones de fuerza bruta.

Asigna una severidad según el número de intentos en esa ventana: LOW, MEDIUM o HIGH.

Genera un resumen en consola (IPs atacantes, usuario más atacado, total de intentos, etc.).

Exporta un CSV con las IPs sospechosas para uso posterior (reglas de firewall, bloqueos, análisis, etc.).

# Requisitos
Python 3 y la librería pandas.

# Instalación rápida de dependencias:

bash
Opción 1:
python3 -m pip install --user pandas

Opción 2: paquetes del sistema (Debian/Ubuntu)
sudo apt update
sudo apt install python3-pandas

# Cómo usar la herramienta
1. Clonar el repositorio
bash
git clone https://github.com/alpacioncio67/SSH-brute-force-attack-detector.git
cd SSH-brute-force-attack-detector
2. Ejecutar con el log de ejemplo
Desde la carpeta del proyecto:

bash
python3 src/analyzer.py --logfile data/auth.log
Esto analizará el archivo data/auth.log incluido en el repo y generará la salida correspondiente.

3. Analizar logs reales de tu sistema
En muchas distribuciones Linux, el log de autenticación está en:

bash

/var/log/auth.log
Ejemplo de uso con un log real:

bash

sudo python3 analyzer.py /var/log/auth.log
Usa sudo solo si tu usuario no puede leer el log directamente.

# Qué información obtendrás
Al terminar la ejecución, verás algo similar en la consola:

text

=== Analysis Summary ===
Total failed attempts: 87
Unique attacking IPs: 5
High severity alerts: 2
Most targeted user: root (45 attempts)
Y en results/sospechosos.csv encontrarás columnas como:

IP

Timestamp (ventana donde se detectó el ataque)

attempts (número de intentos en la ventana)

severity (LOW / MEDIUM / HIGH)

Este CSV se puede usar para:

Automatizar bloqueos de IPs.

Crear reglas de firewall.

# Ideas para probarlo
Generar tus propios intentos fallidos con una herramienta de fuerza bruta (por ejemplo, hydra) contra una máquina de pruebas para ver cómo los detecta el script.

Ajustar el tamaño de la ventana de tiempo o los umbrales de severidad dentro de analyzer.py para experimentar con distintos criterios de alerta.

# Objetivo educativo
Este proyecto está pensado como ejercicio práctico de:

Ciberseguridad defensiva.

Análisis de logs.

Análisis de datos con Python.

Buenas prácticas básicas en proyectos de línea de comandos y GitHub.
