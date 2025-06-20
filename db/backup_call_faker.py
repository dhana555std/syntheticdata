# Auto-generated script to call generate functions in dependency order

import os
import json
from decimal import Decimal

from utils.file_utils import write_to_json_file

from do.DimCategory import generate_DimCategory
from do.DimDate import generate_DimDate
from do.DimPaymentMethod import generate_DimPaymentMethod
from do.DimProduct import generate_DimProduct
from do.DimShipping import generate_DimShipping
from do.DimUser import generate_DimUser
from do.FactOrders import generate_FactOrders
from do.FactPayments import generate_FactPayments
from do.FactShipping import generate_FactShipping


def main_faker():
    print('Calling generate_DimCategory()...')
    DimCategory = generate_DimCategory()
    write_to_json_file('DimCategory', DimCategory)

    print('Calling generate_DimDate()...')
    DimDate = generate_DimDate()
    write_to_json_file('DimDate', DimDate)

    print('Calling generate_DimPaymentMethod()...')
    DimPaymentMethod = generate_DimPaymentMethod()
    write_to_json_file('DimPaymentMethod', DimPaymentMethod)

    print('Calling generate_DimProduct()...')
    DimProduct = generate_DimProduct()
    write_to_json_file('DimProduct', DimProduct)

    print('Calling generate_DimShipping()...')
    DimShipping = generate_DimShipping()
    write_to_json_file('DimShipping', DimShipping)

    print('Calling generate_DimUser()...')
    DimUser = generate_DimUser()
    write_to_json_file('DimUser', DimUser)

    print('Calling generate_FactOrders(DimUser, DimProduct, DimDate)...')
    FactOrders = generate_FactOrders(DimUser, DimProduct, DimDate)
    write_to_json_file('FactOrders', FactOrders)

    print('Calling generate_FactPayments(FactOrders, DimPaymentMethod, DimDate)...')
    FactPayments = generate_FactPayments(FactOrders, DimPaymentMethod, DimDate)
    write_to_json_file('FactPayments', FactPayments)

    print('Calling generate_FactShipping(FactOrders, DimDate)...')
    FactShipping = generate_FactShipping(FactOrders, DimDate)
    write_to_json_file('FactShipping', FactShipping)



if __name__ == '__main__':
    main_faker()
