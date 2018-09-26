""" Class to manage CRUD operations on food item objects"""
class FoodItem(object):
    """docstring for FoodItem"""
    def __init__(self):
        """ define attributes for food item. """
        self.fooditems = []

    def create_item(self, item_data):
        """ add item to fooditems list """
        item = item_data
        item['id'] = len(self.fooditems) + 1
        self.fooditems.append(item)
        return item
    
    def check_if_item_exists(self, name, price):
        """ retrieve item with similar name & price. """
        item = [item for item in self.fooditems if item['name'] == name and item['price'] == price]
        return item

    def fetch_all_fooditems(self):
        """ retrieve all fooditems from list """
        return self.fooditems

    def get_item(self, item_id):
        """ retrieve item with given id. """
        item = [item for item in self.fooditems if item['id'] == item_id]
        return item[0]

    def update_item(self, item_id, item_data):
        """ update item details. """
        item = self.get_item(item_id)
        item['name'] = item_data['name']
        item['price'] = item_data['price']
        return item

    def delete_item(self, item_id):
        """ delete item. """
        item = self.get_item(item_id)
        self.fooditems.remove(item)
        return "fooditem was deleted"
