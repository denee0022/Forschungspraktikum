from src.grid.model import CityModel

if __name__ == "__main__":
    # Simulation initialisieren
    market_fraction = 0.1
    house_fraction = 0.3
    work_fraction = 0.3
    hours = 168
    seed = 42

    #testModel = CityModel(width=5, height=5, n_agents=7,
                     # park_fraction=0.289, seed=seed)

    #model_N1_badQ = CityModel(5, 5, 132, 0.289, 0.46,0.05, 0.49, market_fraction=market_fraction, house_fraction=house_fraction, work_fraction=work_fraction, seed=seed)
    model_N2_goodQ = CityModel(6, 5, 144, 0.247,  0.75, 0.2, 0.05, market_fraction=market_fraction, house_fraction=house_fraction, work_fraction=work_fraction, seed=seed)

    #Aktuelles Model
    model = model_N2_goodQ

    # Test: alle Agenten initial positionieren
    print("Aufbau des Experiments:")
    print(f"Anzahl Knoten im Graph: {len(model.road.graph.nodes())}")
    print(f"Anzahl Häuser: {model.homes}")
    print(f"Anzahl Workplaces: {model.workplaces}")
    print(f"Anzahl Parks: {model.parks}")
    print(f"Anzahl gute Parks: {model.parks_good}")
    print(f"Anzahl mittelmäßige Parks:  {model.parks_medium}")
    print(f"Anzahl schlechte Parks:  {model.parks_bad}")
    print(f"Supermärkte: {model.supermarkets}")
    print(f"Agenten im Modell: {len(model.schedule.agents)}")
    print("Startpositionen der Agenten:")
    for agent in model.schedule.agents:
        print(f"Agent {agent.unique_id} startet bei Knoten {agent.pos}")
        agent.show_tanks()
        #agent.preferences.show_preferences()
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
    for agent in model.schedule.agents:
        print(f"Agent {agent.unique_id} startet bei Knoten {agent.pos}")
        agent.quality_of_life()
        print(f"Agent quality of life: {agent.life_quality}")
    model.get_average_Qlife()
    print(f"Average model quality of life: {model.average_Qlife}")

