
import requests

def get_unemployment_summary():
    """Obtiene un resumen muy simple de paro.

    Aquí se podría utilizar la API TEMPUS del INE, pero como los códigos
    de tabla/serie son específicos y dependen del catálogo, dejamos
    el código listo para ampliación y devolvemos mocks compatibles.

    Formato de retorno:
    {
      "last_value": int,
      "series": [v1, v2, ...],  # lista de valores recientes
      "years": [y1, y2, ...]
    }
    """
    # TODO: implementar llamada real al INE cuando se conozcan códigos de serie/tablas
    # Documentación: https://www.ine.es/dynt3/inebase/es/index.htm

    # Mock
    series = [3800, 3720, 3650, 3590, 3520, 3470, 3410, 3380, 3350]
    years = list(range(2017, 2017 + len(series)))
    return {
        "last_value": series[-1],
        "series": series,
        "years": years,
    }
