import TCP
import Statistical as sts
from containers.Session import Session
import numbers
import numpy as np

def fpackets(container):
    """
    # Packets in forward direction (fpackets)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return len(flow_up)


def bpackets(container):
    """
    # Packets in backward direction (bpackets)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return len(flow_down)


def fbytes(container):
    """
    # Bytes in forward direction (fbytes)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.size(flow_up)


def bbytes(container):
    """
    # Bytes in backward direction (bbytes)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.size(flow_down)


def min_fiat(container):
    """
    Min forward inter-arrival time (min_fiat)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.min_time_delta(flow_up)


def min_biat(container):
    """
    Min backward inter-arrival time (min_biat)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.min_time_delta(flow_down)


def max_fiat(container):
    """
    Max forward inter-arrival time (max_fiat)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.max_time_delta(flow_up)


def max_biat(container):
    """
    Max backward inter-arrival time (max_biat)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.max_time_delta(flow_down)


def std_fiat(container):
    """
    Standard deviation of forward inter- arrival times (std_fiat)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.std_time_delta(flow_up)


def std_biat(container):
    """
    Standard deviation of backward inter- arrival times (std_biat)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.std_time_delta(flow_down)


def mean_fiat(container):
    """
    Mean forward inter-arrival time (mean_fiat)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.mean_time_delta(flow_up)


def mean_biat(container):
    """
    Mean backward inter-arrival time (mean_biat)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.mean_time_delta(flow_down)


def min_fpkt(container):
    """
    Min forward packet length (min_fpkt)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.min_packet_size(flow_up)


def min_bpkt(container):
    """
    Min backward packet length (min_bpkt)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.min_packet_size(flow_down)


def max_fpkt(container):
    """
    Max forward packet length (max_fpkt)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.max_packet_size(flow_up)


def max_bpkt(container):
    """
    Max backward packet length (max_bpkt)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.max_packet_size(flow_down)


def std_fpkt(container):
    """
    Std deviation of forward packet length (std_fpkt)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.std_packet_size(flow_up)


def std_bpkt(container):
    """
    Std deviation of backward packet length (std_bpkt)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.std_packet_size(flow_down)


def mean_fpkt(container):
    """
    Mean forward packet length (mean_fpkt)
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return sts.mean_packet_size(flow_up)


def mean_bpkt(container):
    """
    Mean backward packet length (mean_bpkt)
    """
    if isinstance(container, Session):
        flow_down = container.get_flow_down()
        return sts.mean_packet_size(flow_down)

"""
Our features
"""

def get_mean_ttl(container):
    df = container.get_df()
    if len(df) == 0:
        return 0
    if len(df) == 1:
        return df['ip.ttl'].values[0]
    return df['ip.ttl'].mean()


def mean_fttl(container):
    """
    Discretized upstream TTL values.
    Assuming Two bins: 0-64, 65-128
    """
    if isinstance(container, Session):
        mean_ttl = get_mean_ttl(container.get_flow_up())
        if mean_ttl <= 64:
            return np.array([1,0])
        elif mean_ttl > 64:
            return np.array([0,1])
    else:
        return np.array([0,0])


def mean_fttl_no_bins(container):
    """
    Upstream TTL value.
    No bins
    """
    if isinstance(container, Session):
        mean_ttl = get_mean_ttl(container.get_flow_up())
        if isinstance(mean_ttl, numbers.Number):
            return mean_ttl
    return 0

def fpeak_features(container):
    """
    Forward peak features
    """
    if isinstance(container, Session):
        return TCP.peak_features(container.get_flow_up())


def bpeak_features(container):
    """
    Backward peak features
    """
    if isinstance(container, Session):
        return TCP.peak_features(container.get_flow_down())

"""=================================================="""

def num_keep_alive(container):
    """
    TCP keep alive packet count

    If no such packets exist (i.e. 0) This might indicate usage of IExplorer.

    Notice the usage of 'tcp.analysis.keep_alive' which are requests from the client to the server.
    """
    if isinstance(container, Session):
        flow_up = container.get_flow_up()
        return TCP.num_keep_alive(flow_up)

def fSSLv(container):
    """
    # SSLv3/TLS versions
    SSL3_V = 0x0300
    TLS1_V = 0x0301
    TLS11_V = 0x0302
    TLS12_V = 0x0303

    ssl3   tls1  tls11 tls12
    [0,    0,    0,    1]

    Client to server - SSL version array
    """
    return TCP.SSLv(container)


def fSSLv_no_bins(container):
    """
    # SSLv3/TLS versions
    No bins
    """
    return TCP.SSLv_no_bins(container)


def fcipher_suites(container):
    """
    Cipher suites length
    0-13, 13-17, 17-24

    Note: Each cipher suite is 2 bytes.
    """
    return TCP.cipher_suites(container)


def fcipher_suites_no_bins(container):
    """
    Cipher suites length
    No bins, single value
    """
    return TCP.cipher_suites_no_bins(container)


def fSSL_num_compression_methods(container):
    """
    Client hello SSL number of compression methods
    """
    return TCP.SSL_num_compression_methods(container)



def fSSL_session_id_len(container):
    """
    Client hello SSL Session id length
    """
    return TCP.SSL_session_id_len(container)


def fSSL_num_extensions(container):
    """
    The number of SSL extensions in the client hello packet
    """
    return TCP.SSL_num_extensions(container)
