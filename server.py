"""The server side for Go Pie."""

# Third party library imports.
from podsixnet2.Channel import Channel
from podsixnet2.Server import Server

# Local library imports.
from config import *


class ClientChannel(Channel):
    """The server representation of a client."""

    def get_address(self):
        """Returns the client address as a string "host:port"."""
        return f"{self.addr[0]}:{self.addr[1]}"

    def Close(self):
        """Will be called upon client disconnection."""
        print(f"[Server] Client disconnected {self.get_address()}")
        # Remove self from the server's client list.
        self._server.channels.remove(self)


class PieServer(Server):
    """The server class for Go Pie."""
    def __init__(self, address=(DEFAULT_HOST, DEFAULT_PORT), players=2):
        """Initialize the server."""
        super().__init__(ClientChannel, address)
        # Save the server address.
        self.address = address
        print(f"[Server] Server started on {self.get_address()}")
        # The number of players to wait for.
        self.number_of_players = players

    def get_address(self):
        """Returns the server address as a string "host:port"."""
        return f"{self.address[0]}:{self.address[1]}"

    def pump(self):
        """Pump the network classes.

        Should be called once per game loop."""
        self.Pump()

    def Connected(self, client, address):
        """Accept the new client and send confirmation data."""
        # Log the connection.
        print(f"[Server] New connection from {client.get_address()}")
        # Send a confirmation that this server is valid.
        client.Send({"action": "confirm_connect", "address": address})

    def quit(self):
        """Shut down the server."""
        # Tell the clients that the server has shut down.
        for client in self.channels:
            client.Send({"action": "disconnected", "shutdown": True})
        # Pump the quit messages to the clients.
        self.Pump()
        # Log the server shutting down.
        print("[Server] Shut down.")
        # Close the server.
        self.close()
