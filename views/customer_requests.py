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
    """ gets a single customer"""
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
    """delete a customer record"""

    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM customer
        WHERE id = ?
        """, (id, ))

def update_customer(id, new_customer):
    """ Updates an existing customer record"""

    with sqlite3.connect("./kneeel.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Customer
            SET
                name = ?, 
                address = ?, 
                email = ?, 
                password = ?
        WHERE id = ?
        """, (new_customer['name'], new_customer['address'], new_customer['email'], new_customer['password'], id))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False 
        else: 
            return True

def get_customers_by_email(email):
    print(email)
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        FROM customer c
        WHERE c.email = ?
        """, ( email, ),)

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row['address'], row['email'] , row['password'],)
            customers.append(customer.__dict__)

    print(customers)

    return customers