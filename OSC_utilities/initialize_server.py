import argparse
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc import dispatcher
import asyncio


def receiver(address, *args):

  function = args[0]
  value = args[-1]
  print(function, value)
  return(value)


dispatch = dispatcher.Dispatcher()
dispatch.map("/selected_instrument", receiver)
dispatch.map("/rec_toggle", receiver)



async def initialize_server():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port",
                        type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    server = AsyncIOOSCUDPServer(
        (args.ip, args.port), dispatch, asyncio.get_event_loop())
    # Create datagram endpoint and start serving
    transport, protocol = await server.create_serve_endpoint()
    return transport