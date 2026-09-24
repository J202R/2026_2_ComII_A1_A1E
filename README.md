<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 🚀 Proyecto Integrador — Fase 2. Modelado y Simulación

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Fase__2-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/Modulación-16--QAM-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Aplicación-DCI-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/Simulación-GNU%20Radio%20%7C%20Python-orange?style=flat-square" />
<img src="https://img.shields.io/badge/status-Modelado%20y%20Simulación-success?style=flat-square" />

*Semanas 7-9: 14 de septiembre – 4 de octubre de 2026*

</div>

> 📌 Esta rama corresponde a la **Entrega 2: Informe + Git**. Aquí se construye la cadena completa de transmisión y recepción 16-QAM en simulación, se inyectan AWGN e interferencia controlada y se evalúa el desempeño mediante curvas BER vs. SNR y métricas espectrales.

---

## 📑 Tabla de contenido

- [Integrantes y roles](#-integrantes-y-roles)
- [Contexto: del diseño a la simulación](#-contexto-del-diseño-a-la-simulación)
- [Objetivos de la Fase 2](#-objetivos-de-la-fase-2)
- [Arquitectura del sistema simulado](#-arquitectura-del-sistema-simulado)
- [Parámetros del sistema](#-parámetros-del-sistema)
- [Modelado del canal](#-modelado-del-canal)
- [Evidencias y gráficas requeridas](#-evidencias-y-gráficas-requeridas)
- [Evaluación de desempeño (BER vs. SNR)](#-evaluación-de-desempeño-ber-vs-snr)
- [Flujo de trabajo en Git](#-flujo-de-trabajo-en-git)
- [Entregables y lista de verificación](#-entregables-y-lista-de-verificación)
- [Cómo ejecutar la simulación](#-cómo-ejecutar-la-simulación)
- [Estructura del repositorio](#-estructura-del-repositorio)

---

## 👥 Integrantes y roles

| Integrante | Código | Rol | Responsabilidades en la Fase 2 |
|---|---|---|---|
| **Jarol Nicolas Molano Lopez** | `2230391` | **Líder de Proyecto y Gestor de Git** | Gestiona ramas y *pull requests*, integra los avances y coordina la redacción del informe IEEE. |
| **Juan Andres Rojas Rueda** | `2231065` | **Encargado de Modelado y Simulación** | Implementa Tx/Rx (GNU Radio / Python), curvas BER vs. SNR y gráficas de desempeño. |
| **William Camilo Motta Chacón** | `2234639` | **Encargado de SDR y Canal** | Modela AWGN e interferencia controlada, define parámetros de canal y prepara la transición hacia el hardware SDR (Fase 3). |

---

## 📖 Contexto: del diseño a la simulación

En la **Fase 1** se definió la aplicación: **Interconexión de Centros de Datos (DCI)** sobre enlaces ópticos de alta capacidad, con **16-QAM** como modulación (4 bits/símbolo) y un filtro conformador **RRC**.

En la **Fase 2** se valida ese diseño en un entorno simulado antes de cualquier despliegue en hardware. La simulación permite aislar los efectos del canal, probar el esquema de modulación y validar la mitigación de interferencia bajo condiciones **controladas y repetibles**.

---

## 🎯 Objetivos de la Fase 2

**Objetivo general:** implementar el modelo en software del sistema de comunicación digital 16-QAM, simulando las restricciones del canal (AWGN e interferencia controlada) y evaluando su desempeño mediante curvas BER vs. SNR e informes técnicos formales.

**Objetivos específicos**

1. Modelar los bloques del transmisor, el canal con interferencia y el receptor en la plataforma de simulación seleccionada.
2. Evaluar el impacto de la ISI, el ruido y la interferencia mediante PSD, diagramas de ojo y constelaciones.
3. Consolidar el trabajo colaborativo con el uso estricto de ramas (*branching*) en Git y un informe técnico en formato IEEE.

---

## 🧩 Arquitectura del sistema simulado

```text
┌────────────────┐   ┌──────────────────────┐   ┌───────────────────┐
│ Fuente de datos│──►│ Mapeo 16-QAM         │──►│ Filtro Tx (RRC)   │
│ (bits)         │   │ (4 bits/símbolo)     │   │                   │
└────────────────┘   └──────────────────────┘   └─────────┬─────────┘
                                                          ▼
┌────────────────┐   ┌──────────────────────┐   ┌───────────────────┐
│ Demodulador y  │◄──│ Canal: AWGN          │◄──│ Inyección de      │
│ sumidero       │   │                      │   │ interferencia     │
└───────┬────────┘   └──────────────────────┘   └───────────────────┘
        ▼
┌──────────────────────────────────────────────────────────────────────┐
│ Filtro acoplado RRC → muestreo óptimo → decisión → análisis:         │
│ BER, constelación, diagrama de ojo, PSD                              │
└──────────────────────────────────────────────────────────────────────┘
```

**Bloques del transmisor:** generación de bits → asignación de constelación → filtrado RRC.
**Bloques del receptor:** filtro acoplado RRC → muestreo óptimo → demodulación (decisión por mínima distancia).

---

## ⚙️ Parámetros del sistema

Relaciones fundamentales (según la Guía 1):

| Variable | Significado | Relación |
|---|---|---|
| `M` | Número de símbolos | `M = len(tabla_de_verdad_constelacion) = 16` |
| `bps` | Bits por símbolo | `bps = log2(M) = 4` |
| `Rs` | Tasa de símbolos | Valor de referencia del sistema |
| `Rb` | Tasa de bits | `Rb = Rs × bps` |
| `Sps` | Muestras por símbolo | Definida por el diseño |
| `samp_rate` | Tasa de muestreo | `samp_rate = Rs × Sps` |
| `β` (roll-off) | Factor del RRC | Compromiso entre ancho de banda e ISI |
| `BW` | Ancho de banda ocupado | `BW ≈ Rs × (1 + β)` |

**Valores base de partida** (tomados de los flujogramas de la Guía 1; ajustar y documentar en el informe si el equipo los modifica):

| Parámetro | Valor base |
|---|---|
| `Rs` | 32 kBd |
| `Sps` | 8 |
| `samp_rate` | 256 kHz |
| `Rb` | 128 kbps |
| `β` | *por definir (p. ej. 0.35)* |

**Tabla de constelación 16-QAM** (orden de la guía; el orden define qué grupo de bits selecciona cada punto):

```text
(-3-3j, -1-3j, 1-3j, 3-3j, 3-1j, 1-1j, -1-1j, -3-1j,
 -3+1j, -1+1j, 1+1j, 3+1j, 3+3j, 1+3j, -1+3j, -3+3j)
```

> 💡 Se recomienda conservar `Rs` y `Sps` entre pruebas y variar solo una cosa a la vez (ruido o interferencia), para distinguir qué efectos provienen de cada fuente.

---

## 🌊 Modelado del canal

| Componente | Descripción | Parámetro de control |
|---|---|---|
| **AWGN** | Ruido térmico blanco gaussiano aditivo, configurable en potencia/SNR. | SNR (dB) / `noise_amp` |
| **Interferencia controlada** | Según el escenario de la Fase 1: interferencia senoidal de banda estrecha, señal modulada interferente (análogo al *crosstalk* DWDM) o ruido impulsivo. | Potencia relativa (SIR) y frecuencia de la interferencia |

**Escenarios de simulación**

| # | Escenario | Descripción |
|---|---|---|
| 1 | Ideal | Sin ruido ni interferencia (referencia). |
| 2 | Solo AWGN | Barrido de SNR. |
| 3 | AWGN + interferencia | Interferencia controlada con distintas potencias. |

---

## 📈 Evidencias y gráficas requeridas

Para **cada escenario** (con y sin interferencia):

1. **Dominio del tiempo:** envolvente compleja (I/Q) y señal a la salida del canal.
2. **Dominio de la frecuencia:** PSD de la señal transmitida comparada con la PSD de la interferencia y del ruido.
3. **Diagrama de constelación:** comparativa en el plano complejo de **Tx**, **Rx sin ruido** y **Rx degradado**.
4. **Diagrama de ojo:** evaluación de la ISI tras el filtro acoplado.

---

## 📊 Evaluación de desempeño (BER vs. SNR)

- Curva **BER vs. SNR simulada** (Monte Carlo) para 16-QAM con AWGN, y con interferencia.
- Comparación contra la **curva teórica** de 16-QAM con codificación Gray:

  `BER ≈ (3/8) · erfc( √( 2·Eb/N0 / 5 ) )`

- Análisis de la degradación (en dB) producida por la interferencia respecto al caso solo AWGN.
- Cantidad de bits suficiente por punto de SNR para obtener una estimación estadísticamente confiable.

---

## 🌿 Flujo de trabajo en Git

Uso **estricto de ramas**: nadie hace *commit* directo a `main`.

```text
main
 └── fase-2                      → rama de integración de la fase
      ├── fase-2/modelado-txrx   → Juan Andres (Tx/Rx, BER)
      ├── fase-2/canal-interf    → William Camilo (AWGN + interferencia)
      └── fase-2/informe-ieee    → Jarol Nicolas (informe e integración)
```

```bash
git checkout -b fase-2/modelado-txrx     # crear rama de trabajo
git add . && git commit -m "feat: filtro RRC y receptor 16-QAM"
git push -u origin fase-2/modelado-txrx  # abrir Pull Request hacia fase-2
```

- Los *pull requests* son revisados y aprobados por el Gestor de Git.
- Mensajes de *commit* descriptivos (`feat:`, `fix:`, `docs:`).
- Al cierre de la fase, `fase-2` se integra a `main` con una etiqueta (`v2.0-fase2`).

---

## ✅ Entregables y lista de verificación

**Entrega 2: Informe + Git**

- [ ] Informe técnico en **formato IEEE** (≈ 3-5 páginas).
- [ ] Flujogramas / scripts de simulación **plenamente funcionales** (`.grc`, `.m` o `.py`).
- [ ] Transmisor 16-QAM con filtro RRC (Rs, samp_rate y β configurados).
- [ ] Receptor con filtro acoplado, muestreo óptimo y demodulador.
- [ ] Canal con AWGN configurable e interferencia controlada.
- [ ] Gráficas de tiempo, PSD y constelación (Tx, Rx sin ruido, Rx degradado).
- [ ] Diagrama de ojo.
- [ ] Curva BER vs. SNR (simulada vs. teórica).
- [ ] Historial de Git con ramas y *pull requests* aprobados.

---

## ▶️ Cómo ejecutar la simulación

**Requisitos:** Linux o Windows, Git, y GNU Radio Companion y/o Python 3 (`numpy`, `scipy`, `matplotlib`).

```bash
git clone <URL_DEL_REPOSITORIO>
cd 2026_2_ComII_A1_A1E
git checkout fase-2

# Python
pip install numpy scipy matplotlib
python Fase_2_Modelado_y_Simulacion/Entrega_2/codigo/simulacion_16qam.py

# GNU Radio
gnuradio-companion Fase_2_Modelado_y_Simulacion/Entrega_2/flujogramas/16QAM_AWGN.grc
```

> Los nombres de archivos anteriores son ilustrativos; ajustarlos a los que finalmente contenga el repositorio.

---

## 📁 Estructura del repositorio

```text
2026_2_ComII_A1_A1E/
├── README.md                                 → Documentación principal del repositorio
├── Fase_1_Diseno_y_Planeacion/               → (Semanas 1-3) ✔ Completada
│   └── Entrega_1/                            → Propuesta técnica preliminar y Git
├── Fase_2_Modelado_y_Simulacion/             → (Semanas 7-9) 🔄 En curso
│   └── Entrega_2/
│       ├── codigo/                           → Scripts de simulación (.py / .m)
│       ├── flujogramas/                      → Archivos GNU Radio (.grc)
│       ├── figuras/                          → PSD, constelaciones, ojo, BER vs. SNR
│       └── informe/                          → Informe técnico en formato IEEE
├── Fase_3_Implementacion_Experimental/       → (Semanas 6-8)
│   └── Entrega_3/                            → Integración con SDR y demostración
├── Fase_4_Validacion_Final/                  → (Semanas 8-10)
│   └── Documentacion_Tecnica/                → Ajustes y comparación real vs. simulado
└── Fase_5_Socializacion_y_Evaluacion/        → (Semana 14)
    └── Presentacion/                         → Soportes para la sustentación final
```
