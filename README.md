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
A file named `config.json` holds the default settings.

- `"screen_resolution"` - The starting resolution of the display. The display can be resized.
- `"card_scale"` - The scaling of the card images. Can be adjusted per client.
- `"default_host"` - The default host for servers and clients.
- `"default_port"` - The default port for servers and clients.
- `"public_server"` - A boolean that specifies whether to use `pyngrok` to open the server publicly.

## Key Commands
Press ESC to exit the game.
Use the UP and DOWN arrow keys while playing to scale your cards UP and DOWN.
