import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, create_animal, get_single_animal, get_all_locations, get_single_location
from views import get_single_customer, get_all_customers, get_single_employee, get_all_employees, create_location
from views import create_employee, create_customer, delete_animal, delete_location, delete_employee, delete_customer
from views import update_animal, update_customer, update_employee, update_location, get_customers_by_email, get_animals_by_location
from views import get_employee_by_location, get_animals_by_location, get_animal_by_status
from urllib.parse import urlparse, parse_qs

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_animal(id)
                    if response is None:
                        self._set_headers(404)
                        response = {
                            "message": f"Animal {id} is out playing right now"}

                else:
                    self._set_headers(200)
                    response = get_all_animals()

            if resource == "locations":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_location(id)

                else:
                    self._set_headers(200)
                    response = get_all_locations()

            if resource == "employees":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_employee(id)

                else:
                    self._set_headers(200)
                    response = get_all_employees()

            if resource == "customers":
                if id is not None:
                    self._set_headers(200)
                    response = get_single_customer(id)

                else:
                    self._set_headers(200)
                    response = get_all_customers()
        else: # There is a ? in the path, run the query param functions
            (resource, query) = parsed
            self._set_headers(200)

            if query.get('email') and resource == 'customers':
                response = get_customers_by_email(query['email'][0])

            if query.get('location_id') and resource == 'animals':
                response = get_animals_by_location(query['location_id'][0])

            if query.get('location_id') and resource == 'employees':
                response = get_employee_by_location(query['location_id'][0])

            if query.get('status') and resource == 'animals':
                response = get_animal_by_status(query['status'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        response = {}

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.

        if resource == "animals":
            if "name" in post_body and "breed" in post_body and "location_id" in post_body and "customer_id" in post_body and "status" in post_body:
                self._set_headers(201)
                response = create_animal(post_body)
            else: 
                self._set_headers(400)
                response = {
                "message": f'{"please complete all required fields"}'
                }


        if resource == "locations":
            if "address" in post_body and "name" in post_body:
                self._set_headers(201)
                response = create_location(post_body)
            else:
                self._set_headers(400)
                response = {
                "message": f'{"name is required" if "name" not in post_body else ""}'f'{"address is required" if "address" not in post_body else ""}'
                }

        if resource == "employees":
            if "name" in post_body:
                self._set_headers(201)
                response = create_employee(post_body)
            else: 
                self._set_headers(400)
                response = {
                "message": f'{"please complete all required fields"}'
                }

        if resource == "customers":
            if "name" in post_body:
                self._set_headers(201)
                response = create_customer(post_body)
            else: 
                self._set_headers(400)
                response = {
                "message": f'{"please complete all required fields"}'
                }

        self.wfile.write(json.dumps(response).encode())

    # A method that handles any PUT request.ƒ

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        # Set a 204 response code
        response = {}

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            self._set_headers(204)
            delete_animal(id)

        if resource == "customers":
            self._set_headers(405)
            response = {"message": "deleting customers is unsupported"}

        if resource == "employees":
            self._set_headers(204)
            delete_employee(id)

        if resource == "locations":
            self._set_headers(204)
            delete_location(id)

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(response).encode())

        # A method that handles any PUT request.ƒ

    def do_PUT(self):
        """""Handles PUT requests to the server"""""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        # Delete a single animal from the list
        if resource == "animals":
            success = update_animal(id, post_body)

        if resource == "customers":
            success = update_customer(id, post_body)

        if resource == "employees":
            success = update_employee(id, post_body)

        if resource == "locations":
            success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(400)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
