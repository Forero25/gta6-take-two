"""Estudio de eventos con modelo de mercado (MacKinlay, 1997).

Para cada evento:
- ventana de estimación: 250 sesiones que terminan 21 sesiones antes del día 0, sin los días ±5 de otros eventos;
- modelo: r_TTWO = a + b · r_mercado + e, por mínimos cuadrados;
- retorno anormal (RA) = retorno observado − retorno predicho;
- RA acumulado (RAA) en [0, 1], [-1, 1] y [0, 5];
- prueba t con la desviación de los residuos de la estimación;
- percentil: qué tan raro es |RA del día 0| frente a los días normales de la ventana de estimación.
"""
import numpy as np
import pandas as pd

VENTANAS = {"d0": (0, 0), "0_1": (0, 1), "m1_1": (-1, 1), "0_5": (0, 5)}


def retornos(precios: pd.DataFrame) -> pd.DataFrame:
    return precios.sort_index().pct_change(fill_method=None).iloc[1:]


def ajustar(y, x):
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    sigma = float(np.sqrt(resid @ resid / (len(y) - 2)))
    return float(coef[0]), float(coef[1]), sigma, resid


def un_evento(r: pd.DataFrame, accion: str, mercado: str, dia0: str, excluir=(), n_est=250, hueco=20):
    fechas = r.index
    pos = fechas.searchsorted(pd.Timestamp(dia0))
    if pos >= len(fechas):
        return None
    fin_est = pos - hueco
    ini_est = max(0, fin_est - n_est)
    est = r.iloc[ini_est:fin_est].copy()
    for f in excluir:  # quitar ±5 sesiones alrededor de otros eventos
        p = fechas.searchsorted(pd.Timestamp(f))
        est = est.drop(fechas[max(0, p - 5):p + 6], errors="ignore")
    est = est.dropna(subset=[accion, mercado])
    a, b, sigma, resid = ajustar(est[accion].values, est[mercado].values)
    disponibles = len(fechas) - pos  # sesiones desde el día 0 que ya existen
    out = {"dia0_efectivo": str(fechas[pos].date()), "alfa": a, "beta": b, "sigma": sigma,
           "n_estimacion": int(len(est)), "sesiones_disponibles": int(disponibles)}
    ra = r[accion].iloc[max(0, pos - 1):pos + 6] - (a + b * r[mercado].iloc[max(0, pos - 1):pos + 6])
    out["ra"] = {str(k.date()): float(v) for k, v in ra.items()}
    for nombre, (i, j) in VENTANAS.items():
        if pos + j >= len(fechas):
            out[nombre] = None
            continue
        seg = r.iloc[pos + i:pos + j + 1]
        if seg[[accion, mercado]].isna().any().any():
            out[nombre] = None
            continue
        raa = float((seg[accion] - (a + b * seg[mercado])).sum())
        L = j - i + 1
        out[nombre] = {"raa": raa, "t": raa / (sigma * np.sqrt(L)), "observado": float(seg[accion].sum())}
    if out["d0"] is None:
        return None
    ra0 = out["d0"]["raa"]
    out["percentil_abs"] = float((np.abs(resid) < abs(ra0)).mean())
    return out


def estudio(r, eventos, accion="TTWO", mercado="QQQ"):
    res = {}
    for e in eventos:
        otros = [x["dia0"] for x in eventos if x["id"] != e["id"]]
        res[e["id"]] = un_evento(r, accion, mercado, e["dia0"], excluir=otros)
    return res
