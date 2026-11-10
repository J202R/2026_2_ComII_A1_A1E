<div align="center">

<img src="https://img.shields.io/badge/UIS-Universidad%20Industrial%20de%20Santander-1B5E20?style=for-the-badge" alt="UIS"/>

# ✅ Proyecto Integrador — Fase 4. Validación Final

### Comunicaciones II (27145) — Grupo A1-E
**Escuela de Ingenierías Eléctrica, Electrónica y de Telecomunicaciones**

<img src="https://img.shields.io/badge/Rama-Fase__4-2ea44f?style=flat-square" />
<img src="https://img.shields.io/badge/Modulación-16--QAM-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Métricas-BER%20%7C%20SER-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/Hardware-HackRF%20One-orange?style=flat-square" />
<img src="https://img.shields.io/badge/status-Validación%20final-success?style=flat-square" />

</div>

> 📌 Esta rama corresponde a la **Fase 4 (documento consolidado)**. Se instrumenta el receptor SDR para medir automáticamente curvas **BER y SER vs. Eb/N0**, se comparan con la teoría y se consolida todo el proyecto (Fases 1–4) en un único informe IEEE de máximo 6 páginas.

---

## 📑 Tabla de contenido

- [Integrantes y roles](#-integrantes-y-roles)
- [Contexto](#-contexto)
- [Objetivos de la Fase 4](#-objetivos-de-la-fase-4)
- [Método de medición](#-método-de-medición)
- [Resultados principales](#-resultados-principales)
- [Flujo de trabajo en Git](#-flujo-de-trabajo-en-git)
- [Entregables y lista de verificación](#-entregables-y-lista-de-verificación)
- [Cómo ejecutar](#-cómo-ejecutar)
- [Estructura del repositorio](#-estructura-del-repositorio)

---

## 👥 Integrantes y roles

| Integrante | Código | Rol | Responsabilidades en la Fase 4 |
|---|---|---|---|
| **Jarol Nicolas Molano Lopez** | `2230391` | **Líder de Proyecto y Gestor de Git** | Integra el informe consolidado y cierra el repositorio. |
| **Juan Andres Rojas Rueda** | `2231065` | **Encargado de Modelado y Simulación** | Bloques Python de barrido (`e_EbN0_Sweep`), curvas BER/SER y comparación con la teoría. |
| **William Camilo Motta Chacón** | `2234639` | **Encargado de SDR y Canal** | Operación del enlace físico, ejecución de los barridos y captura de datos. |

---

## 📖 Contexto

Las Fases 1–3 definieron la aplicación (DCI), simularon el enlace y lo implementaron en dos HackRF One. La Fase 4 valida cuantitativamente ese enlace: ¿cuánto se acerca el receptor real a la curva teórica 16-QAM con mapeo Gray?

---

## 🎯 Objetivos de la Fase 4

1. Inyectar ruido AWGN calibrado en el receptor físico, en el punto de decisión.
2. Medir automáticamente BER y SER vs. Eb/N0 (0–14 dB) y compararlas con la teoría.
3. Identificar los límites del método (piso de error del enlace).
4. Consolidar las cuatro fases en un informe final.

---

## 🔬 Método de medición

Cadena Rx: `osmocom Source → lo_offset → ÷32 → AGC → FLL → RRC → Gardner → Costas(4) → AGC → e_EbN0_Sweep → decisores → e_BER_Curve / e_SER_Curve → CSV`

Potencia de ruido inyectada (1 muestra por símbolo, `Ps = 10`):

`Pn = max( Ps·fs / (Rb·Eb/N0) − Pn_real , 0 )`

donde `Pn_real` es el ruido ya presente en el enlace (error cuadrático medio al punto de constelación más cercano, con promedio móvil exponencial). `e_Ref_Tx_Alineada` reconstruye la referencia Tx por correlación (`delay_bits = 0`).

| Parámetro | Valor |
|---|---|
| Barrido | 0–14 dB, paso 1 dB (15 puntos) |
| Bits por punto | 100 000 (+1 000 de guarda) |
| Barridos | 10; el 1.º se descarta, mediana de los barridos 2–10 |
| Frecuencia en el flujograma | 860.6 MHz |

---

## 📊 Resultados principales

| Eb/N0 para BER de | 10⁻² | 10⁻³ | 10⁻⁴ |
|---|:-:|:-:|:-:|
| Teoría (Gray) [dB] | 7.87 | 10.50 | 12.19 |
| **HackRF One, medido [dB]** | **7.51** | **10.73** | **12.34** |
| Desviación [dB] | −0.36 | +0.23 | +0.15 |

- La curva medida sigue la teoría con Gray en todo el rango; la SER se comporta igual.
- Sobre ~12 dB aparece un **piso de error de 4×10⁻⁵ a 9×10⁻⁵** (Es/N0 intrínseco ≈ 18–19 dB): no se puede emular una SNR mayor que la del propio enlace.
- Fases previas: Gray ahorra 0.57 dB; un canal vecino a 36 kHz (SIR 0 dB) cuesta 2.31 dB; LNA = 32 dB / VGA = 4 dB recuperó los 16 grupos.

---

## 🌿 Flujo de trabajo en Git

```text
main
 └── fase-4                          → rama de integración de la fase
      ├── fase-4/barrido-ber-ser     → Juan Andres (bloques Python, curvas)
      ├── fase-4/mediciones-sdr      → William Camilo (barridos y datos)
      └── fase-4/informe-final       → Jarol Nicolas (informe consolidado)
```

```bash
git checkout main && git pull
git checkout -b fase-4
git push -u origin fase-4
git checkout -b fase-4/informe-final
```

Al cierre: PR de `fase-4` hacia `main` y etiqueta `v4.0-fase4`.

---

## ✅ Entregables y lista de verificación

- [ ] Informe IEEE consolidado (≤ 6 páginas).
- [ ] Flujograma `.grc` del receptor con bloques de barrido.
- [ ] Bloques Python: `e_EbN0_Sweep`, `e_Ref_Tx_Alineada`, `e_BER_Curve`, `e_SER_Curve`.
- [ ] CSV de los 10 barridos y figuras BER, SER y barridos individuales.
- [ ] Historial de Git con ramas y *pull requests* aprobados.

---

## ▶️ Cómo ejecutar

```bash
git clone <URL_DEL_REPOSITORIO>
cd 2026_2_ComII_A1_A1E
git checkout fase-4
gnuradio-companion Fase_4_Validacion_Final/Documentacion_Tecnica/flujogramas/
# Ejecutar el barrido; los resultados quedan en curva_BER.csv y curva_SER.csv
```

> Ajustar nombres de archivos a los que contenga el repositorio.

---

## 📁 Estructura del repositorio

```text
Fase_4_Validacion_Final/
└── Documentacion_Tecnica/
    ├── flujogramas/     → Receptor con barrido (.grc)
    ├── codigo/          → Bloques Python del barrido
    ├── datos/           → CSV de BER/SER
    ├── figuras/         → Curvas y flujograma
    └── informe/         → Informe consolidado (main.tex + figs/)
```
