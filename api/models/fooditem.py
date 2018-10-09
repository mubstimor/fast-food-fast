""" Class to manage CRUD operations on food item objects"""
import psycopg2
import psycopg2.extras
from api.db.database import DatabaseConnection

class FoodItem(object):
    """docstring for FoodItem"""
    def __init__(self):
        """ define connections to food items table. """
        self._db = DatabaseConnection()
        self.connection = None
        self.cursor = None

    def create_item(self, item_data):
        """ add item to fooditems list (menu) """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        item = item_data
        item['name'] = str(item_data['name'])
        item['price'] = int(item_data['price'])
        item['category'] = str(item_data['category'])
        self.cursor.execute("INSERT INTO fooditems(name, category, price) \
                            VALUES('"+ item['name'] + "','"+ item['category']
                            + "','"+ str(item['price']) +"') RETURNING item_id")
        item_id = self.cursor.fetchone()[0]
        item['id'] = item_id
        self.connection.close()
        return item

    def check_if_item_exists(self, name):
        """ retrieve item with similar name"""
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT * FROM fooditems where name='"+name+"'")
        rows_found = self.cursor.rowcount
        self.connection.close()
        if rows_found > 0:
            return True
        else:
            return False

    def fetch_all_fooditems(self):
        """ retrieve all fooditems from database """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT * FROM fooditems")
        fooditems = self.cursor.fetchall()
        menuitems = []
        for item in fooditems:
            menu_item = {"id": item['item_id'], "name": item['name'],
                         "category": item['category'], "price": item['price']}
            menuitems.append(menu_item)
        self.connection.close()
        return menuitems

    def get_item(self, item_id):
        """ retrieve item with given id from database. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT * FROM fooditems where item_id='"+str(item_id)+"'")
        item = self.cursor.fetchone()
        rows_found = self.cursor.rowcount
        self.connection.close()
        if rows_found > 0:
            menu_item = {"id": item['item_id'], "name": item['name'],
                         "category": item['category'], "price": item['price']}
            return menu_item
        else:
            return "not found"

    def update_item(self, item_id, item_data):
        """ update item details. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        item = item_data
        item['name'] = str(item_data['name'])
        item['price'] = int(item_data['price'])
        item['category'] = str(item_data['category'])
        self.cursor.execute("UPDATE fooditems set name='"+item['name']
                            +"', category='"+item['category']+"', price='"+str(item['price'])
                            +"' WHERE item_id='"+str(item_id)+"'")
        rows_updated = self.cursor.rowcount
        self.connection.close()
        if rows_updated > 0:
            return item
        else:
            return "unable to update item"

    def delete_item(self, item_id):
        """ delete item. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("DELETE FROM fooditems WHERE item_id='"+str(item_id)+"'")
        rows_deleted = self.cursor.rowcount
        self.connection.close()
        if rows_deleted > 0:
            return "fooditem was deleted"
        else:
            return "unable to delete item"
