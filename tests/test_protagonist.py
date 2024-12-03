import unittest
from src.classes.protagonist import Protagonist, Group1Protagonist, Group2Protagonist

class TestProtagonist(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes das classe Protagonist"""
        self.group1_protagonist = Group1Protagonist(
            name="Daphne",
            speed=5,
            perception=3,
            x_position=10,
            y_position=20,
            width=50,
            height=50,
            direction="north",
            skin="default",
            life=100,
            inventory=["sword", "shield"],
            ability="invisibility",
            sprites_quantity=10,
            map_limits_sup=[200, 200],  
            bullets=5,
            weapon="gun",
            trap_power=50
        )

        
        self.group2_protagonist = Group2Protagonist(
            name="Shaggy",
            speed=12,
            perception=6,
            x_position=10,
            y_position=10,
            width=50,
            height=50,
            direction="up",
            skin="default",
            life=90,
            inventory=["itemA"],
            ability="invisibility",
            sprites_quantity=8,
            map_limits_sup=[200, 200],
            bullets=3,
            weapon="knife",
            deceive_power=20
        )

    def test_life_property(self):
        # Test getter
        self.assertEqual(self.group1_protagonist.life, 100)
        # Test setter
        self.group1_protagonist.life = 80
        self.assertEqual(self.group1_protagonist.life, 80)

    def test_inventory_property(self):
        # Test getter
        self.assertEqual(self.group1_protagonist.inventory, ["sword", "shield"])
        # Test setter
        self.group1_protagonist.inventory = ["item3"]
        self.assertEqual(self.group1_protagonist.inventory, ["item3"])

    def test_ability_property(self):
        # Test getter
        self.assertEqual(self.group1_protagonist.ability, "invisibility")
        # Test setter
        self.group1_protagonist.ability = "dash"
        self.assertEqual(self.group1_protagonist.ability, "dash")

    def test_trap_power_property(self):
        # Test getter
        self.assertNotEqual(self.group1_protagonist.trap_power, 15)
        # Test setter
        self.group1_protagonist.trap_power = 20
        self.assertEqual(self.group1_protagonist.trap_power, 20)

    def test_deceive_power_property(self):
        # Test getter
        self.assertEqual(self.group2_protagonist.deceive_power, 20)
        # Test setter
        self.group2_protagonist.deceive_power = 25
        self.assertEqual(self.group2_protagonist.deceive_power, 25)

if __name__ == "__main__":
    unittest.main()
