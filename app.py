import os
import logging
import sys
from hkube_python_wrapper import Algorunner
from config import Config

import algorithm.main as algorithm

def main():
    logging.info("starting algorithm runner")
    alg = Algorunner()
    alg.loadAlgorithmCallbacks(algorithm.start)
    alg.connectToWorker(Config.socket)
    alg.run()

if __name__ == "__main__":
    logging.basicConfig(level=0,format='%(relativeCreated)6d %(threadName)s %(message)s', stream=sys.stdout)

    main()