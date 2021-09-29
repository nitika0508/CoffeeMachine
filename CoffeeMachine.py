import config
from Models.Ingredient import Ingredient
from Models.Beverage import Beverage

class CoffeMachine:

    def __init__(self,outlets):
        self.outlets = outlets
        self.ingredientsInfo = config.ingredientsInfo
        self.ingredients = {}
        self.beverages = {}

    def getIngredients(self):
        return self.ingredients

    def getBeverages(self):
        return self.beverages

    def addIngredient(self, name, quantity):
        if name not in self.ingredientsInfo:
            raise Exception('Ingredient %s Not Supported', name)

        if name not in self.ingredients:
            ingredient = Ingredient(name, 0)
            self.ingredients[name] = ingredient

        currentQuantity = self.ingredients[name].getQuantity()
        if currentQuantity + quantity > self.ingredientsInfo[name]['capacity']:
            raise Exception("Ingredient quantity %s is exceeding the capacity",name)
        self.ingredients[name].setQuantity(currentQuantity + quantity)

    def addBeverage(self, name, ingredients):
        beverageIngredients = {}
        for ingredient,quantity in ingredients.items():
            beverageIngredients[ingredient] = Ingredient(ingredient,quantity)
        self.beverages[name] = Beverage(name, beverageIngredients)

    def getIngredientQuantity(self, name):
        return self.ingredients[name].getQuantity()

    def setIngredientQuantity(self, name, quantity):
        self.ingredients[name].setQuantity(quantity)

    def canMakeBeverage(self, beverageName):
        if beverageName not in self.beverages:
            raise Exception('Beverage %s is not supported', beverageName)

        beverageIngredients = self.beverages[beverageName].getIngredients()
        for beverageIngredientName,beverageIngredient in beverageIngredients.items():
            if beverageIngredientName not in self.ingredients:
                return False
            if self.getIngredientQuantity(beverageIngredientName) < beverageIngredient.getQuantity():
                return False
        return True


    def makeBeverage(self, beverageName):
        if not self.canMakeBeverage(beverageName):
            raise Exception("Can't prepare beverage")

        beverage = self.beverages[beverageName]
        beverageIngredients = beverage.getIngredients()
        for beverageIngredientName, beverageIngredient in beverageIngredients.items():
            currentIngredientQuantity = self.getIngredientQuantity(beverageIngredientName)
            quantityAfterBeverage = currentIngredientQuantity - beverageIngredient.getQuantity()
            self.setIngredientQuantity(beverageIngredientName,quantityAfterBeverage)
            if(quantityAfterBeverage < self.ingredientsInfo[beverageIngredientName]['threshold']):
                self.refillIndicator(beverageIngredientName)
        return "We have prepared $beverageName"

    def refillIndicator(self, name):
        print("Ingredient Quantity low " + name)

    def __str__(self):
        return "From str method of CoffeeMacine: Outlets is %s, \n ingredientsInfo is %s \n, ingredients is %s" % \
               (self.outlets, self.ingredientsInfo, self.printIngredients())

    def printIngredients(self):
        print 'Ingredients INFO'
        for name, ingredient in self.ingredients.items():
            print ingredient













