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
        if not self.check_if_item_exists(item['name']):
            self.db.cursor.execute("INSERT INTO fooditems(name, category, price) \
            VALUES('"+ item['name'] + "','"+ item['category'] + "','"+ str(item['price']) +"')")
            return item
        else:
            return "Unable to create item"
    
    def check_if_item_exists(self, name):
        """ retrieve item with similar name"""
        # item = [item for item in self.fooditems if item['name'] == name and item['price'] == price]
        # return item
        try:
            self.db.cursor.execute("SELECT * FROM fooditems where name='"+name+"'")
        except TypeError as e:
            pprint(e)
        # item = self.db.cursor.fetchone()
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            return True
        else:
            return False

    def fetch_all_fooditems(self):
        """ retrieve all fooditems from database """
        try:
            self.db.cursor.execute("SELECT * FROM fooditems")
        except TypeError as e:
            pprint(e)
        fooditems = self.db.cursor.fetchall()
        menuitems = []
        for item in fooditems:
            menu_item = {"id": item['id'], "name": item['name'], "category": item['category'], "price": item['price']}
            menuitems.append(menu_item)
        return menuitems

    def get_item(self, item_id):
        """ retrieve item with given id from database. """
        try:
            self.db.cursor.execute("SELECT * FROM fooditems where id='"+str(item_id)+"'")
        except TypeError as e:
            pprint(e)
        item = self.db.cursor.fetchone()
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            menu_item = {"id": item['id'], "name": item['name'], "category": item['category'], "price": item['price']}
            return menu_item
        else:
            return "not found"
        

    def update_item(self, item_id, item_data):
        """ update item details. """
        # item = self.get_item(item_id)
        item = item_data
        item['name'] = str(item_data['name'])
        item['price'] = int(item_data['price'])
        item['category'] = str(item_data['category'])
        try:
            self.db.cursor.execute("UPDATE fooditems set name='"+item['name']+"', category='"+item['category']+"', price='"+str(item['price'])+"' WHERE id='"+str(item_id)+"'")
        except TypeError as e:
            pprint(e)
        
        rows_updated = self.db.cursor.rowcount
        if rows_updated > 0:
            return item
        else:
            return "unable to update item"
        # return item

    def delete_item(self, item_id):
        """ delete item. """
        # item = self.get_item(item_id)
        # self.fooditems.remove(item)
        try:
            self.db.cursor.execute("DELETE FROM fooditems WHERE id='"+str(item_id)+"'")
        except:
            pprint("unable to print")
        rows_deleted = self.db.cursor.rowcount
        if rows_deleted > 0:
            return "fooditem was deleted"
        else:
            return "unable to delete item"


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