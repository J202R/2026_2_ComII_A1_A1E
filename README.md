<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 🚀 Proyecto Integrador — Fase 1. Diseño Conceptual y Planeación

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Fase__1-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/Modulación-16--QAM-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Aplicación-DCI-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/status-Propuesta%20y%20Git-success?style=flat-square" />

*14 de septiembre de 2026*

</div>

> 📌 Esta rama corresponde a la **Entrega 1: Propuesta y Git** del proyecto integrador. Aquí se define la estructura inicial del repositorio, los roles del equipo, el planteamiento del sistema digital basado en 16-QAM y las métricas teóricas a evaluar.

---

## 📑 Tabla de contenido

- [Integrantes y asignación de roles](#-integrantes-y-asignación-de-roles)
- [Descripción del escenario y aplicación](#-descripción-del-escenario-y-aplicación)
- [Justificación técnica del sistema](#-justificación-técnica-del-sistema)
- [Condiciones y degradaciones del canal](#-condiciones-y-degradaciones-del-canal)
- [Métricas de desempeño](#-métricas-de-desempeño)
- [Aclaración sobre la implementación](#-aclaración-sobre-la-implementación)
- [Estructura del repositorio](#-estructura-del-repositorio)

---

## 👥 Integrantes y asignación de roles

El equipo de trabajo ha distribuido las responsabilidades técnicas fundamentales para el desarrollo del proyecto y la administración del flujo de trabajo en Git.

| Integrante | Código | Rol Asignado | Responsabilidades Principales |
|---|---|---|---|
| **Jarol Nicolas Molano Lopez** | `2230391` | **Líder de Proyecto y Gestor de Git** | Administra el repositorio, aprueba solicitudes de extracción (*pull requests*) y coordina la integración de avances. |
| **Juan Andres Rojas Rueda** | `2231065` | **Encargado de Modelado y Simulación** | Diseña los bloques principales en software (GNU Radio, Python). |
| **William Camilo Motta Chacón** | `2234639` | **Encargado de SDR y Canal** | Define los parámetros físicos del hardware y la inyección de interferencia/ruido. |

---

## 📖 Descripción del escenario y aplicación

### Interconexión de Centros de Datos (DCI)
La aplicación seleccionada en el entorno industrial corresponde a la **interconexión de centros de datos (Data Center Interconnect, DCI)** mediante enlaces ópticos de alta capacidad. El crecimiento del tráfico entre estos centros exige aumentar la capacidad de los enlaces sin tener que incrementar continuamente la infraestructura física de fibra. 

La función principal de este sistema es transportar grandes volúmenes de información digital a altas tasas de transmisión, generados por servicios de almacenamiento, replicación de datos, copias de seguridad y cargas de inteligencia artificial.

---

## 🧩 Justificación técnica del sistema

Para abordar la necesidad de alta capacidad en el enlace, el proyecto se centrará en el uso de **16-QAM** como técnica de modulación.

*   **Eficiencia Espectral:** En un sistema basado en 16-QAM, los datos binarios se agrupan en conjuntos de 4 bits por símbolo (log2(16) = 4 bits/símbolo). Esto resulta adecuado porque permite alcanzar una mayor eficiencia espectral y aprovechar mejor el ancho de banda disponible.
*   **Requerimientos del Enlace:** Teóricamente se definirá el ancho de banda estimado (BW) y la tasa de símbolos (Rs).
*   **Filtrado:** Se utilizará un filtro formador de pulsos de tipo Coseno Alzado o Raíz de Coseno Alzado (RRC) para la mitigación de interferencia.

---

## ⚠️ Condiciones y degradaciones del canal

Al existir 16 puntos en la constelación, los símbolos presentan una separación menor, lo que introduce un compromiso entre capacidad y robustez frente al ruido. En un enlace óptico basado en 16-QAM pueden presentarse fenómenos como:

*   **Ruido óptico:** Altera la amplitud y fase de los símbolos.
*   **Reducción del OSNR:** El ruido acumulado disminuye la relación entre la potencia de la señal y el ruido óptico.
*   **Dispersión cromática y efectos no lineales:** Producen distorsión espectral a grandes distancias y a niveles elevados de potencia en la fibra.
*   **Crosstalk DWDM:** Interferencia entre canales cuando múltiples longitudes de onda comparten la fibra.

---

## 📊 Métricas de desempeño

Para la caracterización teórica de la propuesta y la evaluación integral del sistema de comunicación digital, se medirán las siguientes variables:

1.  **Métrica de Error:** 
    *   Curva teórica esperada de Tasa de Error de Bit (BER vs. SNR).
    *   **BER:** Medirá la cantidad de bits recibidos incorrectamente.
2.  **Métricas Espectrales y de Calidad:** 
    *   Ancho de banda ocupado y Densidad Espectral de Potencia (PSD).
    *   **OSNR/SNR:** Calidad de la señal respecto al ruido.
    *   **EVM:** Distancia de los símbolos recibidos respecto a sus posiciones ideales.
    *   **Tasa de transmisión:** Relación de la modulación con la capacidad del enlace.
3.  **Métricas de Canal y Tiempo:**
    *   Evaluación de la Interferencia Intersimbólica (ISI) mediante la apertura del **Diagrama de Ojo**.
    *   **Diagrama de constelación:** Para observar visualmente la degradación y el desplazamiento de los 16 símbolos por efecto del ruido/interferencia.

---

## 🛠️ Aclaración sobre la implementación

Debido a que la aplicación corresponde a un entorno de alta capacidad industrial y el proyecto se desarrolla en un entorno académico, **el sistema será modelado y evaluado mediante simulación**. 

Se emplearán radios de comunicación definida por software (SDR) como medio experimental para representar de forma controlada las condiciones de un enlace de transmisión, analizando el comportamiento de la modulación frente a la calidad de la señal y el ruido.

---

## 📁 Estructura del repositorio

Para llevar un control estricto del progreso y facilitar la reutilización de recursos[cite: 2], el repositorio está organizado en directorios que corresponden a cada hito del proyecto:

```text
2026_2_ComII_A1_A1E/
├── README.md                                 → Documentación principal del repositorio
├── Fase_1_Diseno_y_Planeacion/               → (Semanas 1-3)
│   └── Entrega_1/                            → Propuesta técnica preliminar y Git
├── Fase_2_Modelado_y_Simulacion/             → (Semanas 3-6)
│   └── Entrega_2/                            → Códigos, modelado e informe técnico
├── Fase_3_Implementacion_Experimental/       → (Semanas 6-8)
│   └── Entrega_3/                            → Integración con SDR y demostración
├── Fase_4_Validacion_Final/                  → (Semanas 8-10)
│   └── Documentacion_Tecnica/                → Ajustes y comparación real vs simulado
└── Fase_5_Socializacion_y_Evaluacion/        → (Semana 14)
    └── Presentacion/                         → Soportes para la sustentación final
