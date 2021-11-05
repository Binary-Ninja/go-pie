"""The server side for Go Pie."""

# Third-party library imports.
from podsixnet2.Channel import Channel
from podsixnet2.Server import Server


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

    # The server representation of a client class.
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        """Initialize the server."""
        super().__init__(*args, **kwargs)
        # Save the server address.
        self.address = kwargs["localaddr"]
        print(f"[Server] Server started on {self.address[0]}:{self.address[1]}")

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
        # Log the server shutting down.
        print("[Server] Shut down.")
        # Tell the clients that the server has shut down.
        for client in self.channels:
            client.Send({"action": "disconnected", "shutdown": True})
        # Pump the quit messages to the clients.
        self.Pump()
        # Close the server.
        self.close()
