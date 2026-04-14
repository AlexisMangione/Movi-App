import random

def init_buses():
    """Inicializa una lista de colectivos en Rosario."""
    lat, lon = -32.9442, -60.6505
    return [
        {
            "id": i + 1,
            "lat": lat + random.uniform(-0.015, 0.015),
            "lon": lon + random.uniform(-0.015, 0.015)
        } for i in range(8)
    ]

def move_buses(buses):
    """Simula el movimiento de los buses."""
    for b in buses:
        b["lat"] += random.uniform(-0.0006, 0.0006)
        b["lon"] += random.uniform(-0.0006, 0.0006)
    return buses
  
