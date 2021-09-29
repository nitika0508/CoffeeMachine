import threading
import config
from Models.Ingredient import Ingredient
from Models.Beverage import Beverage
import time

class CoffeMachine:

    def __init__(self,outlets):
        self.__outlets = outlets
        self.__ingredients = {}
        self.__beverages = {}
        self.__ingredientsInfo = config.ingredientsInfo

    def getIngredients(self):
        return self.__ingredients

    def getBeverages(self):
        return self.__beverages

    #adding or refilling Ingredient stock in machine, throws exception if Ingredient can't be added / exceeds capacity
    def addIngredient(self, name, quantity):
        if name not in self.__ingredientsInfo:
            raise Exception('Ingredient %s Not Supported' %(name))

        if name not in self.__ingredients:
            ingredient = Ingredient(name, 0)
            self.__ingredients[name] = ingredient

        currentQuantity = self.__ingredients[name].getQuantity()
        if currentQuantity + quantity > self.__ingredientsInfo[name]['capacity']:
            raise Exception("Ingredient quantity %s is exceeding the capacity" %(name))
        self.__ingredients[name].setQuantity(currentQuantity + quantity)

    #public method assuming beverage can be configured in the coffee machine at any point
    def addBeverage(self, name, ingredients):
        beverageIngredients = {}
        for ingredient,quantity in ingredients.items():
            beverageIngredients[ingredient] = Ingredient(ingredient,quantity)
        self.__beverages[name] = Beverage(name, beverageIngredients)

    def getIngredientQuantity(self, name):
        return self.__ingredients[name].getQuantity()

    def setIngredientQuantity(self, name, quantity):
        self.__ingredients[name].setQuantity(quantity)

    #checks if the beverage ingredients requirement can be fulfilled with the available stock
    def __checkIngredientsStockForBeverage(self, beverageName):
        if beverageName not in self.__beverages:
            raise Exception("Beverage %s is not supported" % (beverageName))

        beverageIngredients = self.__beverages[beverageName].getIngredients()
        for beverageIngredientName,beverageIngredient in beverageIngredients.items():
            if beverageIngredientName not in self.__ingredients:
                print("%s cannot be prepared because %s is not available" %(beverageName, beverageIngredientName))
                return False
            if self.getIngredientQuantity(beverageIngredientName) < beverageIngredient.getQuantity():
                print("%s cannot be prepared because item %s is not sufficient" %(beverageName, beverageIngredientName))
                return False
        return True

    #prepare beverage by removing the beverage required ingredients from the stock
    def __mixIngredientsForBeverage(self, beverageName):
        if not self.__checkIngredientsStockForBeverage(beverageName):
            return False

        beverage = self.__beverages[beverageName]
        beverageIngredients = beverage.getIngredients()
        for beverageIngredientName, beverageIngredient in beverageIngredients.items():
            currentIngredientQuantity = self.getIngredientQuantity(beverageIngredientName)
            quantityAfterBeverage = currentIngredientQuantity - beverageIngredient.getQuantity()
            self.setIngredientQuantity(beverageIngredientName,quantityAfterBeverage)
            if(quantityAfterBeverage < self.__ingredientsInfo[beverageIngredientName]['threshold']):
                self.refillIndicator(beverageIngredientName)
        return True

    def refillIndicator(self, name):
        print("For Ingredient %s Quantity is running low" %(name))

    def __dispense(self, beverageName):
        time.sleep(1)
        print('%s is prepared' %(beverageName))

    #can dispense multiple beverages in parallel with the capacity of n outlets
    def makeBeverage(self, beverageName):
        while(1):
            if threading.active_count() <= self.__outlets:
                result = self.__mixIngredientsForBeverage(beverageName)
                if not result:
                    return
                thread = threading.Thread(target=self.__dispense, args=(beverageName,))
                thread.start()
                break
            print('This beverage %s is in queue'%(beverageName))
            time.sleep(1)