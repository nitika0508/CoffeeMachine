import unittest
from io import StringIO
import sys
import time

class TestCoffeeMachine(unittest.TestCase):

    def setUp(self):
        import json
        from CoffeeMachine import CoffeMachine

        file = open('input.json')
        input = json.load(file)
        file.close()

        outlets = input['machine']['outlets']['count_n']

        beverages = input['machine']['beverages']
        ingredientsStock = input['machine']['total_items_quantity']

        machine = CoffeMachine(outlets)

        for name, quantity in ingredientsStock.items():
            machine.addIngredient(name, quantity)

        for name, ingredients in beverages.items():
            machine.addBeverage(name, ingredients)
        self.machine = machine

    def testOneBeverage(self):
        sys.stdout = mystdout = StringIO()
        self.machine.makeBeverage('black_tea')
        expectedResponse = "black_tea is prepared\n"
        time.sleep(2)
        self.assertEqual(mystdout.getvalue(), expectedResponse)

    def testMultipleBeverage(self):
        sys.stdout = mystdout = StringIO()
        self.machine.makeBeverage('black_tea')
        time.sleep(.5)
        self.machine.makeBeverage('hot_coffee')
        expectedResponse = "black_tea is prepared\nhot_coffee is prepared\n"
        time.sleep(2)
        self.assertEqual(mystdout.getvalue(), expectedResponse)

    def testWhenIngredientsNotAvailable(self):
        sys.stdout = mystdout = StringIO()
        self.machine.makeBeverage('green_tea')
        expectedResponse = "green_tea cannot be prepared because green_mixture is not available\n"
        time.sleep(2)
        self.assertEqual(mystdout.getvalue(), expectedResponse)

    def testWhenIngredientsNotSufficient(self):
        sys.stdout = mystdout = StringIO()
        self.machine.makeBeverage('hot_tea')
        self.machine.makeBeverage('hot_coffee')
        expectedResponse = "hot_coffee cannot be prepared because item hot_water is not sufficient\nhot_tea is prepared\n"
        time.sleep(2)
        self.assertEqual(mystdout.getvalue(), expectedResponse)

    def testWhenMoreBeveragesThanOutlestAndRefillIndicator(self):
        sys.stdout = mystdout = StringIO()
        self.machine.makeBeverage('hot_coffee')
        self.machine.makeBeverage('hot_coffee')
        time.sleep(.5)
        self.machine.makeBeverage('hot_coffee')
        expectedResponse = "This beverage hot_coffee is in queue\nhot_coffee is prepared\nhot_coffee is prepared\nFor Ingredient hot_water Quantity is running low\n" \
                           "For Ingredient ginger_syrup Quantity is running low\nFor Ingredient tea_leaves_syrup Quantity is running low\nhot_coffee is prepared\n"
        time.sleep(3)
        self.assertEqual(mystdout.getvalue(), expectedResponse)

    def testBeverageNotSupported(self):
        with self.assertRaises(Exception) as cm:
            self.machine.makeBeverage('latte')
        self.assertEqual(
            'Beverage latte is not supported',
            str(cm.exception)
        )

    def testIngredientQuantityExceedsCapacity(self):
        with self.assertRaises(Exception) as cm:
            self.machine.addIngredient('hot_water', 2000)
        self.assertEqual(
            'Ingredient quantity hot_water is exceeding the capacity',
            str(cm.exception)
        )


if __name__ == '__main__':
    unittest.main()


