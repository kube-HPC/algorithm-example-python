from __future__ import print_function, division, absolute_import
from hkube_python_wrapper import Algorunner
from algorithm import main as algorithm
def main():
    print("starting algorithm runner")
    Algorunner.Run(start=algorithm.start, stop=algorithm.stop)

if __name__ == "__main__":
    main()
