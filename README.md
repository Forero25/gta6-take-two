# ¿Cuánto vale un anuncio de GTA VI en la bolsa?

GTA VI no cotiza en bolsa: cotiza Take-Two Interactive (TTWO, Nasdaq), dueña de Rockstar Games. Este repositorio mide cómo reaccionó la acción a cada anuncio del juego, desde que se confirmó su desarrollo (febrero de 2022) hasta su lanzamiento (19 de noviembre de 2026), separando el anuncio del movimiento normal del mercado.

## Método

Estudio de eventos con modelo de mercado (MacKinlay, 1997):

1. **Eventos** (`src/eventos.py`): 11 anuncios con fecha, hora y fuente. El día 0 es la primera sesión en la que el mercado pudo reaccionar.
2. **Retorno normal:** regresión del retorno de TTWO sobre el del Nasdaq-100 (QQQ) en 250 sesiones que terminan 21 sesiones antes del día 0, sin los días cercanos a otros anuncios.
3. **Retorno anormal:** lo observado menos lo que el modelo esperaba ese día; se acumula en ventanas de [0, 1], [-1, 1] y [0, 5] sesiones.
4. **Pruebas:** estadístico t con la volatilidad de los residuos, y percentil del movimiento frente a los días normales.
5. **Robustez:** el mismo cálculo contra el ETF de videojuegos ESPO, y un placebo con Roblox (RBLX), una acción de videojuegos que no debería reaccionar a GTA VI. Electronic Arts no sirve de placebo: su compra se anunció en septiembre de 2025 y dejó de cotizar en agosto de 2026.

El flujo de GitHub Actions corre cada día hábil después del cierre de Nueva York, así que el evento del lanzamiento se completa solo a medida que pasan las sesiones.

## Lo que este proyecto no hace

- **No atribuye todo al juego en los eventos "confundidos".** Tres anuncios llegaron junto con un reporte trimestral; su reacción mezcla GTA VI con el resto de los resultados y se reporta aparte.
- **No es una recomendación de inversión.** Describe reacciones pasadas; no pronostica el precio.
- **No publica precios.** Los precios ajustados se descargan de Yahoo Finance en cada corrida y no se guardan; el repositorio solo contiene retornos anormales y estadísticas.
- **No mide ventas del juego.** Take-Two las reportará en su próximo informe trimestral.

## Reproducir

```
pip install -r requirements.txt
pytest
python src/correr.py
```

Código bajo licencia MIT.
