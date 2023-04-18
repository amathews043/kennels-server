import sqlite3
import json

from models import Location, Animal

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    """gets all locations"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.name, 
            a.address
        FROM location a
        """)

        locations = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            location = Location(row['id'], row['name'], row['address'])

            locations.append(location.__dict__)

        return locations

def get_single_location(id):
    """gets a single location from an id """

    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id, 
            a.name, 
            a.address
        FROM location a
        WHERE a.id = ?
        """, (id,))

        data = db_cursor.fetchone()

        location = Location(data['id'], data['name'], data['address'])

        return location.__dict__
        

def create_location(location):
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the animal dictionary
    location["id"] = new_id

    # Add the animal dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    """delete a location record"""

    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))


def update_location(id, new_location):
    """updates and existing location record"""

    with sqlite3.connect("./kennel.sqlite3") as conn: 
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET 
            name = ?, 
            address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id))

        rows_affected = db_cursor.rowcount

        if rows_affected == 0: 
            return False 
        else: 
            return True

def get_animals_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            a.id,
            a.name, 
            a.status, 
            a.breed, 
            a.location_id,
            a.customer_id
        FROM Animal a
        WHERE a.location_id = ?
        """, (location_id, ))

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset: 
            animal = Animal(row['id'], row['name'], row['status'], row['breed'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
    return animals