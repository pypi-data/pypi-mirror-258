from mnn import network,layer,weight
from mnn.activations import relu,sigmoid,straight,binary,leakyrelu
import pickle
from mnn.constants import VERSION
import logging


def geta(a:str):
  logger = logging.getLogger("mnn.load")
  a = a.strip()
  match a:
    case "relu":
      return relu
    case "sigmoid":
      return sigmoid
    case "straight":
      return straight
    case "binary":
      return binary
    case "leakyrelu":
      return leakyrelu
  logger.warn("Unknown activation function: '%s' using straight as default " % a)
  return straight
      
    

class load:
  """
  used to load mnn model files
  """
  def __init__(self,file_name:str):
    self.logger = logging.getLogger("mnn.load")
    self.file_name = file_name


  def load(self):
    """
    loads the network from the file
    returns network class
    """
    with open(self.file_name,"rb") as f:
      net = pickle.load(f)
      if net.version != VERSION:
        self.logger.warn(f"Version mismatch, file version: {net.version}, current version: {VERSION}")
      return net