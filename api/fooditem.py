""" Class to manage CRUD operations on food item objects"""
from api.models import DatabaseConnection
import psycopg2
from pprint import pprint

class FoodItem(object):
    """docstring for FoodItem"""
    def __init__(self):
        """ define attributes for food item. """
        self.fooditems = []
        self.db = DatabaseConnection()
        self.db.create_fooditem_table()
    
    def create_item(self, item_data):
        """ add item to fooditems list (menu) """
        item = item_data
        item['name'] = str(item_data['name'])
        item['price'] = int(item_data['price'])
        item['category'] = str(item_data['category'])
        pprint(item['name'])
        self.db.cursor.execute("INSERT INTO fooditems(name, category, price) \
        VALUES('"+ item['name'] + "','"+ item['category'] + "','"+ str(item['price']) +"')")
        return item
    
    def check_if_item_exists(self, name, price):
        """ retrieve item with similar name & price. """
        item = [item for item in self.fooditems if item['name'] == name and item['price'] == price]
        return item

    def fetch_all_fooditems(self):
        """ retrieve all fooditems from database """
        try:
            self.db.cursor.execute("SELECT * FROM fooditems")
        except TypeError as te:
            pprint(te)
        
        fooditems = self.db.cursor.fetchall()
        # pprint(fooditems)
        menuitems = []
        for item in fooditems:
            menu_item = {"id": item['id'], "name": item['name'], "category": item['category'], "price": item['price']}
            menuitems.append(menu_item)
        return menuitems

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


#   def insert_fooditem(self):
#         new_item = ("Fish", "Foods", '9000')
#         insert_command = "INSERT INTO fooditems(name, category, price) VALUES('"+ new_item[0] + "', '" + new_item[1] + "', '"+ new_item[2] +"')"
#         pprint(insert_command)
#         self.cursor.execute(insert_command)

#     def query_all(self):
#         self.cursor.execute("SELECT * FROM fooditems")
#         fooditems = self.cursor.fetchall()
#         for item in fooditems:
#             pprint("each item : {0}".format(item))

#     def update_record(self):
#         update_command = "UPDATE fooditems SET name='Fish', price=6000 WHERE id=1"
#         self.cursor.execute(update_command)