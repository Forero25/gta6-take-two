"""Anuncios de GTA VI y el día en que el mercado pudo reaccionar (día 0).

Regla: si el anuncio salió antes o durante la sesión, el día 0 es ese día; si salió después del cierre
(16:00 de Nueva York) o en fin de semana, el día 0 es la siguiente sesión.
`confundido` marca los eventos que llegaron junto con un reporte trimestral: su reacción mezcla GTA VI
con el resto de los resultados y no se puede atribuir solo al juego.
"""

EVENTOS = [
    dict(id="confirmacion", fecha="2022-02-04", dia0="2022-02-04", tipo="anuncio", confundido=False,
         es="Rockstar confirma que el próximo GTA está en desarrollo", en="Rockstar confirms the next GTA is in development",
         fuente="https://www.rockstargames.com/newswire (actualización de la comunidad, 4-feb-2022)"),
    dict(id="filtracion", fecha="2022-09-18", dia0="2022-09-19", tipo="filtracion", confundido=False,
         es="Se filtran 90 videos del juego en desarrollo (domingo)", en="90 in-development clips leak (Sunday)",
         fuente="Bloomberg/Reuters, 19-sep-2022"),
    dict(id="anuncio_trailer", fecha="2023-11-08", dia0="2023-11-08", tipo="anuncio", confundido=False,
         es="Rockstar anuncia el primer tráiler para diciembre (antes de la apertura)", en="Rockstar announces the first trailer for December (pre-market)",
         fuente="Rockstar Games en X, 8-nov-2023; el reporte trimestral salió ese día después del cierre, así que entra en el día +1"),
    dict(id="trailer_1", fecha="2023-12-04", dia0="2023-12-05", tipo="trailer", confundido=False,
         es="Tráiler 1, publicado de noche tras filtrarse; fecha: 2025", en="Trailer 1, released at night after a leak; date: 2025",
         fuente="CNBC, 4-dic-2023"),
    dict(id="ventana_otono_2025", fecha="2024-05-16", dia0="2024-05-17", tipo="fecha", confundido=True,
         es="Take-Two acota el lanzamiento a otoño de 2025 (con el reporte anual)", en="Take-Two narrows the launch to fall 2025 (with annual results)",
         fuente="Comunicado de resultados de Take-Two, 16-may-2024, 16:05 ET"),
    dict(id="aplazamiento_1", fecha="2025-05-02", dia0="2025-05-02", tipo="aplazamiento", confundido=False,
         es="Primer aplazamiento: de otoño de 2025 al 26 de mayo de 2026", en="First delay: from fall 2025 to May 26, 2026",
         fuente="Reuters, 2-may-2025 (antes de la apertura)"),
    dict(id="trailer_2", fecha="2025-05-06", dia0="2025-05-06", tipo="trailer", confundido=False,
         es="Tráiler 2, sin aviso previo, durante la sesión", en="Trailer 2, unannounced, during the session",
         fuente="Comunicado de Take-Two, 6-may-2025"),
    dict(id="aplazamiento_2", fecha="2025-11-06", dia0="2025-11-07", tipo="aplazamiento", confundido=True,
         es="Segundo aplazamiento: al 19 de noviembre de 2026 (con el reporte trimestral)", en="Second delay: to November 19, 2026 (with quarterly results)",
         fuente="Comunicado de resultados de Take-Two, 6-nov-2025, después del cierre"),
    dict(id="fecha_confirmada", fecha="2026-05-21", dia0="2026-05-22", tipo="fecha", confundido=True,
         es="Take-Two confirma el 19 de noviembre (con el reporte anual)", en="Take-Two confirms November 19 (with annual results)",
         fuente="Comunicado de resultados de Take-Two, 21-may-2026, después del cierre"),
    dict(id="preventa", fecha="2026-06-18", dia0="2026-06-18", tipo="anuncio", confundido=False,
         es="Rockstar anuncia la preventa para el 25 de junio", en="Rockstar announces pre-orders for June 25",
         fuente="Anuncio de Rockstar, 18-jun-2026"),
    dict(id="lanzamiento", fecha="2026-11-19", dia0="2026-11-19", tipo="lanzamiento", confundido=False,
         es="Lanzamiento de GTA VI", en="GTA VI launches",
         fuente="Rockstar Games"),
]
