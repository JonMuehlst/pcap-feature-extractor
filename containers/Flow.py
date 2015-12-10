#inherits from Packet_container
from PacketContainer import PacketContainer
from Packet import Packet

class Flow(PacketContainer):

    # Class field - Packet container here
    packet_list = []
    start_time = 0
    times = []
    time_deltas = []
    size_array = []
    df = None
    
    def __init__(self, p):
        self.df = p
        
    def get_df(self):
	return self.df

    """ FIX """
    def generate_times(self):
        pass
    
    """  """
    def generate_time_deltas(self):
        pass
    
    """ Length in seconds """
    def duration(self):
        pass
    
    """ Total number of packets with payload """
    def pl_total_packets(self):
        pass
    
    """ Total number of packets without payload """
    def no_pl_total_packets(self):
        pass
    
    """ Size of all packets in bytes """
    def size(self):
        return self.df['tcp.len'].sum()
    
    """ Amount of packets """
    def __len__(self):
        return len(self.df)
    
    """ Mean of packet size """
    def sizemean(self):
        return self.df['tcp.len'].mean()
    
    """ Variance of packet size """
    def sizevar(self):
        return self.df['tcp.len'].var()
    
    """ ADD TO PACKET CONTAINER INTERFACE"""
    """ Max packet size """
    def max_packet_size(self):
        pass
    
    """ ADD TO PACKET CONTAINER INTERFACE"""
    """ Min packet size """
    def min_packet_size(self):
        return self.df['tcp.len'].min()
    
    
