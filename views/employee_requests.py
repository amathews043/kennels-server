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

def create_employee(new_employee):
    """ creates a new employee record """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Employee
            ( name, address, location_id )
        VALUES 
            ( ?, ?, ?);
        """, (new_employee['name'], new_employee['address'], new_employee['location_id'], ))

        id = db_cursor.lastrowid

        new_employee['id'] = id

    return new_employee

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