from src.grid.model import CityModel

if __name__ == "__main__":
    # Simulation initialisieren
    width = 6
    height = 6
    n_agents = 10
    park_fraction = 0.1
    seed = 42

    model = CityModel(width=width, height=height, n_agents=n_agents,
                      park_fraction=park_fraction, seed=seed)

    # Test: alle Agenten initial positionieren
    print(f"Anzahl Knoten im Graph: {len(model.road.graph.nodes())}")
    print(f"Anzahl Häuser: {model.homes}")
    print(f"Anzahl Workplaces: {model.workplaces}")
    print(f"Anzahl Parks: {model.parks}")
    print(f"Supermärkte: {model.supermarkets}")
    print(f"Agenten im Modell: {len(model.schedule.agents)}")
    print("Startpositionen der Agenten:")
    for agent in model.schedule.agents:
        print(f"Agent {agent.unique_id} startet bei Knoten {agent.pos}")
    #print(f"NX-Graph: {model.road.sparse}")
    # Simulation für ein paar Schritte laufen lassen

    steps = 5
    for step in range(steps):
        print(f"\n--- Simulationsschritt {step+1} ---")
        model.step()
        for agent in model.schedule.agents:
            print(f"Agent {agent.unique_id} Position: {agent.pos}, Ziel: {agent.current_goal}")

