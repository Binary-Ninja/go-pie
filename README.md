# go-pie
The Hack-A-Thon Go Pie game.

## Requirements

### Python
This application was built on Python 3.9.7 and uses features exclusive to the 3.9 series and above.

### pygame 2.0.3
`pip install pygame`

Pygame 2 is an SDL2 wrapper for Python.

### pyngrok 5.1.0 (Optional)
`pip install pyngrok`

This library allows localhost ports to be opened to the internet and made public.
Without this library, you cannot host public servers from localhost.
All other functionality remains available.

If you create an [ngrok account](https://ngrok.com/) and install your user auth token in the default path
according to the instructions in the [docs](https://ngrok.com/docs#getting-started-authtoken),
pyngrok should be able to find your token. This will allow your public servers to never expire.


## The Config File
As there is no GUI for the application yet, a file named `config.json` holds the required data.

- `"screen_resolution"` - The starting resolution of the display. The display can be resized.
- `"default_port"` - The port on localhost that servers will be created on.
- `"public_server"` - A boolean that specifies whether to use `pyngrok` to open the server publicly.
- `"server_address"` - A string of the form `"host:port"` that specifies what IP to connect to as a client.

## Controls
Close the window to exit the program.

Press `H` to create a server on localhost and join a client to that server.
The server's port can be specified in the config file.
The server will be opened publicly if specified in the config file.

Press `J` to create a client and join the server address in the config file.

Press `Q` to quit the server and/or client that is running.