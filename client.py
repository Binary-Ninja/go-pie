"""The client side for Go Pie."""

# Third party library imports.
from podsixnet2.Connection import connection, ConnectionListener

# Local library imports.
from config import *
import pydeck as pd


class PieClient(ConnectionListener):
    """The client for the PieServer."""
    def __init__(self, scene, address=(DEFAULT_HOST, DEFAULT_PORT)):
        """Create new instance of a client and connect to the given server address."""
        # The game scene.
        self.scene = scene
        # Connect to the server address.
        self.Connect(address)
        # The client address is unknown until sent by the server.
        self.address = None
        # The player's hand.
        self.hand = pd.Stack()
        # The player id.
        self.player_id = None
        # The stats of all players.
        self.stats = []
        # Whether it is the player's turn.
        self.turn = False

    def get_address(self):
        """Returns the client address as a string "host:port".

        If the server has yet to confirm a valid connection, returns None."""
        return f"{self.address[0]}:{self.address[1]}" if self.address else None

    def pump(self):
        """Pump the network classes.

        Should be called once per game loop."""
        connection.Pump()
        self.Pump()

    def Network_connected(self, data):
        """This method is called upon connection to the server."""
        print(f"[Client] Connected to the server.")

    def Network_server_full(self, data):
        """This method is called when the server is full."""
        print("[Client] Server is full.")
        # Update client status.
        self.scene.update_client_status("Server full")
        # Quit client.
        self.quit()

    def Network_confirm_connect(self, data):
        """The server has confirmed it is valid."""
        # Store the address of the client.
        self.address = data['address']
        print(f"[Client] Confirmed address {self.get_address()}")
        # Update client status.
        self.scene.update_client_status("Waiting for players")

    def Network_start_game(self, data):
        """Receive the player's hand from the server."""
        self.player_id = data["id"]
        self.hand = pd.Stack(data["hand"])
        self.hand.sort()
        self.stats = data["stats"]
        # Update client status.
        self.scene.update_client_status("Not your turn")
        # Update client stats.
        self.scene.update_stats(self.stats)
        # Update client cards.
        self.scene.update_cards([card.rank for card in self.hand])

    def Network_hand_and_stats(self, data):
        """Refreshes the player's hand and stats."""
        self.hand = pd.Stack(data["hand"])
        self.hand.sort()
        self.stats = data["stats"]
        # Update client stats.
        self.scene.update_stats(self.stats)
        # Update client cards.
        self.scene.update_cards([card.rank for card in self.hand])

    def Network_turn(self, data):
        """It is this player's turn."""
        # Update scene.
        self.scene.update_client_status("Your turn: No card selected")
        self.scene.update_turn()

    def Network_game_over(self, data):
        """The game has ended."""
        self.scene.update_client_status("Game Over")

    def Network_error(self, data):
        """Log the socket errors that occur."""
        print(f"[Client] Error {data['error'][0]}: {data['error'][1]}")

    def Network_disconnected(self, data):
        """This method is called upon disconnection from the server."""
        if data.get("shutdown", False):
            # The disconnect was deliberate.
            print("[Client] Server shut down.")
            # Update client status.
            self.scene.update_client_status("Server shut down")
        else:
            # The disconnect was not planned.
            print(f"[Client] Disconnected from the server.")
            # Update client status.
            self.scene.update_client_status("Disconnected from server")
        # Quit client.
        self.quit()

    def quit(self):
        """Quit the client and exit the server.
        If the connection has been closed, this has no effect."""
        if connection.connected:
            print("[Client] Client shut down.")
            # Close connection to the server.
            connection.close()
