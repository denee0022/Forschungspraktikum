
class Action:

    def sleeping(self, citizen):
        citizen.tank_mental_health.update(10)
        citizen.tank_physical_health.update(20)
        citizen.tank_leisure.update(-20)
        citizen.tank_social_inclusion.update(-30)
        citizen.tank_self_determination.update(-20)
        citizen.tank_food.update(-20)
    def working(self, citizen):
        citizen.tank_mental_health.update(-30)
        citizen.tank_physical_health.update(-30)
        citizen.tank_leisure.update(-30)
        citizen.tank_social_inclusion.update(10)
        citizen.tank_self_determination.update(-20)
        citizen.tank_food.update(-20)

    def freetime_UGS(self, citizen):
        citizen.tank_mental_health.update(20)
        citizen.tank_physical_health.update(20)
        citizen.tank_leisure.update(30)
        citizen.tank_social_inclusion.update(20)
        citizen.tank_self_determination.update(30)
        citizen.tank_food.update(20)

    def freetime_home(self, citizen):
        citizen.tank_mental_health.update(20)
        citizen.tank_physical_health.update(10)
        citizen.tank_leisure.update(30)
        citizen.tank_social_inclusion.update(10)
        citizen.tank_self_determination.update(30)
        citizen.tank_food.update(-10)

#Start oder Zielknoten ist ein park
    def path_UGS(self, citizen):
        citizen.tank_mental_health.update(10)
        citizen.tank_physical_health.update(-10)
        citizen.tank_leisure.update(10)
        citizen.tank_social_inclusion.update(0)
        citizen.tank_self_determination.update(0)
        citizen.tank_food.update(-10)

#Start und Zielknoten ist kein Park
    def path_street(self, citizen):
        citizen.tank_mental_health.update(-10)
        citizen.tank_physical_health.update(-10)
        citizen.tank_leisure.update(0)
        citizen.tank_social_inclusion.update(0)
        citizen.tank_self_determination.update(0)
        citizen.tank_food.update(-10)

    def eating(self, citizen):
        citizen.tank_mental_health.update(10)
        citizen.tank_physical_health.update(20)
        citizen.tank_leisure.update(10)
        citizen.tank_social_inclusion.update(10)
        citizen.tank_self_determination.update(10)
        citizen.tank_food.update(70)
