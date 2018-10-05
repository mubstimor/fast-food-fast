""" Class to manage CRUD operations on order objects"""
import psycopg2
import psycopg2.extras
from api.db.database import DatabaseConnection

class Order(DatabaseConnection):
    """docstring for Orders"""
    def __init__(self):
        """ define attributes for order. """
        DatabaseConnection.__init__(self)
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) 

    def create_order(self, user_id, order_data):
        """ add order to orders list """
        order = order_data
        order['item'] = int(order_data['item'])
        order['quantity'] = str(order_data['quantity'])
        order['status'] = 'new'
        try:
            self.cursor.execute("INSERT INTO orders(item, quantity, status, user_id) \
                                VALUES('"+ str(order['item']) + "','"+ order['quantity'] +"', '"+ \
                                order['status']+"', '"+str(user_id)+"') RETURNING id")
            order_id = self.cursor.fetchone()[0]
            return order_id
        except (psycopg2.DatabaseError) as error:
            return
        
        
    def check_if_order_exists(self, user_id, item, quantity):
        """ retrieve order with given id. """
        self.cursor.execute("SELECT * FROM orders where user_id='"+str(user_id) \
            +"' AND item='"+ str(item)+"' AND quantity='"+ str(quantity)+"'")
        rows_found = self.cursor.rowcount
        if rows_found > 0:
            return True

    def fetch_all_orders(self):
        """ retrieve all orders from db """
        self.cursor.execute("SELECT od.id as id, menu.name as item, od.quantity as quantity, cu.name as user_id, od.status as status \
                            FROM orders as od, users as cu, fooditems as menu \
                            WHERE od.id=cu.id and od.id=menu.item_id and od.status !='cancelled'")
        orderitems = self.cursor.fetchall()
        orders = []
        for item in orderitems:
            order = {"order_id": item['id'], "item": item['item'], "quantity": item['quantity'], "status": item['status'], "customer": item['user_id']}
            orders.append(order)
        return orders

    def fetch_user_orders(self, user_id):
        """ retrieve all orders from list """
        self.cursor.execute("SELECT od.id as id, menu.name as item, \
od.quantity as quantity, od.status as status \
                            FROM orders as od, fooditems as menu \
                            WHERE od.item=menu.item_id and od.status !='cancelled' and od.user_id='"+str(user_id)+"'")
        order_items = self.cursor.fetchall()
        orders = []
        for item in order_items:
            order = {"id": item['id'], "item": item['item'], "quantity": item['quantity'], "status": item['status']}
            orders.append(order)
        return orders

    def get_order(self, order_id):
        """ retrieve order with given id. """
        sql = """SELECT od.id as id, menu.name as item,
             od.quantity as quantity, od.status as status, cu.name as user_id
             FROM orders as od, fooditems as menu, users as cu
              WHERE od.item=menu.item_id and od.status !='cancelled'
              and od.user_id=cu.id and od.id=%s;
             ;"""
        self.cursor.execute(sql, (str(order_id)))
        order_item = self.cursor.fetchone()
        rows_found = self.cursor.rowcount
        if rows_found > 0:
            order = {"id": order_item['id'], "item": order_item['item'], "quantity": order_item['quantity'], "status": order_item['status'], "user_id": order_item['user_id']}
            return order

    def update_order(self, order_id, order_data):
        """ update order details. """
        order = order_data
        order['status'] = str(order_data['status'])
        self.cursor.execute("UPDATE orders set status='"+order['status']+"' WHERE id='"+str(order_id)+"'")
        
        rows_updated = self.cursor.rowcount
        if rows_updated > 0:
            return order
        else:
            return "unable to update order"

    def update_user_order(self, order_id, order_data):
        """ update order details. """
        order = order_data
        order['item'] = str(order_data['item'])
        order['quantity'] = int(order_data['quantity'])
        order['status'] = str(order_data['status'])
        self.cursor.execute("UPDATE orders set item='"+order['item']+"', quantity='"+ str(order['quantity'])+"', status='"+order['status']+"' WHERE id='"+str(order_id)+"'")
        rows_updated = self.cursor.rowcount
        if rows_updated > 0:
            order['id'] = order_id
            return order
        else:
            return "unable to update order"

    def delete_order(self, order_id):
        """ delete order. """
        self.cursor.execute("DELETE FROM orders WHERE id='"+str(order_id)+"'")
        rows_deleted = self.cursor.rowcount
        if rows_deleted > 0:
            return "order was deleted"
        else:
            return "unable to delete order"

    def close_order_connection(self):
        """ close db conn """
        self.cursor.close()
        self.connection.close()


order = Order()
order.close_order_connection()