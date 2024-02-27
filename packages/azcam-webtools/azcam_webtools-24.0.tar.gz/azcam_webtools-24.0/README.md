# azcam-webtools

*azcam-webtools* contains azcam web applications which interact with azcamserver over the web interface. Current functions include a status page and an exposure control page.

## Installation

`pip install azcam-webtools`

Or download from github: https://github.com/mplesser/azcam-webtools.git.

## Usage:

ToDo


# Working - In Progress

## Webserver Tool

This tool implements a FastAPI-based web server.  See https://fastapi.tiangolo.com.

```python
from azcam.tools.webserver.fastapi_server import WebServer
webserver = WebServer()
webserver.index = f"index_mysystem.html"
webserver.start()
```

## Browser-based Tools

These tools implements various browser-based tools which connect to an azcam web server.

### Usage

Open a web browser to an address such as http://localhost:2403/status, replacing `localhost`, `2403`, and `status` with the appropriate hostname, web server port number, and tool name.

### Supported Browser Tools
 - status - display current exposure status
 - exptool - a simple exposure control tool
