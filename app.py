import os
from hkube_python_wrapper import Algorunner
from config import Config

import algorithm.main as algorithm

def main():
    print("starting algorithm runner")
    alg = Algorunner()
    alg.loadAlgorithmCallbacks(algorithm.start)
    job = alg.connectToWorker(Config.socket)
    job.join()

if __name__ == "__main__":
    main()