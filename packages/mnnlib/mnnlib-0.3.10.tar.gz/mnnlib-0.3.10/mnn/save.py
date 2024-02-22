from mnn import network
import pickle


class save: 
  """
  saves the network to a mnn model file
  """
  def __init__(self,net:network):
    self.net = net


  def save(self,file_name:str):
    """
    saves to a file
    """
    with open(file_name,"wb") as f:
      pickle.dump(self.net, f)