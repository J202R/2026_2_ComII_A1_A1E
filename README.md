<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 📡 Práctica 2 — PSD de Señales Aleatorias en GNU Radio

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Practica__2-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/GNU%20Radio-Companion-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Git-GitHub-black?style=flat-square&logo=git" />
<img src="https://img.shields.io/badge/PSD-Señales%20Aleatorias-orange?style=flat-square" />

---

*Septiembre de 2026*

</div>

> 📌 Esta rama corresponde al desarrollo de la **Práctica 2** del curso de Comunicaciones II.  
> En esta práctica se estudia la **Densidad Espectral de Potencia (PSD)** de señales aleatorias utilizando **GNU Radio**, analizando señales binarias bipolares, ruido blanco y señales provenientes de fuentes del mundo real como imágenes y audio.

---

## 📑 Tabla de contenido

- [Descripción de la práctica](#-descripción-de-la-práctica)
- [Objetivos](#-objetivos)
- [Integrantes y archivos aportados](#-integrantes-y-archivos-aportados)
- [Estructura de directorios](#-estructura-de-directorios)
- [Desarrollo de la práctica](#-desarrollo-de-la-práctica)
- [Señal binaria aleatoria bipolar](#-señal-binaria-aleatoria-bipolar)
- [Análisis del ruido blanco](#-análisis-del-ruido-blanco)
- [Análisis de una imagen](#-análisis-de-una-imagen)
- [Análisis de una señal de audio](#-análisis-de-una-señal-de-audio)
- [Preguntas de control](#-preguntas-de-control)
- [Resultados y observaciones](#-resultados-y-observaciones)
- [Conclusiones](#-conclusiones)
- [Cómo reproducir esta práctica](#-cómo-reproducir-esta-práctica)
- [Referencias](#-referencias)

---

## 📖 Descripción de la práctica

La **Densidad Espectral de Potencia (PSD)** permite analizar cómo se distribuye la potencia de una señal en función de la frecuencia. Esta herramienta es fundamental para estudiar la estructura espectral de señales y reconocer características que no son evidentes únicamente en el dominio temporal.

En esta práctica se estudia el comportamiento de señales aleatorias mediante diferentes bloques de **GNU Radio**, realizando observaciones tanto en el dominio del tiempo como en el dominio de la frecuencia.

El desarrollo inicia con una **señal binaria aleatoria bipolar de forma rectangular**, para posteriormente analizar el comportamiento del ruido blanco y estudiar qué sucede cuando los bits provienen de fuentes reales, específicamente una **imagen (`rana.jpg`)** y una señal de **audio (`sonido.wav`)**.

La guía de la práctica plantea el análisis de la señal para diferentes valores de muestras por símbolo (**Sps = 4, 8, 16 y 1**), además del estudio de parámetros como frecuencia de muestreo, rata de bits y ancho de banda. :contentReference[oaicite:2]{index=2}

---

## 🎯 Objetivos

### Objetivo general

Interiorizar los conceptos relacionados con las **señales aleatorias** y utilizarlos para generar patrones con los cuales sea posible calcular y analizar la **Densidad Espectral de Potencia (PSD)**. :contentReference[oaicite:3]{index=3}

### Objetivos específicos

- Generar funciones a partir de bloques de implementación de código para generar los vectores de promedio.
- Producir diferentes combinaciones de bloques de **GNU Radio** para aplicaciones específicas relacionadas con señales aleatorias.
- Analizar señales binarias aleatorias en el dominio temporal y frecuencial.
- Estudiar el efecto de diferentes valores de **Sps** sobre la PSD.
- Comparar las características espectrales de señales binarias provenientes de diferentes fuentes.
- Analizar el comportamiento del ruido blanco en tiempo y frecuencia. :contentReference[oaicite:4]{index=4}

---

## 👥 Integrantes y archivos aportados

Cada integrante desarrolló una parte de la práctica en su respectiva rama personal y posteriormente los aportes fueron integrados en la rama correspondiente a la **Práctica 2**.

| Integrante | Subrama | Archivo(s) / aporte realizado |
|---|---|---|
| **Jarol Nicolás Molano López** | `P2_Jarol` | Informe completo de la práctica realizado en Overleaf y exportado a PDF |
| **Juan Andrés Rojas Rueda** | `P2_Juan` | Diagramas de GNU Radio, gráficas, evidencias y fotografías de la práctica |
| **William Camilo Motta Chacón** | `P2_william` | Preguntas de control respondidas y organizadas en PDF |

> 🔀 Los aportes de los tres integrantes permiten consolidar el desarrollo completo de la práctica: informe, evidencias experimentales y preguntas de control.

---

## 📁 Estructura de directorios

```text
Practica_2/
├── GNURadio/
│   ├── [Flowgraphs de GNU Radio]
│   ├── [Diagramas y evidencias]
│   └── [Gráficas obtenidas]
│
├── Informe/
│   ├── Informe_Practica_2.pdf
│   └── Preguntas_Practica_2.pdf
│
├── Fotos/
│   └── [Evidencias fotográficas]
│
└── README.md
