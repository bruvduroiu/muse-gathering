import argparse
import math
import time
import sys

from pythonosc import dispatcher
from pythonosc import osc_server

alpha = []
beta = []
gamma = []
theta = []
jaw = []

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip",
                            default="127.0.0.1",
                            help="The ip to listen  on")
        parser.add_argument("--port",
                            type=int,
                            default=5000,
                            help="The port to listen on")
        args = parser.parse_args()

        dispatcher = dispatcher.Dispatcher()
        dispatcher.map("/debug", print)
        dispatcher.map("/muse/elements/alpha_relative",
                lambda unused_addr, ch1, ch2, ch3, ch4 : alpha.append((ch1+ch2+ch3+ch4) / 4))
        dispatcher.map("/muse/elements/beta_relative",
                lambda unused_addr, ch1, ch2, ch3, ch4 : beta.append((ch1+ch2+ch3+ch4) / 4))
        dispatcher.map("/muse/elements/gamma_relative",
                lambda unused_addr, ch1, ch2, ch3, ch4 : gamma.append((ch1+ch2+ch3+ch4) / 4))
        dispatcher.map("/muse/elements/theta_relative",
                lambda unused_addr, ch1, ch2, ch3, ch4 : theta.append((ch1+ch2+ch3+ch4) / 4))
        dispatcher.map("/muse/elements/jaw_clench",
                lambda unused_addr, val : jaw.append(val))

        server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        server.serve_forever()
    except KeyboardInterrupt:
        orig_stdout = sys.stdout
        f = open('out.txt', 'w')
        sys.stdout = f
        print ("alpha:{}".format(alpha))
        print ("beta:{}".format(beta))
        print ("gamma:{}".format(gamma))
        print ("theta:{}".format(theta))
        print ("jaw:{}".format(jaw))

        sys.stdout = orig_stdout
        f.close()
