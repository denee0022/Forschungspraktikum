from src.grid.model import CityModel

if __name__ == "__main__":
    # Simulation initialisieren
    width = 5
    height = 5
    n_agents = 4
    park_fraction = 0.289
    seed = 42

    model = CityModel(width=width, height=height, n_agents=n_agents,
                      park_fraction=park_fraction, seed=seed)

    # Test: alle Agenten initial positionieren
    print("Aufbau des Experiments:")
    print(f"Anzahl Knoten im Graph: {len(model.road.graph.nodes())}")
    print(f"Anzahl Häuser: {model.homes}")
    print(f"Anzahl Workplaces: {model.workplaces}")
    print(f"Anzahl Parks: {model.parks}")
    print(f"Supermärkte: {model.supermarkets}")
    print(f"Agenten im Modell: {len(model.schedule.agents)}")
    print("Startpositionen der Agenten:")
    for agent in model.schedule.agents:
        print(f"Agent {agent.unique_id} startet bei Knoten {agent.pos}")
    print("______________________________________________________________________")
    #print(f"NX-Graph: {model.road.sparse}")

    # Simulation für ein paar Schritte laufen lassen
    steps = 48
    for step in range(steps):
        print(f"\n--- Simulationsschritt {step} -> {(step+1)%24}:00Uhr ---")
        model.step()
    model_df = model.datacollector.get_model_vars_dataframe()
    agent_df = model.datacollector.get_agent_vars_dataframe()
    model_df.to_csv("model_log.csv")
    agent_df.to_csv("agent_log.csv")
