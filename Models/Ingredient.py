class Ingredient:

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def getName(self):
        return self.name

    def getQuantity(self):
        return self.quantity

    def setQuantity(self, quantity):
        self.quantity = quantity
