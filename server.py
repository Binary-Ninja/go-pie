"""The server side for Go Pie."""

# Third party library imports.
from podsixnet2.Channel import Channel
from podsixnet2.Server import Server

# Local library imports.
from config import *
import pydeck as pd


class ClientChannel(Channel):
    """The server representation of a client."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand = pd.Stack()

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
        self.max_clients = players
        # The deck of the game.
        self.deck = pd.new_deck(shuffle=True)

    def get_address(self):
        """Returns the server address as a string "host:port"."""
        return f"{self.address[0]}:{self.address[1]}"

    def pump(self):
        """Pump the network classes.

        Should be called once per game loop."""
        self.Pump()

    def send_all(self, data):
        """Sends the network data to all clients in channel list."""
        [client.Send(data) for client in self.channels]

    def Connected(self, client, address):
        """Accept the new client and send confirmation data."""
        # Log the connection.
        print(f"[Server] New connection from {client.get_address()}")
        # Only accept a certain number of clients.
        if len(self.channels) > self.max_clients:
            client.Send({"action": "server_full"})
        else:
            # Send a confirmation that this server is valid.
            client.Send({"action": "confirm_connect", "address": address})
        # Start the game.
        if len(self.channels) == self.max_clients:
            for client in self.channels:
                client.hand = self.deck.deal(5)
                client.Send({"action": "start_game", "hand": [str(card) for card in client.hand]})

    def quit(self):
        """Shut down the server."""
        # Tell the clients that the server has shut down.
        self.send_all({"action": "disconnected", "shutdown": True})
        # Pump the quit messages to the clients.
        self.Pump()
        # Log the server shutting down.
        print("[Server] Shut down.")
        # Close the server.
        self.close()
