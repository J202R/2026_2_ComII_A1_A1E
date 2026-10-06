# Fase 2 – Simulación en Python: BER vs SNR (16-QAM)

Complementa los flujogramas de GNU Radio (`Modulaciones_basadas_en_constelaciones*.grc`).
Reproduce la misma cadena (Rs = 32 kBd, Sps = 8, tabla 16-QAM del laboratorio) y agrega
lo que el flujograma no tiene: filtro RRC (β = 0.35), filtro acoplado, detector y conteo de errores.

## Contenido
| Carpeta | Qué hay |
|---|---|
| `codigo/simulacion_16qam_ber.py` | Script de la simulación |
| `codigo/resultados.json` | Resultados numéricos (BER, SNR por `noise_amp`, Eb/N0 para BER = 1e-4) |
| `figuras/` | Figuras generadas por el script (BER, PSD, ojo, constelaciones, mapeo) |
| `informe/` | Informe IEEE de la Fase 2 (`.tex`, `.bib` y PDF) |

## Qué calcula
1. SNR equivalente a cada `noise_amp` usado en GNU Radio (0.10, 0.25, 0.32, 0.40, 0.50).
2. BER vs Eb/N0 en AWGN: tabla del laboratorio (binario) vs codificación Gray.
3. BER con interferencia de canal adyacente 16-QAM (Δf = 36 kHz, SIR = 0 dB), que modela la diafonía DWDM de la Fase 1.
4. Figuras de PSD, diagrama de ojo y constelación a la salida del filtro acoplado.

## Cómo ejecutarlo
```bash
pip install numpy scipy matplotlib
cd codigo
python3 simulacion_16qam_ber.py
```
Tarda ~1.5 min. Las figuras se guardan en `figuras/` y los números en `codigo/resultados.json`.

## Codificación Gray
El flujograma usa los bits como índice en binario de `tabla_de_verdad_constelacion`, por lo que la
asignación efectiva no es Gray. Para que lo sea sin agregar bloques, se usa esta tabla:
```
(-3-3j, -1-3j, 3-3j, 1-3j, -3-1j, -1-1j, 3-1j, 1-1j, -3+3j, -1+3j, 3+3j, 1+3j, -3+1j, -1+1j, 3+1j, 1+1j)
```
