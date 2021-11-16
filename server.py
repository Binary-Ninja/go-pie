"""The server side for Go Pie."""

# Third party library imports.
from podsixnet2.Channel import Channel
from podsixnet2.Server import Server

# Local library imports.
from config import *
import pydeck as pd


class DummyPlayer:
    """Ignore this class, but don't delete it or the PieServer.player_ask method will crash."""
    connected = False


class ClientChannel(Channel):
    """The server representation of a client."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The player id.
        self.player_id = None
        # Initialize the player info.
        self.hand = pd.Stack()
        # The tricks taken as a list of ranks.
        self.tricks = []

    def get_address(self):
        """Returns the client address as a string "host:port"."""
        return f"{self.addr[0]}:{self.addr[1]}"

    def Network_ask(self, data):
        """Called when a player asks another for a card."""
        self._server.player_ask(self, data["player"], data["rank"])

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
        # The player whose turn it is.
        self.turn = 0
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
            for player_id, player in enumerate(self.players):
                player.player_id = player_id
                player.hand = self.deck.deal(6)
                self.update_tricks(player)
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
            self.players[self.turn].Send({"action": "turn"})

    def update_tricks(self, player: ClientChannel):
        """Searches given player's hand for tricks and updates accordingly."""
        ranks = {card.rank for card in player.hand}
        for rank in ranks:
            # Four cards of a same rank equal a trick.
            if len(player.hand.get(rank)) == 4:
                # Remove the cards from player's hand.
                player.hand.remove(rank)
                # Add to the player's tricks list.
                player.tricks.append(rank)

    def update_empty(self, player: ClientChannel):
        """Checks given player's hand for emptiness and refills from deck."""
        if player.hand.is_empty():
            player.hand = self.deck.deal(6)

    def player_ask(self, player_asking: ClientChannel, player_id: int, rank: str):
        """Player has asked another player for a specific rank."""
        print(f"[Server] Player {player_asking.player_id} asked player {player_id} for {rank}s.")
        # Do all the go fish logic.
        player_asked = self.players[player_id]

        if cards := player_asked.hand.get(rank):
            print(f"[Server] Player {player_asking.player_id} gets {len(cards)} {rank}s.")
            # Remove the cards from the asked player's hand.
            player_asked.hand.remove(rank)
            self.update_empty(player_asked)
            self.update_tricks(player_asked)
            # Add the cards to the asking player's hand.
            player_asking.hand.add_list(cards)
            self.update_tricks(player_asking)
            self.update_empty(player_asking)
            self.update_tricks(player_asking)
            # Continue the turn.
            player_asking.Send({"action": "turn"})
        else:
            print(f"[Server] Player {player_asking.player_id} goes fish.")
            if not self.deck.is_empty():
                # Add a card to the player's hand from the deck.
                card = self.deck.deal(1)[0]
                player_asking.hand.add(card)
                self.update_tricks(player_asking)
                self.update_empty(player_asking)
                self.update_tricks(player_asking)

                if card.rank == rank:
                    print(f"[Server] Player {player_asking.player_id} gets a {rank}.")
                    # Continue the turn.
                    player_asking.Send({"action": "turn"})
                    # Update the players.
                    stats = [(len(player.hand), player.tricks) for player in self.players]
                    for player in self.players:
                        player.Send({"action": "hand_and_stats",
                                     "hand": [str(card) for card in player.hand],
                                     "stats": stats,
                                     })
                    # Leave the function early to avoid turn counter.
                    return
            else:
                print("[Server] The deck is empty.")

            # Switch turns to the next player.
            player = DummyPlayer
            # Only send the turn signal to valid players.
            # Only loop around a certain number of times.
            for _ in range(self.max_clients):
                if not player.connected or player.hand.is_empty():
                    # Skip this player.
                    self.turn += 1
                    self.turn %= self.max_clients
                    player = self.players[self.turn]
                else:
                    # Use this player.
                    break

            # Send the turn action or end the game.
            if player is DummyPlayer:
                # End the game.
                self.send_all({"action": "game_over"})
            else:
                # Tell the next player to take their turn.
                player.Send({"action": "turn"})

        # Update the players.
        stats = [(len(player.hand), player.tricks) for player in self.players]
        for player in self.players:
            player.Send({"action": "hand_and_stats",
                         "hand": [str(card) for card in player.hand],
                         "stats": stats,
                         })

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
