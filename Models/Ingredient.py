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

    def __str__(self):
        return "From str method of Ingredient: Name is %s, Quantity is %s" % \
               (self.name, self.quantity)