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
        # Initialize the player info.
        self.hand = pd.Stack()
        # The tricks taken as a list of ranks.
        self.tricks = []

    def get_address(self):
        """Returns the client address as a string "host:port"."""
        return f"{self.addr[0]}:{self.addr[1]}"

    def Network_ask(self, data):
        """Called when a player asks another for a card."""
        print(f"[Server] {self.get_address()} asked player {data['player']} for {data['rank']}s.")

    def Close(self):
        """Will be called upon client disconnection."""
        print(f"[Server] Client disconnected {self.get_address()}")
        # Remove self from the server's client list if not a player.
        # Removing player clients will cause problems.
        if self not in self._server.players:
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
        # The list of playing clients.
        self.players = []
        # The deck of the game.
        self.deck = pd.new_deck(shuffle=True)
        # Whether the game is playing.
        self.playing = False

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
            # Start playing the game.
            self.playing = True
            self.players = list(self.channels)
            # Deal hands and send out the start data.
            # Does not deal with tricks in starting hands.
            for player in self.players:
                player.hand = self.deck.deal(6)
            # Calculate the game stats.
            stats = [(len(player.hand), player.tricks) for player in self.players]
            # Send the start game information to all players.
            for player in self.players:
                player.Send({"action": "start_game",
                             "id": self.players.index(player),
                             "hand": [str(card) for card in player.hand],
                             "stats": stats,
                             })
            # Tell the first player it's their turn.
            self.players[0].Send({"action": "turn"})

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
