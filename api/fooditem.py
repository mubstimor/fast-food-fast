""" Class to manage CRUD operations on food item objects"""
from api.models import DatabaseConnection

class FoodItem(object):
    """docstring for FoodItem"""
    def __init__(self):
        """ define connections to food items table. """
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
        try:
            self.db.cursor.execute("SELECT * FROM fooditems where name='"+name+"'")
        except TypeError as e:
            print(e)
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
            print(e)
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
            print(e)
        item = self.db.cursor.fetchone()
        rows_found = self.db.cursor.rowcount
        if rows_found > 0:
            menu_item = {"id": item['id'], "name": item['name'], "category": item['category'], "price": item['price']}
            return menu_item
        else:
            return "not found"
        

    def update_item(self, item_id, item_data):
        """ update item details. """
        item = item_data
        item['name'] = str(item_data['name'])
        item['price'] = int(item_data['price'])
        item['category'] = str(item_data['category'])
        try:
            self.db.cursor.execute("UPDATE fooditems set name='"+item['name']+"', category='"+item['category']+"', price='"+str(item['price'])+"' WHERE id='"+str(item_id)+"'")
        except TypeError as e:
            print(e)
        
        rows_updated = self.db.cursor.rowcount
        if rows_updated > 0:
            return item
        else:
            return "unable to update item"

    def delete_item(self, item_id):
        """ delete item. """
        try:
            self.db.cursor.execute("DELETE FROM fooditems WHERE id='"+str(item_id)+"'")
        except:
            print("unable to delete")
        rows_deleted = self.db.cursor.rowcount
        if rows_deleted > 0:
            return "fooditem was deleted"
        else:
            return "unable to delete item"
