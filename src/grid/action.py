
class Action:

    def sleeping(self, citizen):
        citizen.tank_mental_health.update(1)
        citizen.tank_physical_health.update(2)
        citizen.tank_leisure.update(-2)
        citizen.tank_social_inclusion.update(-3)
        citizen.tank_self_determination.update(-2)
        citizen.tank_food.update(-2)
    def working(self, citizen):
        citizen.tank_mental_health.update(-3)
        citizen.tank_physical_health.update(-3)
        citizen.tank_leisure.update(-3)
        citizen.tank_social_inclusion.update(1)
        citizen.tank_self_determination.update(-2)
        citizen.tank_food.update(-2)

    def freetime_UGS(self, citizen):
        citizen.tank_mental_health.update(4)
        citizen.tank_physical_health.update(4)
        citizen.tank_leisure.update(6)
        citizen.tank_social_inclusion.update(4)
        citizen.tank_self_determination.update(6)
        citizen.tank_food.update(4)

    def freetime_home(self, citizen):
        citizen.tank_mental_health.update(4)
        citizen.tank_physical_health.update(2)
        citizen.tank_leisure.update(6)
        citizen.tank_social_inclusion.update(2)
        citizen.tank_self_determination.update(6)
        citizen.tank_food.update(-2)

#Start oder Zielknoten ist ein park
    def path_UGS(self, citizen, greenscore):

        if greenscore >= 66:
            citizen.tank_mental_health.update(2)
            citizen.tank_physical_health.update(-2)
            citizen.tank_leisure.update(2)
            citizen.tank_social_inclusion.update(0)
            citizen.tank_self_determination.update(0)
            citizen.tank_food.update(-2)
        elif 33 <= greenscore < 66:
            citizen.tank_mental_health.update(1)
            citizen.tank_physical_health.update(-2)
            citizen.tank_leisure.update(1)
            citizen.tank_social_inclusion.update(0)
            citizen.tank_self_determination.update(0)
            citizen.tank_food.update(-2)
        elif greenscore < 33:
            citizen.tank_mental_health.update(-1)
            citizen.tank_physical_health.update(-2)
            citizen.tank_leisure.update(-1)
            citizen.tank_social_inclusion.update(0)
            citizen.tank_self_determination.update(0)
            citizen.tank_food.update(-2)

#Start und Zielknoten ist kein Park
    def path_street(self, citizen):
        citizen.tank_mental_health.update(-2)
        citizen.tank_physical_health.update(-2)
        citizen.tank_leisure.update(0)
        citizen.tank_social_inclusion.update(0)
        citizen.tank_self_determination.update(0)
        citizen.tank_food.update(-2)

    def eating(self, citizen):
        citizen.tank_mental_health.update(-1)
        citizen.tank_physical_health.update(-2)
        citizen.tank_leisure.update(-1)
        citizen.tank_social_inclusion.update(-1)
        citizen.tank_self_determination.update(-1)
        citizen.tank_food.update(-20)
