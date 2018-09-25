""" Class to manage CRUD operations on order objects"""
class Order(object):
    """docstring for Orders"""
    def __init__(self):
        """ define attributes for order. """
        self.orders = []

    def create_order(self, order_data):
        """ add order to orders list """
        order = order_data
        order['id'] = len(self.orders) + 1
        order['status'] = 'pending'
        self.orders.append(order)
        return order
    
    def check_if_order_exists(self, user_id, item, quantity):
        """ retrieve order with given id. """
        order = [order for order in self.orders if order['user_id'] == user_id and order['item'] == item and order['quantity'] == quantity ]
        return order

    def fetch_all_orders(self):
        """ retrieve all orders from list """
        return self.orders

    def get_order(self, order_id):
        """ retrieve order with given id. """
        order = [order for order in self.orders if order['id'] == order_id]
        return order[0]

    def update_order(self, order_id, order_data):
        """ update order details. """
        order = self.get_order(order_id)
        order['status'] = order_data['status']
        return order

    def delete_order(self, order_id):
        """ delete order. """
        order = self.get_order(order_id)
        self.orders.remove(order)
        return "Order was deleted"
