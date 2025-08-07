from mesa.visualization import SolaraViz, make_space_component
from model import CityModel
import solara


def agent_portrayal(agent):
    if hasattr(agent, "current_activity"):
        return {
            "shape": "circle",
            "color": "red",
            "r": 3,
            "tooltip": f"Citizen at {agent.pos}"
        }
    else:
        return {
            "shape": "rect",
            "color": "green",
            "w": 2,
            "h": 2,
            "tooltip": f"{agent.kind} at {agent.pos}"
        }


class CityApp:
    def __init__(self, population):
        # Modellinstanz erzeugen
        model_instance = CityModel(population)

        canvas = make_space_component(
            portrayal_method=agent_portrayal,
            width=500,
            height=500
        )

        # SolaraViz mit Modellinstanz und Komponenten erzeugen
        self.viz = SolaraViz(
            model=model_instance,
            components=[canvas],
            model_params={"population": population},  # <--- hier alle erforderlichen Parameter angeben
            name="Urban Model",
        )

    def show(self):
        return self.viz
