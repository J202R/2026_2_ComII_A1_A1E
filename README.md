<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# 📡 Proyecto Integrador — Fase 3. Implementación Experimental

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Fase__3-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/Modulación-16--QAM-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Aplicación-DCI-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/Hardware-HackRF%20One-orange?style=flat-square" />
<img src="https://img.shields.io/badge/status-Implementación%20SDR-success?style=flat-square" />

</div>

> 📌 Esta rama corresponde a la **Entrega 3: Informe + Git**. El canal simulado de la Fase 2 se reemplaza por un enlace físico entre **dos HackRF One**, conservando los parámetros de diseño y caracterizando el comportamiento real del enlace.

---

## 📑 Tabla de contenido

- [Integrantes y roles](#-integrantes-y-roles)
- [Contexto: de la simulación al hardware](#-contexto-de-la-simulación-al-hardware)
- [Objetivos de la Fase 3](#-objetivos-de-la-fase-3)
- [Arquitectura del enlace](#-arquitectura-del-enlace)
- [Parámetros del sistema y del radio](#-parámetros-del-sistema-y-del-radio)
- [Pruebas realizadas](#-pruebas-realizadas)
- [Resultados principales](#-resultados-principales)
- [Flujo de trabajo en Git](#-flujo-de-trabajo-en-git)
- [Entregables y lista de verificación](#-entregables-y-lista-de-verificación)
- [Cómo ejecutar](#-cómo-ejecutar)
- [Estructura del repositorio](#-estructura-del-repositorio)

---

## 👥 Integrantes y roles

| Integrante | Código | Rol | Responsabilidades en la Fase 3 |
|---|---|---|---|
| **Jarol Nicolas Molano Lopez** | `2230391` | **Líder de Proyecto y Gestor de Git** | Gestiona ramas y *pull requests*, integra avances y coordina el informe IEEE. |
| **Juan Andres Rojas Rueda** | `2231065` | **Encargado de Modelado y Simulación** | Adapta Tx/Rx de GNU Radio (sincronización, decodificador de texto) y analiza resultados. |
| **William Camilo Motta Chacón** | `2234639` | **Encargado de SDR y Canal** | Configura los HackRF One, el montaje, las mediciones y la verificación con analizador de espectro. |

---

## 📖 Contexto: de la simulación al hardware

En la **Fase 2** el sistema 16-QAM se validó por completo en simulación (GNU Radio y Python). En la **Fase 3** la señal I/Q sale por un HackRF One, se propaga por aire (≈2 m) y la adquiere un segundo HackRF One. El objetivo no es medir BER, sino configurar bien el radio y observar los problemas reales que no existían en simulación: nivel de señal, saturación, componente DC, fuga del oscilador local, desplazamiento de frecuencia y pérdida de sincronía.

---

## 🎯 Objetivos de la Fase 3

**Objetivo general:** integrar dos HackRF One con el Tx y el Rx 16-QAM de las fases previas, sin alterar los parámetros de diseño, y caracterizar el enlace físico resultante.

**Objetivos específicos**

1. Relacionar frecuencia central, tasa de muestreo, ganancias y ancho de banda del radio con las variables de banda base.
2. Verificar el espectro del transmisor con un analizador de espectro.
3. Evaluar el efecto de la amplitud digital (Tx) y de las ganancias LNA/VGA (Rx) sobre potencia, constelación y mensaje decodificado.
4. Identificar casos de ruido dominante y saturación, y el efecto de un canal adyacente y del pico DC.
5. Distinguir parámetros de diseño de comunicaciones frente a parámetros de interfaz de hardware.

---

## 🧩 Arquitectura del enlace

```text
TX (PC + HackRF #1)                                   RX (PC + HackRF #2)
Bits / texto⊕PN → Mapeo 16-QAM → RRC → Canal emulado → ×32 → +200 kHz → Osmocom Sink
                                                     ))) aire (~2 m) (((
Osmocom Source → +lo_offset → ÷32 → AGC → FLL → RRC → Gardner → Costas(4) → AGC → Decisión / decodificador de texto
```

- **Canal emulado de la Fase 2** conservado en el Tx (atenuación, AWGN con Es/N0 ≈ 27 dB y canal vecino a 36 kHz).
- **Sincronización añadida:** AGC, FLL de borde de banda, Gardner, Costas de orden 4.
- **Decodificador de texto propio:** busca delimitadores en las 4 rotaciones de 90° y 2 alineaciones, y reporta el % de caracteres correctos.

---

## ⚙️ Parámetros del sistema y del radio

| Parámetro | Valor |
|---|---|
| `Rs` / `Sps` / `Rb` | 32 kBd / 8 / 128 kb/s |
| Filtro RRC | β = 0.35, 81 coeficientes, B = 43.2 kHz |
| Tasa banda base → radio | 256 kS/s → 8.192 MS/s (L = M = 32) |
| Frecuencia | 880 MHz (verificación del Tx), 890 MHz (enlace) |
| Frecuencia Tx / Rx | `fc − 200 kHz` / `fc + lo_offset` |
| Ganancia Tx IF | 47 dB |
| LNA / VGA (Rx) | 0–40 dB (pasos de 8) / 0–62 dB (pasos de 2) |
| Amp. RF, Bias-T | Desactivados |

---

## 🧪 Pruebas realizadas

1. Espectro del Tx a 880 MHz con analizador.
2. Amplitud digital `A_tx` = 0.03, 0.1, 0.15.
3. Barrido de VGA (4, 10, 20, 26 dB) y de LNA (8–32 dB).
4. Casos extremos: LNA = VGA = 0 dB y LNA = VGA = 40 dB.
5. Canal adyacente con `A_int` = 0.2, 0.3, 0.5.
6. Posición del pico DC: `lo_offset` = 0.1, 0.6, 2 MHz.
7. Separación máxima de antenas y configuración final (LNA = 32 dB).

---

## 📊 Resultados principales

| LNA [dB] | VGA [dB] | Nivel [dBFS] | Constelación |
|:-:|:-:|:-:|---|
| 0 | 0 | −66.6 | Nube sin estructura |
| 24 | 26 | −27.9 | Anillos, menor dispersión |
| 32 | 4 | −26.1 | **16 grupos (óptimo)** |
| 40 | 40 | −0.4 | Saturación del ADC |

- Con LNA = 32 dB / VGA = 4 dB el mensaje se recuperó con **91–100 %** de caracteres correctos.
- Canal adyacente a 36 kHz: sin efecto con SIR de 12.0 y 8.4 dB; con 4.0 dB destruyó la constelación.
- La amplitud digital no mejora la SNR (escala señal y ruido por igual).
- El pico DC no limita la calidad mientras quede fuera de ±21.6 kHz.
- Conclusión: la **SNR fijada por la primera etapa del receptor** dominó la calidad del enlace.

---

## 🌿 Flujo de trabajo en Git

```text
main
 └── fase-3                         → rama de integración de la fase
      ├── fase-3/implementacion-sdr → William Camilo (radios, montaje, mediciones)
      ├── fase-3/receptor-sync      → Juan Andres (cadena Rx, decodificador)
      └── fase-3/informe-ieee       → Jarol Nicolas (informe e integración)
```

```bash
git checkout main && git pull
git checkout -b fase-3
git push -u origin fase-3
git checkout -b fase-3/informe-ieee
```

Al cierre: PR de `fase-3` hacia `main` y etiqueta `v3.0-fase3`.

---

## ✅ Entregables y lista de verificación

- [ ] Informe IEEE de la Fase 3.
- [ ] Flujogramas `.grc` de Tx y Rx funcionales.
- [ ] Bloque Python del decodificador de texto.
- [ ] Capturas: analizador de espectro, espectros RF, constelaciones por prueba.
- [ ] Foto del montaje físico.
- [ ] Historial de Git con ramas y *pull requests* aprobados.

---

## ▶️ Cómo ejecutar

**Requisitos:** GNU Radio Companion con `gr-osmosdr`, 2 × HackRF One, Python 3 (`numpy`).

```bash
git clone <URL_DEL_REPOSITORIO>
cd 2026_2_ComII_A1_A1E
git checkout fase-3
hackrf_info                       # obtener los números de serie
# Abrir los .grc: asignar hackrf=<serial> en Sink (Tx) y Source (Rx)
gnuradio-companion Fase_3_Implementacion_Experimental/Entrega_3/flujogramas/
```

> Ajustar nombres de archivos a los que contenga el repositorio.

---

## 📁 Estructura del repositorio

```text
Fase_3_Implementacion_Experimental/
└── Entrega_3/
    ├── flujogramas/     → Tx y Rx (.grc)
    ├── codigo/          → Decodificador de texto (.py)
    ├── figuras/         → Espectros, constelaciones, montaje
    └── informe/         → Informe IEEE (main.tex + sections/)
```
