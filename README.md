
# 🔮 Arganda Predictiva (versión PRO)

Prototipo de **gemelo digital** para Arganda del Rey, pensado para concursos de
datos abiertos. Muestra cómo combinar datos de:

- AEMET (clima)
- DGT (tráfico)
- INE (paro)
- (opcional) Copernicus / satélite

en un panel unificado con:

- estado actual de la ciudad,
- predicción de riesgo de accidentes,
- mapa de riesgo,
- exploración de relaciones paro–tráfico.

## 🚀 Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

Luego abre http://localhost:8501 en tu navegador.

## ☁️ Despliegue en Streamlit Cloud

1. Sube este proyecto a un repositorio de GitHub.
2. Ve a https://share.streamlit.io.
3. Conéctalo con tu cuenta de GitHub.
4. Crea una nueva app:
   - Repo: el tuyo
   - Branch: main
   - File: `app.py`
5. Opcional: configura tu `AEMET_KEY` en la sección de *Secrets* de Streamlit.

## 🔧 Estructura

- `app.py` — aplicación principal de Streamlit.
- `modules/aemet.py` — lógica de integración (simplificada) con AEMET.
- `modules/dgt.py` — punto de entrada para datos DGT (simulado, listo para extender).
- `modules/ine.py` — punto de entrada para datos de paro del INE (simulado, listo para extender).
- `modules/models.py` — lógica de cálculo y predicción.
- `modules/risk_map.py` — generación de mapa de riesgo simulado.
- `.streamlit/secrets.toml` — configuración de claves privadas (AEMET, etc.).

## 🏆 Uso en concursos

Este proyecto está pensado para que puedas:

- enseñar un dashboard funcional,
- explicar una arquitectura modular basada en datos abiertos,
- argumentar el impacto en:
  - seguridad vial,
  - planificación urbana,
  - toma de decisiones basada en evidencia.

Puedes adaptar el texto de tu presentación a partir de este prototipo.
