class Order():
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

    def fetch_all_orders(self):
        """ retrieve all orders from list """
        return self.orders

    def get_order(self, order_id):
        """ retrieve order with given id. """
        order = [order for order in self.orders if order['id'] == order_id]
        return order

    def update_order(self, order_id, order_data):
        """ update order details. """
        order = self.get_order(order_id)
        order[0]['status'] = order_data['status']
        order[0]['item'] = order_data['item']
        order[0]['quantity'] = order_data['quantity']
        return order

    def delete_order(self, order_id):
        """ delete order. """
        order = self.get_order(order_id)
        self.orders.remove(order[0])
        return True
