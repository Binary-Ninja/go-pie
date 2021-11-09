"""The client side for Go Pie."""

# Third party library imports.
from podsixnet2.Connection import connection, ConnectionListener

# Local library imports.
from config import *


class PieClient(ConnectionListener):
    """The client for the PieServer."""
    def __init__(self, address=(DEFAULT_HOST, DEFAULT_PORT)):
        """Create new instance of a client and connect to the given server address."""
        # Connect to the server address.
        self.Connect(address)
        # The client address is unknown until sent by the server.
        self.address = None

    def get_address(self):
        """Returns the client address as a string "host:port".

        If the server has yet to confirm a valid connection, returns "None"."""
        return f"{self.address[0]}:{self.address[1]}" if self.address else None

    def pump(self):
        """Pump the network classes.

        Should be called once per game loop."""
        connection.Pump()
        self.Pump()

    def Network_connected(self, data):
        """This method is called upon connection to the server."""
        print(f"[Client] Connected to the server.")

    def Network_confirm_connect(self, data):
        """The server has confirmed it is valid."""
        # Store the address of the client.
        self.address = data['address']
        print(f"[Client] Confirmed address {self.get_address()}")

    def Network_error(self, data):
        """Log the socket errors that occur."""
        print(f"[Client] Error {data['error'][0]}: {data['error'][1]}")
        print(data)

    def Network_disconnected(self, data):
        """This method is called upon disconnection from the server."""
        if data.get("shutdown", False):
            # The disconnect was deliberate.
            print("[Client] Server shut down.")
        else:
            # The disconnect was not planned.
            print(f"[Client] Disconnected from the server.")
        # Close connection to the server.
        connection.close()

    def quit(self):
        """Quit the client and exit the server."""
        print("[Client] Client shut down.")
        # Close connection to the server.
        connection.close()
