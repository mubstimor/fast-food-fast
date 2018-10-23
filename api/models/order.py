""" Class to manage CRUD operations on order objects"""
import psycopg2
import psycopg2.extras
from api.db.database import DatabaseConnection

class Order(object):
    """docstring for Orders"""
    def __init__(self):
        """ define attributes for order. """
        self._db = DatabaseConnection()
        self.connection = None
        self.cursor = None

    def create_order(self, user_id, order_data):
        """ add order to orders list """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        order = order_data
        order['item'] = int(order_data['name'])
        order['quantity'] = str(order_data['quantity'])
        order['status'] = 'new'
        self.cursor.execute("INSERT INTO orders(item, quantity, \
                            status, user_id) \
                            VALUES('"+ str(order['item']) + "','"+
                            order['quantity']
                            +"', '"+ order['status']+"', '"
                            +str(user_id)+"') RETURNING id")
        order_id = self.cursor.fetchone()[0]
        self.connection.close()
        return order_id

    def check_if_order_exists(self, user_id, item, quantity):
        """ retrieve order with given id. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute(
            "SELECT * FROM orders where user_id='"
            +str(user_id)
            +"' AND item='"+ str(item)
            +"' AND quantity='"+ str(quantity)
            +"' AND "+
            "last_updated > current_timestamp - interval '30 minutes'")
        rows_found = self.cursor.rowcount
        self.connection.close()
        if rows_found > 0:
            return True

    def fetch_all_orders(self):
        """ retrieve all orders from db """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute(
            "SELECT od.id as id, menu.name as item, od.quantity as quantity, \
            cu.name as user_id, od.status as status \
            FROM orders as od, users as cu, fooditems as menu \
            WHERE od.user_id=cu.id and od.item=menu.item_id \
            and od.status !='cancelled'")
        orderitems = self.cursor.fetchall()
        orders = []
        for item in orderitems:
            order = self.order_json(item['id'], item['item'],
                                    item['quantity'], item['status'],
                                    item['user_id'])
            orders.append(order)
        self.connection.close()
        return orders

    def fetch_user_orders(self, user_id):
        """ retrieve all orders from list """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT od.id as id, menu.name as item, \
		trim(trailing ' ' from to_char(od.last_updated, 'Day')) || \
          ', ' || \
          trim(trailing ' ' from to_char(od.last_updated, 'Month')) || \
          ' ' || \
          to_char(od.last_updated, 'DD') || \
          ', ' || \
          to_char(od.last_updated, 'YYYY') \
          ||' at ' || \
          to_char(od.last_updated, 'HH24:MM') \
           as order_date, \
                            od.quantity as quantity, od.status as status \
                            FROM orders as od, fooditems as menu \
                            WHERE od.item=menu.item_id \
                            and od.status !='cancelled' \
                            and od.user_id='"+str(user_id)+"'")
        order_items = self.cursor.fetchall()
        orders = []
        for item in order_items:
            order = {"id": item['id'], "order_date": item['order_date'],
                     "item": item['item'], "quantity": item['quantity'],
                     "status": item['status']}
            orders.append(order)
        self.connection.close()
        return orders

    def fetch_user_order(self, order_id, user_id):
        """ retrieve order of a user based on order id & user id. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        self.cursor.execute("SELECT od.id as id, menu.name as item, \
                            od.quantity as quantity, od.status as status \
                            FROM orders as od, fooditems as menu \
                            WHERE od.item=menu.item_id and \
                            od.status !='cancelled' \
                            and od.user_id='"+str(user_id)+"' and od.id='"
                            +str(order_id)+"'")
        order_item = self.cursor.fetchone()
        self.connection.close()
        order = {"id": order_item['id'], "item": order_item['item'],
                 "quantity": order_item['quantity'],
                 "status": order_item['status']
                }
        return order

    def get_order(self, order_id):
        """ retrieve order with given id. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        sql = "SELECT od.id as id, menu.name as item,\
             od.quantity as quantity, od.status as status, cu.name as user_id \
             FROM orders as od, fooditems as menu, users as cu \
              WHERE od.item=menu.item_id and od.status !='cancelled' \
              and od.user_id=cu.id and od.id='"+str(order_id)+"'"
        self.cursor.execute(sql)
        item = self.cursor.fetchone()
        rows_found = self.cursor.rowcount
        self.connection.close()
        if rows_found > 0:
            order = self.order_json(item['id'], item['item'],
                                    item['quantity'], item['status'],
                                    item['user_id'])
            return order

    def update_order(self, order_id, order_data):
        """ update order details. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        order = order_data
        order['status'] = str(order_data['name'])
        self.cursor.execute("UPDATE orders set status='"+order['status']
                            + "' WHERE id='"+str(order_id)+"'")
        rows_updated = self.cursor.rowcount
        self.connection.close()
        if rows_updated > 0:
            return order
        else:
            return "unable to update order"

    def update_user_order(self, order_id, order_data):
        """ update order details. """
        self.connection = self._db.connect_db()
        self.cursor = self.connection.cursor(
            cursor_factory=psycopg2.extras.DictCursor)
        order = order_data
        order['item'] = str(order_data['item'])
        order['quantity'] = int(order_data['quantity'])
        order['status'] = str(order_data['status'])
        self.cursor.execute("UPDATE orders set item='"+order['item']
                            +"', quantity='"+ str(order['quantity'])
                            +"', status='"
                            + order['status']+"' WHERE id='"+str(order_id)+"'")
        rows_updated = self.cursor.rowcount
        self.connection.close()
        if rows_updated > 0:
            order['id'] = order_id
            return order
        else:
            return "unable to update order"

    def order_json(self, _id, item, quantity, status, user_id):
        """ generate json for single order object. """
        order = {"id": _id, "item": item,
                 "quantity": quantity, "status": status,
                 "customer": user_id}
        return order
