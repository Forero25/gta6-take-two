"""Descarga precios ajustados, corre el estudio y guarda solo resultados derivados.

Los precios vienen de Yahoo Finance (vía yfinance) y no se guardan en el repositorio:
se publican únicamente retornos anormales y estadísticas.
"""
import json, os, sys
from datetime import date, timedelta
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from eventos import EVENTOS
from estudio import estudio, retornos

TICKERS = ["TTWO", "QQQ", "ESPO", "EA"]   # acción, Nasdaq-100, ETF de videojuegos, par más cercano
INICIO = "2020-06-01"


def descargar():
    import time
    import yfinance as yf
    fin = (date.today() + timedelta(days=1)).isoformat()
    series = {}
    for t in TICKERS:  # uno por uno: la descarga en paralelo de yfinance falla con "database is locked"
        for intento in range(3):
            d = yf.download(t, start=INICIO, end=fin, auto_adjust=True, progress=False, threads=False)
            if len(d):
                series[t] = d["Close"].squeeze()
                break
            time.sleep(5)
        else:
            raise SystemExit(f"No se pudo descargar {t}")
    df = pd.DataFrame(series).dropna()
    if len(df) < 1000:
        raise SystemExit(f"Muy pocas sesiones: {len(df)}")
    acciones = yf.Ticker("TTWO").get_shares_full(start=INICIO, end=fin)
    return df, acciones


def main():
    precios, acciones = descargar()
    r = retornos(precios)
    base = estudio(r, EVENTOS, "TTWO", "QQQ")
    sector = estudio(r, EVENTOS, "TTWO", "ESPO")
    placebo = estudio(r, EVENTOS, "EA", "QQQ")   # EA no debería reaccionar a GTA VI
    acciones = acciones.sort_index()
    acciones.index = pd.to_datetime(acciones.index).tz_localize(None).normalize()
    salida = {"ultimo_dato": str(r.index[-1].date()), "tickers": TICKERS, "eventos": []}
    for e in EVENTOS:
        b = base[e["id"]]
        fila = {**e, "mercado": b, "sector": sector[e["id"]], "placebo_ea": placebo[e["id"]]}
        if b and b["0_1"]:
            d = pd.Timestamp(b["dia0_efectivo"])
            prev = precios.index[precios.index < d][-1]
            n = acciones[acciones.index <= d]
            if len(n):
                cap = float(precios.loc[prev, "TTWO"]) * float(n.iloc[-1])
                fila["capitalizacion_previa_musd"] = cap / 1e6
                fila["valor_raa_0_1_musd"] = cap * b["0_1"]["raa"] / 1e6
        salida["eventos"].append(fila)
    # resumen por tipo, solo eventos limpios y con ventana completa
    limpios = [f for f in salida["eventos"] if not f["confundido"] and f["mercado"] and f["mercado"]["0_1"]]
    salida["promedios"] = {}
    for t in sorted({f["tipo"] for f in limpios}):
        v = [f["mercado"]["0_1"]["raa"] for f in limpios if f["tipo"] == t]
        salida["promedios"][t] = {"n": len(v), "raa_0_1_promedio": float(np.mean(v))}
    salida["volatilidad_diaria_normal"] = float(np.median([f["mercado"]["sigma"] for f in salida["eventos"] if f["mercado"]]))
    os.makedirs("resultados", exist_ok=True)
    json.dump(salida, open("resultados/estudio_eventos.json", "w"), ensure_ascii=False, indent=1)
    for f in salida["eventos"]:
        m = f["mercado"]
        if m:
            w = m["0_1"]
            print(f"{f['id']:20s} d0={m['dia0_efectivo']} RA0={m['d0']['raa']*100:6.2f}% t={m['d0']['t']:6.2f} "
                  f"RAA[0,1]={(w['raa']*100 if w else float('nan')):6.2f}% pct={m['percentil_abs']:.3f}")


if __name__ == "__main__":
    main()
