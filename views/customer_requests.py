from models import Customer

import sqlite3
import json

CUSTOMERS = [
    {
        "id": 1,
        "name": "Ryan Tanay"
    }, 
    {
        "id": 2,
        "name": "R. Smith"
    }, 
    {
        "id": 3,
        "name": "Samantha Jones"
    }, 
    {
        "id": 4,
        "name": "Mya Harper"
    }, 
    {
        "id": 5,
        "name": "Mya Harper"
    }
] 



def get_all_customers(): 
    """gets all customers"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.name, 
            a.address, 
            a.email, 
            a.password
        FROM customer a
        """)

        customers = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'], row['password'])

            customers.append(customer.__dict__)

        return customers

def get_single_customer(id):
    """ gets a single animal"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.name, 
            a.address, 
            a.email, 
            a.password
        FROM customer a 
        WHERE a.id = ? 
        """, (id, ))
    data = db_cursor.fetchone()

    customer = Customer(data['id'], data['name'], data['address'], data['email'], data['password'])

    return customer.__dict__

def create_customer(customer):
    # Get the id value of the last customer in the list
    max_id = CUSTOMERS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    customer["id"] = new_id

    # Add the animal dictionary to the list
    CUSTOMERS.append(customer)

    # Return the dictionary with `id` property added
    return customer

def delete_customer(id):
    # Initial -1 value for customer index, in case one isn't found
    customer_index = -1

    # Iterate the CUSTOMERS list, but use enumerate() so that you
    # can access the index value of each item
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Store the current index.
            customer_index = index

    # If the customer was found, use pop(int) to remove it from list
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)

def update_customer(id, new_customer):
    # Iterate the customerS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, customer in enumerate(CUSTOMERS):
        if customer["id"] == id:
            # Found the customer. Update the value.
            CUSTOMERS[index] = new_customer
            break