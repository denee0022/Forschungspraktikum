from model import CityModel
from app import CityApp

if __name__ == "__main__":
    #model = CityModel(population=5)
    #model.step()
    app = CityApp(5)
    page = app.show()
