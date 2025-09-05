from src.grid.model import CityModel

if __name__ == "__main__":
    # Simulation initialisieren
    market_fraction = 0.1
    house_fraction = 0.3
    work_fraction = 0.3
    hours = 48
    seed = 42

    testModel = CityModel(width=5, height=5, n_agents=7,
                      park_fraction=0.289, seed=seed)

    #model_N1_goodQ = CityModel(5, 5, 132, 0.289, market_fraction=market_fraction, house_fraction=house_fraction, work_fraction=work_fraction, seed=seed)
    #model_N2_badQ = CityModel(6, 5, 144, 0.247, market_fraction=market_fraction, house_fraction=house_fraction, work_fraction=work_fraction, seed=seed)

    #Aktuelles Model
    model = testModel

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
    for hour in range(hours):
        print(f"\n--- Simulationsschritt {hour+1} -> {(hour+1)%24}:00Uhr ---")
        model.step()
    model_df = model.datacollector.get_model_vars_dataframe()
    agent_df = model.datacollector.get_agent_vars_dataframe()
    model_df.to_csv("model_log.csv")
    agent_df.to_csv("agent_log.csv")
