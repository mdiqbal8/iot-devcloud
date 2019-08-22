from openvino.inference_engine import IENetwork
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument("-x", "--xml", help="Path to an .xml file with a trained model.", required=True, type=str)
parser.add_argument("-b", "--bin", help="Path to an .bin file with a trained model.", required=True, type=str)
args = parser.parse_args()

# There are no ways to obtain the supported versions from OpenVINO. 
# So we simply try to load it, and exit with non-zero if we can't load it.
try:
  net = IENetwork(model=args.xml, weights=args.bin)
  print("model is compatible")
except RuntimeError:
  print("model is not compatible")
  sys.exit(1)

