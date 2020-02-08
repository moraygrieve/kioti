import re
from pysys.basetest import BaseTest
from pysys.utils.allocport import portIsInUse, tcpServerPortPool
from kioti.constants import CORDA_DISTRIBUTION, CORDA_ENT_DISTRIBUTION, CORDA_OS_DISTRIBUTION, ENVIRONMENT
from kioti.corda.node import NodeHelper
from kioti.corda.bootstrap import BootStrapper
from kioti.distribution import CordaType, CordaDistribution
from kioti.model.node import Notary

class CordaBaseTest(BaseTest):
    """The base test class for all Corda test scenarios.

    All subclasses of CordaBaseTest can be run in a variety of modes as specified in the top level pysysdirconfig.xml
    file. These modes follow the syntax (OS|ENT)-version format, and represent running against either OS and ENT Corda
    on a specific version. Should version be DEFAULT, the default version as configured in constants.py will be used.
    """
    DIST_REGEX = re.compile('(?P<type>(OS|ENT))-(?P<version>.*)$', re.M)

    def __init__ (self, descriptor, outsubdir, runner):
        """Construct an instance of a PySys base test specifically for testing Corda Nodes.

        :param descriptor: The descriptor for the test giving all test details
        :param outsubdir: The output subdirectory the test output will be written to
        :param runner: Reference to the runner responsible for executing the testcase
        """
        BaseTest.__init__(self, descriptor, outsubdir, runner)
        self.distribution = self.__parseMode()
        self.log.info('Corda distribution set to %s, %s' % (self.distribution.type.product, self.distribution.version))


    def __parseMode(self):
        """Return the distribution for a specific mode."""
        if self.mode is not None and self.DIST_REGEX.search(self.mode) is not None:
            type = re.match(self.DIST_REGEX, self.mode).group('type')
            version = re.match(self.DIST_REGEX, self.mode).group('version')
            if version == 'DEFAULT' and type == 'ENT': return CORDA_ENT_DISTRIBUTION
            elif version == 'DEFAULT' and type == 'OS': return CORDA_OS_DISTRIBUTION
            else: return CordaDistribution(CordaType.forType(type), version)
        return CORDA_DISTRIBUTION


    def getPort(self, portRange=None):
        """Find an unallocated port that is not in use.

        The {getPort} function allocates from a global pool of available ports, not in use by processes outside
        the scope of this running instance of PySys, or allocated to another process within the scope of this
        instance of PySys but yet to be run. Allocated ports are returned to a pool at testcase cleanup and as
        such all requests for an available port should be made through a call to this function.

        :param portRange: Tuple of low, high port values to select from
        :return: An available TCP port
        """
        if portRange is None:
            while True:
                port = tcpServerPortPool.popleft()
                if not portIsInUse(port):
                    self.addCleanupFunction(lambda: tcpServerPortPool.append(port))
                    return port
                else:
                    tcpServerPortPool.append(port)
        else:
            attempts = 0
            while True and attempts < 3:
                for port in range(portRange[0], portRange[1]):
                    try:
                        tcpServerPortPool.remove(port)
                        if not portIsInUse(port) :
                            self.addCleanupFunction(lambda: tcpServerPortPool.append(port))
                            return port
                        else:
                            tcpServerPortPool.append(port)
                    except: pass
                attempts+=1
            raise Exception('Unable to allocate port in requested range %d - %d' % (portRange[0], portRange[1]))


    def waitForNodeLog(self, node, expr="", timeout=10, condition=">=1", ignores=[]):
        """Wait for a log message condition in a node logfile.

        :param node: The node reference to wait on the log expression
        :param expr: The regular expression to search for in the text file
        :param condition: The condition to be met for the number of lines matching the regular expression
        :param ignores: A list of regular expressions used to denote lines in the files which should be ignored
        """
        self.waitForSignal(file=node.nodeLogfile, filedir=node.nodeLogdir, expr=expr, timeout=timeout, condition=condition, ignores=ignores)



class NetworkTest(CordaBaseTest):
    """The base test class for networked (using CENM) tests. """

    def startNode(self, name, network=ENVIRONMENT, distribution=None, database=None, cordapps=None):
        """Start a node running against a real network, returning a reference to the NodeHelper.

        The function creates the NodeHelper using the distribution for the test (default or mode) and
        against the environment specified. It performs the registration, copys any jars into the node
        cordapps directory using the copyjars function which takes a single parameter being the directory
        to copy to, and then runs up the node, returning a reference to it. Note that all nodes started
        are registered in the cleanup function of the testcase and therefore do not need to be explicitly
        stopped.

        :param name: The name of the node
        :param network: The network to run against
        :param distribution: The distribution of corda to use
        :param database: The database to use for the node vault (defaults to None so H2 used)
        :param cordapps: A list of cordapp wrappers used to copy over the jars and configure
        :return: An instance of net.corda.test.node.NodeHelper
        """
        if distribution is None: distribution = self.distribution
        node = NodeHelper.networkNode(name, testcase=self, distribution=distribution, network=network, database=database, cordapps=cordapps)
        node.prepare()
        node.register()
        return node.run()


class BootstrapTest(CordaBaseTest):
    """The base test class for local (bootstrapped) network tests. """

    def __init__ (self, descriptor, outsubdir, runner):
        """Construct an instance of a PySys base test specifically for testing Corda Nodes.

        :param descriptor: The descriptor for the test giving all test details
        :param outsubdir: The output subdirectory the test output will be written to
        :param runner: Reference to the runner responsible for executing the testcase
        """
        CordaBaseTest.__init__(self, descriptor, outsubdir, runner)
        self.participants = []
        self.addCleanupFunction(self.stopNetwork)


    def localNode(self, name, distribution=None, database=None, cryptoService=None, notary=None, cordapps=None):
        """Create a NodeHelper ready for running against a development local network.

        Creates a NodeHelper ready for bootstrapping, adds a name.lower class instance attribute to
        reference the NodeHelper, and registers the node as being part of the network for top level
        network operations to be performed, e.g. starting and stopping the network.
        """
        node = NodeHelper.create(name, self, distribution, bootstrapped=True, network=None, database=database, cryptoService=cryptoService, notary=notary, cordapps=cordapps)
        setattr(self, node.name.lower(), node)
        self.participants.append(node)


    def localNetwork(self, nodes, notaries=None, cordapps=None):
        """Create a local bootstrapped network using default configurations.

        This convenience method creates default nodes and notaries based on the simple names
        passed in to the parameters. For each node or notary name, a NodeHelper is created and
        an instance attribute created to reference it i.e. for an entry in the node names of the
        form PartyA, an instance attribute of self.partya will be create reference the NodeHelper
        for that node. Once created the network can be bootstrapped and started using the normal
        methods of this class.

        :param nodes: A list of the node names
        :param notaries: A list of the notaries
        :param cordapps: A list of cordapp wrappers used to copy over the jars and configure
        """
        map(lambda x: self.localNode(name=x, cordapps=cordapps), nodes)
        map(lambda x: self.localNode(name=x, notary=Notary(False)), ([] if notaries is None else notaries))


    def bootstrapNetwork(self):
        """Bootstrap a network.

        The method first calls the prepare task of each node to ensure any external dependencies
        such as database containers are started. Once performed the bootstrapper is executed over the
        directory structure to create the network parameters and copies of the nodeInfos for each node.
        """
        map(lambda x: x.prepare(), self.participants)
        BootStrapper(self, distribution=self.distribution).run()


    def startNetwork(self, devMode=True):
        """Start registered nodes in the network.

        :param devMode: If false starts the network on non dev mode
        """
        map(lambda x: x.devMode(devMode), self.participants)
        map(lambda x: x.run(), self.participants)


    def stopNetwork(self):
        """Stop registered nodes in the network. """
        map(lambda x: x.stop(), self.participants)

