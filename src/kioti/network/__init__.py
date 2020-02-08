import collections

Network = collections.namedtuple('Environment', 'networkMapURL networkTrustStore networkTruststorePassword doormanUrl')

class Networks():
    """Class to hold static information on the supported test networks."""

    default = Network('http://kioti.network.com:10001', 'kioti-network-root-truststore.jks', 'password', 'http://kioti.network.com:10001')

