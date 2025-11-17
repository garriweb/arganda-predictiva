
import datetime

def get_dgt_incidents():
    """Devuelve un pequeño resumen de incidencias de tráfico.

    Aquí podrías:
    - Descargar el feed DATEX2 de la DGT desde el NAP
    - Filtrar por el área geográfica de Arganda
    - Contar incidencias de hoy, semana, tipos, etc.

    De momento devolvemos valores simulados.
    """
    today = datetime.date.today()
    # valores mock
    return {
        "today_date": today.isoformat(),
        "today_count": 4,
        "week_avg": 5.2
    }
