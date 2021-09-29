import json
from CoffeeMachine import CoffeMachine

file = open('input.json')
input = json.load(file)

outlets = input['machine']['outlets']['count_n']

beverages = input['machine']['beverages']
ingredientsStock = input['machine']['total_items_quantity']

machine = CoffeMachine(outlets)

for name,quantity in ingredientsStock.items():
    machine.addIngredient(name,quantity)

for name,ingredients in beverages.items():
    machine.addBeverage(name, ingredients)

machine.makeBeverage('hot_tea')
machine.makeBeverage('hot_tea')
machine.makeBeverage('hot_tea')



