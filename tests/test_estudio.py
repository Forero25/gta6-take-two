import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from estudio import un_evento, ajustar
from eventos import EVENTOS


def serie(n=400, beta=1.3, choque=0.10, dia=350, semilla=1):
    rng = np.random.default_rng(semilla)
    fechas = pd.bdate_range("2023-01-02", periods=n)
    m = rng.normal(0, 0.01, n)
    a = 0.0002 + beta * m + rng.normal(0, 0.012, n)
    a[dia] += choque
    return pd.DataFrame({"TTWO": a, "QQQ": m}, index=fechas), fechas[dia]


def test_recupera_beta():
    r, _ = serie()
    a, b, s, _ = ajustar(r.TTWO.values, r.QQQ.values)
    assert abs(b - 1.3) < 0.15 and abs(s - 0.012) < 0.002


def test_detecta_el_choque_y_lo_marca_como_raro():
    r, d = serie(choque=0.10)
    out = un_evento(r, "TTWO", "QQQ", str(d.date()))
    assert abs(out["d0"]["raa"] - 0.10) < 0.03
    assert out["d0"]["t"] > 5 and out["percentil_abs"] > 0.99


def test_sin_choque_no_hay_efecto():
    r, d = serie(choque=0.0, semilla=3)
    out = un_evento(r, "TTWO", "QQQ", str(d.date()))
    assert abs(out["d0"]["t"]) < 3


def test_ventana_incompleta_queda_vacia():
    r, _ = serie(n=400)
    out = un_evento(r, "TTWO", "QQQ", str(r.index[-1].date()))
    assert out["d0"] is not None and out["0_5"] is None


def test_eventos_bien_formados():
    ids = [e["id"] for e in EVENTOS]
    assert len(ids) == len(set(ids))
    for e in EVENTOS:
        assert e["dia0"] >= e["fecha"] and pd.Timestamp(e["dia0"]).dayofweek < 5
