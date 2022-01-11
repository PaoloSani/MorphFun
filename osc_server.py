"""
OSC Server
"""
import argparse

from pythonosc import dispatcher
from pythonosc import osc_server

def print_whole_message(address, *args):
    print(f"{address}: {args}")


def receiver(address, *args):

  function = args[0]
  value = args[-1]
  print(function, value)
  return(value)

  

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/selected_instrument", receiver)
  dispatcher.map("/rec_toggle", receiver)

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))

  
  server.serve_forever()