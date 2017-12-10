"""
This class contains:
    1. Packet objects
    2. Methods which return information about a subset (or all) of the packets.
"""

class PacketContainer(object):

    # Class field - Packet container here

    def __init__(self):
        """
        self.list_of_packets
        or
        self.flows
        """


    def duration(self):
        """
        Length in seconds
        """
        pass


    def total_packets(self):
        """
        Total number of packets
        """
        pass


    def pl_total_packets(self):
        """
        Total number of packets with payload
        """
        pass


    def no_pl_total_packets(self):
        """
        Total number of packets without payload
        """
        pass


    def size(self):
        """
        Size of all packets in bytes
        """
        pass


    def __len__(self):
        """
        Amount of packets
        """
        pass


    def mean_packet_size(self):
        """
        Mean of packet size
        """
        pass


    def sizevar(self):
        """
        Variance of packet size
        """
        pass


    def max_packet_size(self):
        """
        Max packet size
        """
        pass


    def min_packet_size(self):
        """
        Min packet size 
        """
        pass
