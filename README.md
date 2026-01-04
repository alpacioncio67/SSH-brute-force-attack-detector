# 🔐 SSH Brute Force Log Analyzer (v2)

Proyecto educativo orientado a **ciberseguridad defensiva** y **análisis de datos**, cuyo objetivo es analizar logs de autenticación SSH (`auth.log`) para detectar **posibles ataques de fuerza bruta** mediante ventanas temporales, clasificación de severidad y un resumen tipo SOC.

Este proyecto está pensado para demostrar:

* Pensamiento de **analista de seguridad (SOC)**
* Uso de **Python para análisis de logs**
* Buenas prácticas de scripting (CLI, estructura, outputs)

---

## 🧠 ¿Qué hace el proyecto?

El programa analiza logs SSH y:

* Extrae **timestamp, IP atacante y usuario objetivo**
* Detecta **intentos fallidos de autenticación**
* Agrupa eventos por **ventanas de tiempo (5 minutos)**
* Clasifica los eventos por **severidad (LOW / MEDIUM / HIGH)**
* Identifica:

  * IPs sospechosas
  * Usuarios más atacados
* Genera un **resumen tipo SOC** en consola
* Exporta resultados a CSV

---

## 🗂️ Estructura del proyecto

```
ssh-log-analyzer/
│
├── analyzer.py              # Script principal
├── data/
│   └── auth.log             # Logs de ejemplo (o logs reales)
├── results/
│   └── sospechosos.csv      # Resultados del análisis
├── README.md
└── requirements.txt
```

---

## ⚙️ Requisitos

* Python 3.8+
* Librerías:

  * pandas

Instalación:

```bash
pip install pandas
```

---

## ▶️ Uso (CLI)

El programa se ejecuta desde la línea de comandos usando `argparse`:

```bash
python analyzer.py --logfile data/auth.log
```

### Argumentos

| Argumento   | Descripción                                         |
| ----------- | --------------------------------------------------- |
| `--logfile` | Ruta al archivo `auth.log` a analizar (obligatorio) |

Ejemplo con logs reales (Kali Linux):

```bash
python analyzer.py --logfile /var/log/auth.log
```

---

## 📊 Análisis realizado

### 1️⃣ Detección de intentos fallidos

Se filtran las líneas que contienen:

```
Failed password
```

---

### 2️⃣ Extracción de campos clave

De cada evento se extraen:

* Timestamp
* IP de origen
* Usuario objetivo

---

### 3️⃣ Ventana temporal

Los eventos se agrupan por IP en una **ventana móvil de 5 minutos**, permitiendo distinguir entre:

* Actividad normal
* Ataques de fuerza bruta

---

### 4️⃣ Clasificación de severidad

| Intentos en 5 min | Severidad |
| ----------------- | --------- |
| < 10              | LOW       |
| 10 – 19           | MEDIUM    |
| ≥ 20              | HIGH      |

---

### 5️⃣ Resumen tipo SOC

El programa genera un resumen en consola con:

* Total de intentos fallidos
* Número de IPs atacantes únicas
* Número de alertas de alta severidad
* Usuario más atacado

Ejemplo:

```
=== Analysis Summary ===
Total failed attempts: 87
Unique attacking IPs: 5
High severity alerts: 2
Most targeted user: root (45 attempts)
```

---

## 📁 Output

Se genera un archivo CSV con las IPs sospechosas:

```
results/sospechosos.csv
```

Incluye:

* IP
* Timestamp
* Número de intentos
* Severidad

Este archivo puede ser usado para:

* Bloqueo de IPs
* Reglas de firewall
* Análisis posterior

---

## 🐉 Kali Linux vs Logs de ejemplo

Este proyecto puede ejecutarse:

### ✅ En Windows

Usando logs de ejemplo incluidos en `data/auth.log`.

### ✅ En Kali Linux / Linux real

Usando logs reales del sistema:

```
/var/log/auth.log
```

Esto permite:

* Validar el funcionamiento en un entorno real
* Simular el flujo de trabajo de un SOC

---

## 🧩 Tecnologías utilizadas

* Python
* pandas
* argparse
* regex

---

## 🚀 Posibles mejoras futuras

* Ventana temporal configurable por CLI
* Umbrales de severidad configurables
* Detección por IP + usuario
* Exportar resumen a archivo `.txt` o `.md`
* Visualizaciones
* Tests automáticos

---

## 🎓 Objetivo educativo

Este proyecto está diseñado como **proyecto de aprendizaje** para:

* Ciberseguridad defensiva
* Análisis de logs
* Análisis de datos con Python
* Buenas prácticas para proyectos en GitHub

---

## 👤 Autor

Proyecto desarrollado con fines educativos y de portfolio.
