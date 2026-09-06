<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 🧪 Práctica 1 — Introducción a GNURadio, Python Block y GitHub

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Practica__1-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/GNU%20Radio-Companion-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Python-Embedded%20Block-yellow?style=flat-square&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/status-mergeado%20a%20main-success?style=flat-square" />

*1 de septiembre de 2026*

</div>

> 📌 Esta rama corresponde al desarrollo de la **Práctica 1** del curso. Aquí se integran (vía *merge*) los aportes individuales realizados en las subramas personales `P1_Jarol`, `P1_Juan` y `P1_william`.

---

## 📑 Tabla de contenido

- [Descripción de la práctica](#-descripción-de-la-práctica)
- [Integrantes y archivos aportados](#-integrantes-y-archivos-aportados)
- [Estructura de directorios](#-estructura-de-directorios)
- [Bloques desarrollados](#-bloques-desarrollados)
- [Aplicación: análisis estadístico de una señal ECG](#-aplicación-análisis-estadístico-de-una-señal-ecg)
- [Resultados](#-resultados)
- [Conclusiones](#-conclusiones)
- [Cómo reproducir esta práctica](#-cómo-reproducir-esta-práctica)
- [Referencias](#-referencias)

---

## 📖 Descripción de la práctica

Esta práctica introduce el diseño de bloques personalizados en Python (*Embedded Python Block*) dentro de **GNU Radio Companion**, orientados al procesamiento de señales en tiempo real. Se implementaron y corrigieron tres bloques base propuestos por el libro guía del curso:

1. **Acumulador** (`e_Acum`) — suma acumulativa de una señal, con memoria de estado entre buffers.
2. **Diferenciador** (`e_Diff`) — diferencia discreta entre muestras consecutivas, con continuidad entre buffers.
3. **Estadísticas de tiempo** (`Promedios_de_tiempos`) — cálculo acumulativo de media, media cuadrática (MS), RMS, potencia promedio y desviación estándar.

Finalmente, estos bloques se integraron en una aplicación práctica de **caracterización y mitigación de ruido** sobre una señal real de electrocardiograma (ECG).

---

## 👥 Integrantes y archivos aportados

Cada integrante desarrolló su parte en su propia subrama (`P1_Nombre`) dentro de la carpeta `GNURadio`, y posteriormente se hizo **merge** de esa subrama hacia `Practica_1`.

| Integrante | Subrama | Archivo(s) aportado(s) | Bloque(s) trabajado(s) |
|---|---|---|---|
| **Jarol Nicolás Molano López** | `P1_Jarol` | `Acumulador_Final.grc`, `Diferenciador_Final.grc` | Bloque acumulador (`e_Acum`) y bloque diferenciador (`e_Diff`) |
| **Juan Andrés Rojas Rueda** | `P1_Juan` | `ECG_Final.grc` | Aplicación integrada: análisis estadístico sobre señal ECG (original, con ruido y filtrada) |
| **William Camilo Motta Chacón** | `P1_william` | `Estadistico_Final.grc` | Bloque de estadísticas de tiempo (`Promedios_de_tiempos`) |

> 🔀 Los tres flowgraphs fueron fusionados (*merge*) en la rama `Practica_1`, que constituye la versión de "preproducción" revisada por el docente.

---

## 📁 Estructura de directorios

```
Practica_1/
├── GNURadio/
│   ├── Acumulador_Final.grc        → Jarol
│   ├── Diferenciador_Final.grc     → Jarol
│   ├── Estadistico_Final.grc       → William
│   └── ECG_Final.grc               → Juan
└── Informe/
    └── Practica_1_ComII_A1_A1E.pdf
```

---

## 🧩 Bloques desarrollados

### 1️⃣ Bloque acumulador (`e_Acum`)

Corrige el código base, que reiniciaba la suma en cada buffer y retornaba una variable inexistente. Se agregó la variable de estado `valor_anterior` para conservar la acumulación entre llamados sucesivos a `work`.

```python
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self, name='e_Acum',
            in_sig=[np.float32],
            out_sig=[np.float32])
        self.valor_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]
        y0[:] = self.valor_anterior + np.cumsum(x)
        if len(y0) > 0:
            self.valor_anterior = y0[-1]
        return len(y0)
```

### 2️⃣ Bloque diferenciador (`e_Diff`)

Corrige un error de sintaxis del código base y añade la variable `muestra_anterior` para mantener continuidad entre buffers antes de aplicar `np.diff`.

```python
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self, name='e_Diff',
            in_sig=[np.float32],
            out_sig=[np.float32])
        self.muestra_anterior = 0.0

    def work(self, input_items, output_items):
        x = input_items[0]
        y0 = output_items[0]
        if len(x) == 0:
            return 0
        x_completo = np.insert(x, 0, self.muestra_anterior)
        y0[:] = np.diff(x_completo)
        self.muestra_anterior = x[-1]
        return len(y0)
```

### 3️⃣ Bloque de estadísticas de tiempo (`Promedios_de_tiempos`)

Calcula de forma acumulativa cinco estimadores: **media**, **media cuadrática (MS)**, **RMS**, **potencia promedio** y **desviación estándar**, usando acumuladores escalares (`acum_x`, `acum_x2`) y la identidad σ² = E[X²] − (E[X])² para simplificar el cálculo.

```python
import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self, name='Promedios_de_tiempos',
            in_sig=[np.float32],
            out_sig=[np.float32]*5)
        self.acum_x = 0.0
        self.acum_x2 = 0.0
        self.Ntotales = 0

    def work(self, input_items, output_items):
        x = input_items[0]
        y0, y1, y2, y3, y4 = output_items
        N = len(x)
        if N == 0:
            return 0
        self.Ntotales += N
        self.acum_x += np.sum(x)
        self.acum_x2 += np.sum(x**2)
        media = self.acum_x / self.Ntotales
        ms = self.acum_x2 / self.Ntotales
        rms = np.sqrt(ms)
        var = ms - media**2
        if var < 0:
            var = 0
        std = np.sqrt(var)
        y0[:] = media
        y1[:] = ms
        y2[:] = rms
        y3[:] = ms
        y4[:] = std
        return len(x)
```

---

## ❤️ Aplicación: análisis estadístico de una señal ECG

Se utilizó una señal real de ECG limpia (registro 118 de la **MIT-BIH Arrhythmia Database**), a la cual se le añadió ruido gaussiano artificial (bloques *Noise Source* + *Add*), posteriormente atenuado con un bloque *Moving Average* (longitud 4 muestras, escala 1/M), cumpliendo la frecuencia máxima de monitoreo clínico *f*<sub>max</sub> = 40 Hz.

Las tres versiones de la señal (**original**, **con ruido** y **filtrada**) se conectaron a tres instancias del bloque `Promedios_de_tiempos` para comparar sus estimadores estadísticos.

---

## 📊 Resultados

**Comparación de estimadores estadísticos — señal ECG (original, con ruido y filtrada):**

| Estimador | Original | Con ruido | Filtrada |
|---|---|---|---|
| Desviación estándar | 0.404398 | 0.638660 | 0.439031 |
| Potencia promedio | 1.176480 | 1.412420 | 1.241412 |
| RMS | 1.084656 | 1.188453 | 1.114187 |
| Media cuadrática | 1.176480 | 1.412420 | 1.241412 |
| Media | -1.006450 | -1.002264 | -1.024043 |

**Pruebas individuales:**

- **Diferenciador:** ante una señal constante (5.5), la salida permanece en cero; ante una señal rampa periódica (1,2,3,4,5,0), la salida presenta los saltos esperados (1,1,1,1,−5), validando que el bloque responde solo a los cambios de la señal.
- **Acumulador:** ante una señal constante (1m), la salida crece linealmente sin saltos entre buffers, confirmando la conservación correcta del estado interno.
- **Estadísticas de tiempo:** ante una señal cosenoidal de 1 kHz y amplitud 1, los estimadores convergen a los valores teóricos esperados (potencia promedio ≈ 0.5, RMS ≈ 0.707).

---

## ✅ Conclusiones

- La señal con ruido añadido presenta valores más altos de desviación estándar, potencia promedio y RMS respecto a la señal original.
- El filtrado con *Moving Average* reduce estos valores acercándolos a los de la señal original, aunque sin recuperarla por completo, ya que el promediado modifica ligeramente la forma de onda.
- Los tres bloques personalizados (acumulador, diferenciador y estadísticas de tiempo) fueron validados exitosamente frente a señales de prueba conocidas y frente a una señal real (ECG).

---

## 🔄 Cómo reproducir esta práctica

```bash
git clone https://github.com/J202R/2026_2_ComII_A1_A1E.git
cd 2026_2_ComII_A1_A1E
git checkout Practica_1
```

Abrir cualquiera de los flowgraphs con GNU Radio Companion:

```bash
gnuradio-companion Practica_1/GNURadio/Acumulador_Final.grc
gnuradio-companion Practica_1/GNURadio/Diferenciador_Final.grc
gnuradio-companion Practica_1/GNURadio/Estadistico_Final.grc
gnuradio-companion Practica_1/GNURadio/ECG_Final.grc
```

---

## 📚 Referencias

1. Wikipedia contributors, *"Gnu radio — embedded python block"*, 2025. [wiki.gnuradio.org](https://wiki.gnuradio.org/index.php/Embedded_Python_Block)
2. H. Ortega Boada y O. M. Reyes Torres, *Comunicaciones Digitales basadas en radio definida por software*. Bucaramanga, Colombia: Universidad Industrial de Santander, 2019.
3. G. B. Moody y R. G. Mark, *"MIT-BIH Arrhythmia Database"*, 2005, registro 118. [physionet.org](https://physionet.org/content/mitdb/1.0.0/)
4. O. J. Tíjaro R., *"The time averages"*, E3T-UIS, sep. 2025, material de clase.
5. Wave Walker DSP, *"Bandwidth of a moving average filter"*, ago. 2022. [wavewalkerdsp.com](https://www.wavewalkerdsp.com/2022/08/03/bandwidth-of-a-moving-average-filter/)

---

<div align="center">

*Construimos Futuro* 🇨🇴

</div>
