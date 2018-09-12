"""Describes all models that represent data in the app."""

class User():
    """docstring for User"""
    def __init__(self, id, email, password, gender, user_type='customer'):
        """ Define user attributes """
        self.id = id
        self.email = email
        self.password = password
        self.gender = gender
        self.user_type = user_type

    def get_user(self):
        """ Return user data """
        return {'id': self.id, 'email': self.email}

class FoodItem():
    """docstring for FoodItem"""
    def __init__(self, id, name, price):
        """ Define food item attributes """
        self.id = id
        self.name = name
        self.price = price

    def get_food_item(self):
        """ format food item object into a dictionary. """
        return {'id': self.id, 'name': self.name, 'price': self.price}


class OrderItem():
    """docstring for OrderItem"""
    def __init__(self, food_item, quantity):
        """ Define order item attributes """
        self.food_item = food_item
        self.quantity = quantity

    def get_order_item(self):
        """ format order item object into a dictionary. """
        return {'food_item':self.food_item.name, \
        'quantity': self.quantity, 'order_value': self.quantity * self.food_item.price}
