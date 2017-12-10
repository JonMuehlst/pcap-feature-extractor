import numpy as np
from conf.conf import client_hello_num, server_hello_num, SSL3_V, TLS1_V, TLS11_V, TLS12_V, get_temp_folder, TCP_PROTOCOL, UDP_PROTOCOL


def num_keep_alive(container):
    """
    TCP keep alive packet count
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_df()
        ka_df = df[df['tcp.analysis.keep_alive'] == True]
        ans = len(ka_df)
        return ans
    else:
        return 0

def SSLv(container):
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
    if container.transport_protocol() == TCP_PROTOCOL:
        client_hello_pkt = container.get_client_hello()
        if not(client_hello_pkt.empty):
            ssl_version = client_hello_pkt['ssl.record.version'].iloc[0]
            hist = []
            if issubclass(type(ssl_version), str):
                hist = np.histogram(np.array(int(ssl_version,0)),
                                     bins=[ SSL3_V, TLS1_V, TLS11_V,
                                     TLS12_V-1, TLS12_V ])
            else:
                hist = np.histogram(np.array(ssl_version),
                                    bins=[ SSL3_V, TLS1_V,
                                    TLS11_V, TLS12_V-1, TLS12_V ])
            return hist[0]
    return [0,0,0,0]


def SSLv_no_bins(container):
    """
    # SSLv3/TLS versions
    No bins
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        client_hello_pkt = container.get_client_hello()
        if not(client_hello_pkt.empty):
            ssl_version = client_hello_pkt['ssl.record.version'].iloc[0]
            if issubclass(type(ssl_version), str):
                ssl_version = int(ssl_version,0)
            return ssl_version
    return 0


def cipher_suites(container):
    """
    Cipher suites length
    0-13, 13-17, 17-24

    Note: Each cipher suite is 2 bytes.
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        client_hello_pkt = container.get_client_hello()
        if not(client_hello_pkt.empty):
            cipher_suites = client_hello_pkt['ssl.handshake.cipher_suites_length'].iloc[0]/2
            hist = np.histogram(np.array(cipher_suites), bins=[ 0, 13, 17, 24 ])
            return hist[0]
    return [0,0,0]


def cipher_suites_no_bins(container):
    """
    Cipher suites length
    No bins, single value
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        client_hello_pkt = container.get_client_hello()
        if not(client_hello_pkt.empty):
            cipher_suites = client_hello_pkt['ssl.handshake.cipher_suites_length'].iloc[0]/2
            return len(cipher_suites)
    return 0


def SSL_num_compression_methods(container):
    """
    Client hello SSL number of compression methods
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_client_hello()
        if not(df.empty):
            return df['ssl.handshake.comp_methods_length'].iloc[0]
    return 0



def SSL_session_id_len(container):
    """
    Client hello SSL Session id length
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_client_hello()
        if not(df.empty):
            return df['ssl.handshake.session_id_length'].iloc[0]
    return 0


def SSL_num_extensions(container):
    """
    The number of SSL extensions in the client hello packet
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_client_hello()
        num_ext = len(df['ssl.handshake.extension.type'].iloc[0].split(','))
        return num_ext
    else:
        return 0


def SYN_tcp_winsize(container):
    """
    Return the SYN packets TCP window size value
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_syn_pkt()
        winsize_val = df['tcp.window_size']
        if not(winsize_val.empty):
            return winsize_val.iloc[0]
        return 65535
    return 0


def SYN_MSS(container):
    """
    Get the SYN packet Max Segment Size.

    If MSS is not set return 1500 - IPv4 header (20 bytes) - TCP header (20 bytes)
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_syn_pkt()
        mss = df['tcp.options.mss_val']
        if not(mss.empty):
            return mss.iloc[0]
        return 1460
    return 0



def SYN_tcp_scale(container):
    """
    Return the SYN packets TCP scale value.
    """
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_syn_pkt()
        scale_val = df['tcp.options.wscale.shift']
        if not(scale_val.empty):
            return scale_val.iloc[0]
    return 0



def time_plus_ip_port_tuple(container):
    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_df()
        # df = self.client_hello_pkt
        df = df.head(1)
        # print len(df)
        epoch_time = df['frame.time_epoch'].iloc[0]
        src_ip = df['ip.src'].iloc[0]
        src_port = df['tcp.srcport'].iloc[0]
        dst_ip = df['ip.dst'].iloc[0]
        dst_port = df['tcp.dstport'].iloc[0]
        id_str = str(epoch_time) + '-' + str(src_ip) + '-' \
                 + str(src_port) + '-' + str(dst_ip) + '-' + str(dst_port)
        # print id_str
        return id_str
    else:
        return float('nan')


def peak_features(container):
    """
    Peak features:
           peak mean
           peak min
           peak max
           peak std
           Number Of peaks

           peak inter arrival time std
           peak inter arrival time mean
           peak inter arrival time min
           peak inter arrival time max

    """
    feature_arr = np.zeros(9)

    if container.transport_protocol() == TCP_PROTOCOL:
        df = container.get_df()

        df['tcp.ack'].fillna(0)

        """ Add a column stating whether a certain packet represents a peak """
        df['isPeak'] = np.where(df['frame.time_delta'] > 0.05, True, False)

        """ A DataFrame containing only peak representing packets """
        peak_df = df[df['isPeak'] == True]

        """ Getting rid of RST packets which cause undesired behaviour (negative ack diffs)"""
        peak_df = peak_df[peak_df['tcp.flags.reset'] == False]

        """ For every trailing couple of peak representing packets (rows) compute the difference """
        peak_diff_ack = peak_df['tcp.ack'].diff()

        """ Peak inter arrival times """
        piat = peak_df['frame.time_epoch'].diff()

        """ Remove first value since peaks are num (representing) packets - 1 """
        peak_diff_ack = peak_diff_ack[1:]

        """ Same for piat """
        piat = piat[1:]

        if len(peak_df) > 0 :
            """ Features """

            peak_mean = 0
            peak_min = 0
            peak_max = 0
            peak_std = 0
            num_of_peaks = 0
            piat_mean = 0
            piat_min = 0
            piat_max = 0
            piat_std = 0


            if len(peak_diff_ack) > 0:
                if len(peak_diff_ack) == 1:
                    peak_mean = peak_diff_ack.values[0]
                    peak_min = peak_diff_ack.min()
                    peak_max = peak_diff_ack.max()
                    num_of_peaks = len(peak_diff_ack)
                else:
                    peak_mean = peak_diff_ack.mean()
                    peak_min = peak_diff_ack.min()
                    peak_max = peak_diff_ack.max()
                    peak_std = peak_diff_ack.std()
                    num_of_peaks = len(peak_diff_ack)

            if len(piat) > 0:
                if len(piat) == 1:
                    piat_mean = piat.values[0]
                    piat_min = piat.min()
                    piat_max = piat.max()
                else:
                    piat_mean = piat.mean()
                    piat_min = piat.min()
                    piat_max = piat.max()
                    piat_std = piat.std()

            feature_arr = np.array([peak_mean, peak_min, peak_max, peak_std, num_of_peaks, piat_mean, piat_min, piat_max, piat_std])


    return feature_arr
