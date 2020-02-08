import collections

Network = collections.namedtuple('Environment', 'networkMapURL networkTrustStore networkTruststorePassword doormanUrl')

class Networks():
    """Class to hold static information on the supported test networks."""

    daywatch = Network('http://day3-netmap.cordaconnect.io:10001', 'daywatch-network-root-truststore.jks', 'password', 'http://day3-doorman.cordaconnect.io:10001')
    nightwatch = Network('http://night1.cordaconnect.io:10001', 'nightwatch-network-root-truststore.jks', 'password', 'http://night1.cordaconnect.io:10001')
    nightwatchv4 = Network('http://night4-netmap.cordaconnect.io:10001', 'nightwatchv4-network-root-truststore.jks', 'password', 'http://night4-doorman.cordaconnect.io:10001')

