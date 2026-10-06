#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fase 2 - Modelado y simulación de un enlace 16-QAM (Comunicaciones II, grupo A1-E)

Este script complementa los flujogramas de GNU Radio
(Modulaciones_basadas_en_constelaciones*.grc) y reproduce la misma cadena
de transmisión (Rs = 32 kBd, Sps = 8, tabla 16-QAM del laboratorio) para:

  1. Relacionar el parámetro noise_amp del bloque Noise Source con la SNR.
  2. Obtener curvas BER vs Eb/N0 en canal AWGN (mapeo del laboratorio vs Gray).
  3. Incorporar el filtrado RRC (transmisor y filtro acoplado en el receptor).
  4. Modelar interferencia controlada: diafonía
     de un canal adyacente 16-QAM (análogo a la diafonía entre canales DWDM).
  5. Generar PSD, diagramas de ojo y constelaciones para el informe.

Uso:  python3 simulacion_16qam_ber.py        (genera figs/*.pdf y resultados.json)
"""
import json
import os

import numpy as np
from scipy.signal import fftconvolve, welch
from scipy.special import erfc
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Parámetros del sistema (iguales a los del flujograma GRC)
# ---------------------------------------------------------------------------
Rs = 32_000            # tasa de símbolos [Bd]
Sps = 8                # muestras por símbolo
fs = Rs * Sps          # samp_rate = 256 kHz
M = 16
bps = int(np.log2(M))  # 4 bits/símbolo
Rb = Rs * bps          # 128 kb/s
beta = 0.35            # roll-off del filtro RRC
span = 10              # duración del filtro RRC en símbolos

# Tabla de verdad usada en el GRC (orden en serpentina, NO es Gray)
TABLA_LAB = np.array([-3-3j, -1-3j, 1-3j, 3-3j, 3-1j, 1-1j, -1-1j, -3-1j,
                      -3+1j, -1+1j, 1+1j, 3+1j, 3+3j, 1+3j, -1+3j, -3+3j])

# Tabla con codificación Gray: b3b2 -> I, b1b0 -> Q (00,01,11,10 -> -3,-1,1,3)
_g = {0b00: -3, 0b01: -1, 0b11: 1, 0b10: 3}
TABLA_GRAY = np.array([_g[k >> 2] + 1j * _g[k & 3] for k in range(M)])

ES = np.mean(np.abs(TABLA_LAB) ** 2)   # energía media por símbolo = 10

OUT_FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figuras")
os.makedirs(OUT_FIG, exist_ok=True)
rng = np.random.default_rng(2026)

plt.rcParams.update({
    "font.family": "serif", "font.size": 8, "axes.titlesize": 8,
    "axes.labelsize": 8, "legend.fontsize": 7, "xtick.labelsize": 7,
    "ytick.labelsize": 7, "lines.linewidth": 1.0, "axes.grid": True,
    "grid.alpha": 0.3, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
COL_W = 3.5  # ancho de columna IEEE [in]


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def rrc(beta, sps, span):
    """Respuesta al impulso de un filtro raíz de coseno alzado (energía unitaria)."""
    t = np.arange(-span * sps / 2, span * sps / 2 + 1) / sps
    h = np.zeros_like(t)
    for i, ti in enumerate(t):
        if np.isclose(ti, 0.0):
            h[i] = 1 - beta + 4 * beta / np.pi
        elif np.isclose(abs(ti), 1 / (4 * beta)):
            h[i] = beta / np.sqrt(2) * ((1 + 2 / np.pi) * np.sin(np.pi / (4 * beta))
                                        + (1 - 2 / np.pi) * np.cos(np.pi / (4 * beta)))
        else:
            h[i] = (np.sin(np.pi * ti * (1 - beta)) + 4 * beta * ti * np.cos(np.pi * ti * (1 + beta))) \
                   / (np.pi * ti * (1 - (4 * beta * ti) ** 2))
    return h / np.sqrt(np.sum(h ** 2))


H_RRC = rrc(beta, Sps, span)
DELAY = len(H_RRC) - 1          # retardo total Tx + Rx (en muestras)


def bits_a_indices(bits):
    """Agrupa 4 bits (MSB primero, como packed_to_unpacked con GR_MSB_FIRST)."""
    b = bits.reshape(-1, bps)
    return b @ (1 << np.arange(bps - 1, -1, -1))


def indices_a_bits(idx):
    return ((idx[:, None] >> np.arange(bps - 1, -1, -1)) & 1).astype(np.uint8).ravel()


def construir_detector(tabla):
    """Detector de mínima distancia para 16-QAM cuadrada: decisión por eje."""
    lut = np.zeros((4, 4), dtype=int)
    for k, s in enumerate(tabla):
        lut[int((s.real + 3) / 2), int((s.imag + 3) / 2)] = k

    def detectar(y):
        iI = np.clip(np.floor((y.real + 4) / 2), 0, 3).astype(int)
        iQ = np.clip(np.floor((y.imag + 4) / 2), 0, 3).astype(int)
        return lut[iI, iQ]
    return detectar


def tx_rrc(simbolos):
    up = np.zeros(len(simbolos) * Sps, dtype=complex)
    up[::Sps] = simbolos
    return fftconvolve(up, H_RRC)


def rx_rrc(r, n_sim):
    y = fftconvolve(r, H_RRC)
    return y[DELAY: DELAY + n_sim * Sps: Sps]       # muestreo en el instante óptimo


def awgn(n, sigma2, rng):
    """Ruido complejo de potencia total sigma2 (sigma2/2 por componente),
    igual que el bloque Noise Source complejo de GNU Radio con amplitud sqrt(sigma2)."""
    return np.sqrt(sigma2 / 2) * (rng.standard_normal(n) + 1j * rng.standard_normal(n))


def ber_teorica_gray(ebn0_db):
    g = 10 ** (np.asarray(ebn0_db) / 10)
    return 3 / 8 * erfc(np.sqrt(0.4 * g))


def ser_teorica(esn0_db):
    g = 10 ** (np.asarray(esn0_db) / 10)
    p = 0.75 * erfc(np.sqrt(g / 10))       # 2(1-1/sqrt(M)) Q(sqrt(3 Es/((M-1) N0)))
    return 1 - (1 - p) ** 2


def interferencia_canal_adyacente(n_sim, p_i, df, p_s):
    """Señal 16-QAM independiente desplazada df Hz (diafonía de canal vecino)."""
    s_int = TABLA_GRAY[rng.integers(0, M, n_sim + 2 * span)]
    x_int = tx_rrc(s_int)[: n_sim * Sps + len(H_RRC) - 1]
    t = np.arange(len(x_int)) / fs
    return np.sqrt(p_i / p_s) * x_int * np.exp(1j * 2 * np.pi * df * t)


# Potencia media por muestra de la señal RRC transmitida
P_TX_RRC = ES / Sps


def simular_rrc(ebn0_db, tabla, n_sim, interf=None, sir_db=None, f_or_df=None,
                devolver_muestras=False):
    """Cadena completa: bits -> mapeo -> RRC -> canal (AWGN + interferencia) -> RRC -> decisión."""
    bits = rng.integers(0, 2, n_sim * bps).astype(np.uint8)
    idx = bits_a_indices(bits)
    x = tx_rrc(tabla[idx])
    esn0 = 10 ** ((ebn0_db + 10 * np.log10(bps)) / 10)
    sigma2 = ES / esn0 / 1.0          # varianza por muestra antes del filtro acoplado
    # Con filtro de energía unitaria la varianza del ruido a la salida del filtro
    # acoplado es sigma2 y la energía de símbolo es ES  ->  Es/N0 = ES / sigma2
    r = x + awgn(len(x), sigma2, rng)
    if interf is not None:
        p_i = P_TX_RRC / 10 ** (sir_db / 10)
        if interf == "adyacente":
            r = r + interferencia_canal_adyacente(n_sim, p_i, f_or_df, P_TX_RRC)
    y = rx_rrc(r, n_sim)
    idx_hat = construir_detector(tabla)(y)
    bits_hat = indices_a_bits(idx_hat)
    ber = np.mean(bits_hat != bits)
    ser = np.mean(idx_hat != idx)
    if devolver_muestras:
        return ber, ser, y, r
    return ber, ser


def simular_grc_rect(noise_amp, tabla, n_sim):
    """Cadena idéntica al GRC del laboratorio (pulso rectangular h=[1]*Sps).
    Devuelve BER decidiendo con UNA muestra por símbolo (lo que muestra el
    Constellation Sink) y con filtro acoplado integrate-and-dump."""
    bits = rng.integers(0, 2, n_sim * bps).astype(np.uint8)
    idx = bits_a_indices(bits)
    x = np.repeat(tabla[idx], Sps)
    r = x + awgn(len(x), noise_amp ** 2, rng)
    det = construir_detector(tabla)
    y_muestra = r[Sps // 2::Sps]
    y_id = r.reshape(-1, Sps).mean(axis=1)
    ber_m = np.mean(indices_a_bits(det(y_muestra)) != bits)
    ber_id = np.mean(indices_a_bits(det(y_id)) != bits)
    return ber_m, ber_id


# ---------------------------------------------------------------------------
# 1) Relación noise_amp -> SNR para las capturas de GNU Radio
# ---------------------------------------------------------------------------
print("== Tabla noise_amp -> SNR (cadena GRC, pulso rectangular) ==")
amps = [0.10, 0.25, 0.32, 0.40, 0.50]
tabla_amp = []
for a in amps:
    snr_m = 10 * np.log10(ES / a ** 2)                 # SNR por muestra
    esn0 = snr_m + 10 * np.log10(Sps)                  # tras filtro acoplado
    ebn0 = esn0 - 10 * np.log10(bps)
    ebn0_m = snr_m - 10 * np.log10(bps)
    ber_m, ber_id = simular_grc_rect(a, TABLA_LAB, 400_000)
    fila = dict(noise_amp=a, snr_muestra_db=round(snr_m, 2), esn0_mf_db=round(esn0, 2),
                ebn0_mf_db=round(ebn0, 2), ebn0_muestra_db=round(ebn0_m, 2),
                ber_sim_una_muestra=ber_m, ber_sim_mf=ber_id,
                ber_teo_gray_una_muestra=float(ber_teorica_gray(ebn0_m)),
                ber_teo_gray_mf=float(ber_teorica_gray(ebn0)))
    tabla_amp.append(fila)
    print(fila)

# ---------------------------------------------------------------------------
# 2) BER vs Eb/N0 en AWGN: mapeo del laboratorio vs Gray (cadena RRC)
# ---------------------------------------------------------------------------
print("\n== BER vs Eb/N0 (AWGN, RRC) ==")
ebn0_vec = np.arange(0, 17, 1)
N_SIM = 300_000
res_awgn = {"ebn0": ebn0_vec.tolist(), "teo_gray": ber_teorica_gray(ebn0_vec).tolist(),
            "lab": [], "gray": [], "ser_lab": [], "ser_gray": [],
            "ser_teo": ser_teorica(ebn0_vec + 10 * np.log10(bps)).tolist()}
for e in ebn0_vec:
    n = N_SIM if e < 12 else 3 * N_SIM
    b_l, s_l = simular_rrc(e, TABLA_LAB, n)
    b_g, s_g = simular_rrc(e, TABLA_GRAY, n)
    res_awgn["lab"].append(b_l); res_awgn["gray"].append(b_g)
    res_awgn["ser_lab"].append(s_l); res_awgn["ser_gray"].append(s_g)
    print(f"Eb/N0={e:2d} dB  BER lab={b_l:.3e}  BER gray={b_g:.3e}  teo={ber_teorica_gray(e):.3e}  "
          f"SER lab={s_l:.3e} SER gray={s_g:.3e}")

# ---------------------------------------------------------------------------
# 3) BER vs Eb/N0 con interferencia controlada (mapeo Gray)
# ---------------------------------------------------------------------------
DF_ADY = 36_000         # separación del canal vecino [Hz] (< Rs(1+beta) = 43.2 kHz)
SIR_ADY = 0             # dB (canales vecinos de igual potencia)
print("\n== BER vs Eb/N0 con interferencia ==")
res_int = {"ebn0": ebn0_vec.tolist(), "adyacente": [], "n_bits": []}
for e in ebn0_vec:
    n = N_SIM if e < 12 else 3 * N_SIM
    res_int["n_bits"].append(n * bps)
    res_int["adyacente"].append(simular_rrc(e, TABLA_GRAY, n, "adyacente", SIR_ADY, DF_ADY)[0])
    print(f"Eb/N0={e:2d} dB  "
          f"ady={res_int['adyacente'][-1]:.3e}")


# Penalización en Eb/N0 para BER = 1e-4 (interpolación log-lineal)
def ebn0_para_ber(ebn0, ber, objetivo=1e-4):
    ber = np.asarray(ber, float); ebn0 = np.asarray(ebn0, float)
    for k in range(len(ber) - 1):
        if ber[k] >= objetivo > ber[k + 1] and ber[k + 1] > 0:
            l0, l1 = np.log10(ber[k]), np.log10(ber[k + 1])
            return float(ebn0[k] + (np.log10(objetivo) - l0) / (l1 - l0))
    return None


ref = {k: ebn0_para_ber(ebn0_vec, v) for k, v in
       [("teo_gray", res_awgn["teo_gray"]), ("gray", res_awgn["gray"]), ("lab", res_awgn["lab"]),
        ("adyacente", res_int["adyacente"])]}
print("\nEb/N0 requerido para BER=1e-4:", ref)

# ---------------------------------------------------------------------------
# 4) Figuras
# ---------------------------------------------------------------------------
NB = np.array([(N_SIM if e < 12 else 3 * N_SIM) * bps for e in ebn0_vec])


def _nz(v):
    """Oculta puntos con menos de 10 errores (estimación poco confiable)."""
    v = np.asarray(v, float)
    return np.where(v * NB >= 10, v, np.nan)


# 4a) BER AWGN
fig, ax = plt.subplots(figsize=(COL_W, 2.5))
ax.semilogy(ebn0_vec, res_awgn["teo_gray"], "k-", label="Teórica (Gray)")
ax.semilogy(ebn0_vec, _nz(res_awgn["gray"]), "o", color="C0", ms=3.5, mfc="none",
            label="Simulada, mapeo Gray")
ax.semilogy(ebn0_vec, _nz(res_awgn["lab"]), "s--", color="C3", ms=3, mfc="none",
            label="Simulada, tabla del laboratorio")
ax.set_xlabel(r"$E_b/N_0$ [dB]"); ax.set_ylabel("BER")
ax.set_ylim(1e-6, 0.5); ax.set_xlim(0, 16)
ax.legend(loc="lower left")
sec = ax.secondary_xaxis("top", functions=(lambda e: e + 10 * np.log10(bps), lambda s: s - 10 * np.log10(bps)))
sec.set_xlabel(r"SNR $= E_s/N_0$ [dB]")
fig.savefig(os.path.join(OUT_FIG, "fig_ber_awgn.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_ber_awgn.png"), dpi=200)
plt.close(fig)

# 4b) BER con interferencia
fig, ax = plt.subplots(figsize=(COL_W, 2.5))
ax.semilogy(ebn0_vec, res_awgn["teo_gray"], "k-", label="Solo AWGN (teórica)")
ax.semilogy(ebn0_vec, _nz(res_int["adyacente"]), "d-", color="C4", ms=3, mfc="none",
            label=fr"AWGN + canal adyacente, $\Delta f$ = {DF_ADY/1e3:.0f} kHz")
ax.set_xlabel(r"$E_b/N_0$ [dB]"); ax.set_ylabel("BER")
ax.set_ylim(1e-6, 0.5); ax.set_xlim(0, 16)
ax.legend(loc="lower left")
sec = ax.secondary_xaxis("top", functions=(lambda e: e + 10 * np.log10(bps), lambda s: s - 10 * np.log10(bps)))
sec.set_xlabel(r"SNR $= E_s/N_0$ [dB]")
fig.savefig(os.path.join(OUT_FIG, "fig_ber_interf.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_ber_interf.png"), dpi=200)
plt.close(fig)

# 4c) PSD de señal, ruido e interferencias
n_psd = 200_000
x = tx_rrc(TABLA_GRAY[rng.integers(0, M, n_psd)])
e_psd = 12
sig2 = ES / 10 ** ((e_psd + 6.02) / 10)
ruido = awgn(len(x), sig2, rng)
ady = interferencia_canal_adyacente(n_psd, P_TX_RRC, DF_ADY, P_TX_RRC)[: len(x)]
fig, ax = plt.subplots(figsize=(COL_W, 2.6))
for sgn, lab, c in [(x, "Señal Tx 16-QAM (RRC)", "C0"), (ruido, rf"AWGN ($E_b/N_0$ = {e_psd} dB)", "0.5"),
                    (ady, rf"Canal adyacente ($\Delta f$ = {DF_ADY/1e3:.0f} kHz)", "C4")]:
    f, P = welch(sgn, fs=fs, nperseg=2048, return_onesided=False, window="blackmanharris", detrend=False)
    f = np.fft.fftshift(f); P = np.fft.fftshift(P)
    ax.plot(f / 1e3, 10 * np.log10(P / np.max(welch(x, fs=fs, nperseg=2048, return_onesided=False,
                                                    window="blackmanharris", detrend=False)[1]) + 1e-15),
            color=c, label=lab, lw=0.9)
ax.axvspan(-Rs * (1 + beta) / 2e3, Rs * (1 + beta) / 2e3, color="C0", alpha=0.07)
ax.set_xlabel("Frecuencia [kHz]"); ax.set_ylabel("PSD relativa [dB]")
ax.set_xlim(-128, 128); ax.set_ylim(-80, 45)
ax.legend(loc="upper center", ncol=2, fontsize=5.8, columnspacing=0.8, handlelength=1.5)
fig.savefig(os.path.join(OUT_FIG, "fig_psd_interf.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_psd_interf.png"), dpi=200)
plt.close(fig)


# 4d) Diagramas de ojo (componente I a la salida del filtro acoplado)
def ojo(ax, r, titulo, n_traz=300):
    y = fftconvolve(r, H_RRC)[DELAY - Sps: DELAY - Sps + (n_traz + 2) * Sps]
    L = 2 * Sps
    t = np.arange(L + 1) / Sps - 1
    for k in range(n_traz):
        seg = y[k * Sps: k * Sps + L + 1]
        if len(seg) == L + 1:
            ax.plot(t, seg.real, color="C0", alpha=0.15, lw=0.5)
    ax.set_title(titulo); ax.set_ylim(-5, 5); ax.set_xlim(-1, 1)
    ax.set_ylabel("Amplitud I")


n_ojo = 2000
s_ojo = TABLA_GRAY[rng.integers(0, M, n_ojo)]
x_ojo = tx_rrc(s_ojo)
sig2_ojo = ES / 10 ** ((14 + 6.02) / 10)
r_ruido = x_ojo + awgn(len(x_ojo), sig2_ojo, rng)
fig, axs = plt.subplots(2, 1, figsize=(COL_W, 3.4), sharex=True)
ojo(axs[0], x_ojo, "(a) Sin ruido")
ojo(axs[1], r_ruido, r"(b) AWGN, $E_b/N_0$ = 14 dB")
axs[-1].set_xlabel(r"$t/T_s$")
fig.tight_layout(h_pad=0.6)
fig.savefig(os.path.join(OUT_FIG, "fig_ojo.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_ojo.png"), dpi=200)
plt.close(fig)

# 4e) Constelaciones a la salida del filtro acoplado
n_c = 3000
casos = [("(a) Tx ideal", None, None, None, 60),
         (r"(b) Rx, $E_b/N_0$ = 14 dB", None, None, None, 14),
         ("(c) Rx + canal adyacente", "adyacente", SIR_ADY, DF_ADY, 14)]
fig, axs = plt.subplots(3, 1, figsize=(1.9, 5.5))
for ax, (tit, it, sir, fpar, e) in zip(axs, casos):
    if e == 60:
        y = TABLA_GRAY[rng.integers(0, M, n_c)]
    else:
        _, _, y, _ = simular_rrc(e, TABLA_GRAY, n_c, it, sir, fpar, devolver_muestras=True)
    ax.plot(y.real, y.imag, ".", ms=1.2, color="C0", alpha=0.6)
    ax.plot(TABLA_GRAY.real, TABLA_GRAY.imag, "r+", ms=4, mew=0.8)
    for v in (-2, 0, 2):
        ax.axvline(v, color="0.6", lw=0.4, ls=":"); ax.axhline(v, color="0.6", lw=0.4, ls=":")
    ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.6, 4.6); ax.set_aspect("equal")
    ax.set_title(tit); ax.set_ylabel("Q")
axs[-1].set_xlabel("I")
fig.tight_layout(h_pad=0.5)
fig.savefig(os.path.join(OUT_FIG, "fig_const_rx.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_const_rx.png"), dpi=200)
plt.close(fig)

# 4f) Mapeo de bits: tabla del laboratorio vs Gray
fig, axs = plt.subplots(2, 1, figsize=(1.9, 3.8))
for ax, tabla, tit in [(axs[0], TABLA_LAB, "(a) Tabla del laboratorio"), (axs[1], TABLA_GRAY, "(b) Codificación Gray")]:
    ax.plot(tabla.real, tabla.imag, "o", color="C0", ms=4)
    for k, s in enumerate(tabla):
        ax.annotate(format(k, "04b"), (s.real, s.imag), textcoords="offset points", xytext=(0, 4.5),
                    ha="center", fontsize=5.5)
    ax.set_xlim(-4, 4); ax.set_ylim(-4, 4.4); ax.set_aspect("equal")
    ax.set_xticks([-3, -1, 1, 3]); ax.set_yticks([-3, -1, 1, 3])
    ax.set_title(tit); ax.set_ylabel("Q")
axs[-1].set_xlabel("I")
fig.tight_layout(h_pad=0.5)
fig.savefig(os.path.join(OUT_FIG, "fig_mapeo.pdf")); fig.savefig(os.path.join(OUT_FIG, "fig_mapeo.png"), dpi=200)
plt.close(fig)

# Bits que cambian entre vecinos (horizontal/vertical) en cada tabla
def bits_vecinos(tabla):
    pos = {(int(s.real), int(s.imag)): k for k, s in enumerate(tabla)}
    d = []
    for (i, q), k in pos.items():
        for di, dq in ((2, 0), (0, 2)):
            if (i + di, q + dq) in pos:
                d.append(bin(k ^ pos[(i + di, q + dq)]).count("1"))
    return float(np.mean(d)), int(max(d))


resultados = dict(parametros=dict(Rs=Rs, Sps=Sps, fs=fs, Rb=Rb, beta=beta, span=span, Es=float(ES),
                                  BW_rrc=Rs * (1 + beta),                                   df_ady=DF_ADY, SIR_ady=SIR_ADY),
                  noise_amp=tabla_amp, awgn=res_awgn, interferencia=res_int, ebn0_ber1e4=ref,
                  bits_vecinos=dict(lab=bits_vecinos(TABLA_LAB), gray=bits_vecinos(TABLA_GRAY)))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados.json"), "w") as fjs:
    json.dump(resultados, fjs, indent=1, default=float)
print("\nBits distintos entre vecinos (media, máx):", resultados["bits_vecinos"])
print("Listo. Figuras en", os.path.abspath(OUT_FIG))
