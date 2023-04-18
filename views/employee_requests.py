import sqlite3
import json

from models import Employee, Location

EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }, 
    {
        "id": 2,
        "name": "Jenna Solis"
    }
]

def get_all_employees():
    """gets all employees"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.name, 
            a.address, 
            a.location_id,
            l.name as location_name,
            l.address as location_address
        FROM Employee a 
        JOIN Location l
            on a.location_id = l.id
        """)

        employees = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            location = Location(row['location_id'], row['location_name'], row['location_address'])

            employee.location = location.__dict__
            employees.append(employee.__dict__)

        return employees


def get_single_employee(id):
    """gets a single employee from id """
    with sqlite3.connect("./kennel.sqlite3") as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT 
                a.id, 
                a.name, 
                a.address, 
                a.location_id
            FROM employee a 
            Where a.id = ?
            """, (id,))
            
            data = db_cursor.fetchone()
            employee = Employee(data['id'], data['name'], data['address'], data['location_id'])
    
            return employee.__dict__

def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    employee["id"] = new_id

    # Add the animal dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    """ Deletes an employee record"""
    with sqlite3.connect("./kennel.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id, ))


def update_employee(id, new_employee):
    """Updates an existing employee record"""
    with sqlite3.connect("./kennelsqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
            UPDATE Employee
                SET 
                    name = ?, 
                    address = ?, 
                    location_id = ?
            WHERE id = ? 
        """, (new_employee['name'], new_employee['address'], new_employee['location_id'], id))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False 
    else: 
        return True
    


def get_employee_by_location(location_id): 
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            e.id,
            e.name, 
            e.address, 
            e.location_id
        FROM Employee e
        WHERE e.location_id = ?
        """, (location_id, ))

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset: 
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)
    return employees