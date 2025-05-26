# Auto-generated script to call generate functions in dependency order

import os
import json
from decimal import Decimal

from utils.file_utils import write_to_json_file

from do.Categories import generate_Categories
from do.Products import generate_Products
from do.Users import generate_Users
from do.Cart import generate_Cart
from do.Orders import generate_Orders
from do.OrderItems import generate_OrderItems
from do.Payments import generate_Payments
from do.Reviews import generate_Reviews
from do.Shipping import generate_Shipping


def main_faker():
    print('Calling generate_Categories()...')
    Categories = generate_Categories()
    write_to_json_file('Categories', Categories)

    print('Calling generate_Products(Categories)...')
    Products = generate_Products(Categories)
    write_to_json_file('Products', Products)

    print('Calling generate_Users()...')
    Users = generate_Users()
    write_to_json_file('Users', Users)

    print('Calling generate_Cart(Users, Products)...')
    Cart = generate_Cart(Users, Products)
    write_to_json_file('Cart', Cart)

    print('Calling generate_Orders(Users)...')
    Orders = generate_Orders(Users)
    write_to_json_file('Orders', Orders)

    print('Calling generate_OrderItems(Orders, Products)...')
    OrderItems = generate_OrderItems(Orders, Products)
    write_to_json_file('OrderItems', OrderItems)

    print('Calling generate_Payments(Orders)...')
    Payments = generate_Payments(Orders)
    write_to_json_file('Payments', Payments)

    print('Calling generate_Reviews(Users, Products)...')
    Reviews = generate_Reviews(Users, Products)
    write_to_json_file('Reviews', Reviews)

    print('Calling generate_Shipping(Orders)...')
    Shipping = generate_Shipping(Orders)
    write_to_json_file('Shipping', Shipping)



if __name__ == '__main__':
    main_faker()
