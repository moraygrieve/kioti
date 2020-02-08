import socket
from copy import deepcopy
from pysys.constants import BACKGROUND, PASSED
from pysys.utils.filecopy import filecopy
from pysys.utils.fileutils import deletedir
from kioti.constants import *
from kioti.distribution.artifact import getCordaArtifact
from kioti.database import getDriver
from kioti.model.node import NodeConfig
from kioti.container import DatabaseContainers
from kioti.utils.dname import DistinguisedName

class NodeHelper:
    """Class abstraction over a Corda Node.

    NodeHelper is designed for use by an instance of a CordaBaseTest class or extension. The class can
    be constructed with static class methods to create a node ready for bootstrapping for a local
    development network, or ready for running against a remote network. An instance of the class should
    relate to a single logical instance of a node, though it may be used to start the node multiple times
    e.g. when running an initial registration against a remote network, or when stopping and restarting.
    """

    @classmethod
    def create(cls, name, testcase, distribution, bootstrapped, network=None, database=None, cryptoService=None, notary=None, cordapps=None):
        """Create a NodeHelper ready for real or bootstrapped network.

        :param name: The logical name of  the node entity
        :param testcase: A reference to the owning testcase
        :param distribution: The distribution of Corda to use
        :param bootstrapped: If True this is for bootstrapping
        :param network: A reference to the network to run against
        :param database: The database type to use for the node vault (defaults H2)
        :param cryptoService: The cryptoservice to use (HSM)
        :param notary: If this node is to be a notary
        :param cordapps: A list of cordapp wrappers used to copy over the jars and configure
        """
        if distribution is None: distribution = testcase.distribution
        node = NodeHelper(name, testcase, distribution, network, database)

        # write the node configuration to the node directory
        node.config = NodeConfig.init(name, testcase, devMode=bootstrapped)
        node.config.withDatabase(testcase, distribution.isOS(), node.database, node.database_port)
        node.config.withNetworkServices(network) if network is not None else None
        node.config.withCryptoService(cryptoService.name, cryptoService.conf) if cryptoService is not None else None
        node.config.withNotary(notary.validating) if notary is not None else None

        # create the node directory structure and write out the node configuration file
        os.makedirs(node.directory)
        os.makedirs(os.path.join(node.directory, 'drivers'))
        os.makedirs(os.path.join(node.directory, 'cordapps'))
        node.config.write(os.path.join(node.directory, 'node.conf'))

        # copy over any cordapps or drivers
        map(lambda x: x.copyjars(os.path.join(node.directory, 'cordapps')), cordapps if cordapps is not None else [])
        if database is not None: filecopy(getDriver(database), os.path.join(node.directory, 'drivers', database.driver))

        # corda jar will be taken as requested from the distribution
        filecopy(getCordaArtifact(distribution, 'corda'), os.path.join(node.directory, 'corda.jar'))
        node.jar = os.path.join(node.directory, 'corda.jar')
        return node


    @classmethod
    def localNode(cls, name, testcase, distribution=None, database=None, cryptoService=None, notary=None, cordapps=None):
        """Create a NodeHelper ready for running against a development local network."""
        return cls.create(name, testcase, distribution, bootstrapped=True, network=None, database=database, cryptoService=cryptoService, notary=notary, cordapps=cordapps)


    @classmethod
    def networkNode(cls, name, testcase, network, distribution=None, database=None, cryptoService=None, notary=None, cordapps=None):
        """Create a NodeHelper ready for running against a remote network."""
        return cls.create(name, testcase, distribution, bootstrapped=False, network=network, database=database, cryptoService=cryptoService, notary=notary, cordapps=cordapps)


    def __init__(self, name, testcase, distribution, network, database=None):
        """Class constructor.

        :param name: The logical name of the Corda node
        :param testcase: The testcase managing the Corda node
        :param distribution: The distribution of Corda to use
        :param network: The network to run against (None is bootstrapped)
        :param database: The database for the node to use (H2 or container)
        """
        self.name = name
        self.distribution = distribution
        self.network = network
        self.database = database
        self.database_port = database.getMappedPort(testcase) if database is not None else None
        self.environs = deepcopy(os.environ)
        self.processes = []
        self.testcase = testcase
        self.log = testcase.log
        self.addCleanupFunction = testcase.addCleanupFunction
        self.startProcess = testcase.startProcess
        self.waitForSignal = testcase.waitForSignal
        self.directory = os.path.join(testcase.output, name)
        self.nodeLogfile = 'node-%s.log' % socket.gethostname()
        self.nodeLogdir = os.path.join(self.directory,'logs')
        self.nodeLog = os.path.join(self.nodeLogdir, self.nodeLogfile)
        self.addCleanupFunction(self.clean)


    def clean(self):
        """Remove large files and folders if the test passes"""
        if self.testcase.getOutcome() == PASSED:
            self.log.info('Purging node %s output directory of large files' % self.name)
            os.remove(self.jar)
            map(lambda x: deletedir(os.path.join(self.directory, x)), ['artemis', 'brokers'])


    def prepare(self):
        """Prepares the node helper for running (starts database contained, registers cleanup functions)."""
        if self.database is not None and DatabaseContainers.forType(self.database) is not None:
            clazz = DatabaseContainers.forType(self.database)
            container = clazz('%s-db' % DistinguisedName.getOrganisation(self.config.myLegalName), self.testcase, self.database, self.database_port)
            self.addCleanupFunction(container.stop)
            container.run()
        self.addCleanupFunction(self.stop)


    def devMode(self, mode=False):
        """Set the devMode of the node configuration and write to the node.conf.

        :param mode: The value for devMode (True|False)
        """
        self.config.devMode=mode
        self.config.write(os.path.join(self.directory, 'node.conf'))


    def upgrade(self, distribution):
        """Set the node jar file to a new distribution version of Corda.

        This method downloads the requested distribution of Corda if it is not available, and
        sets the node jar file to reference this. In order to perform the upgrade, the node
        should be stopped and then restarted.

        :param distribution: The new distribution to upgrade to
        """
        self.distribution = distribution
        filecopy(getCordaArtifact(distribution, self.jar))


    def register(self):
        """Initialise the node by running an initial-registration with the identity manager.

        :return: A reference to this instance (useful in a builder paradigm)
        """
        assert(self.network is not None)

        self.log.info('Performing initial registration for corda %s' % self.name)
        stdout = os.path.join(self.directory, 'corda-init.out')
        stderr = os.path.join(self.directory, 'corda-init.err')

        arguments = ['-jar', self.jar]
        arguments.append('initial-registration')
        arguments.append('--log-to-console')
        arguments.append('--network-root-truststore=%s' % (os.path.join(KEYS, self.network.networkTrustStore)))
        arguments.append('--network-root-truststore-password=%s' % (self.network.networkTruststorePassword))

        process = self.startProcess(command=PROJECT.JAVA, displayName='corda', workingDir=self.directory,
                                    environs=self.environs, arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)
        self.waitForSignal(stdout, expr='Successfully registered Corda node with compatibility zone', timeout=180)
        self.processes.append(process)
        return self


    def run(self, logToConsole=False):
        """Run up the node loading any CorDapps in the cordapp directory.

        :param logToConsole: If true redirect the node log messages to stdout
        :return: A reference to this instance (useful in a builder paradigm)
        """
        self.log.info('Starting corda %s' % self.name)
        stdout = os.path.join(self.directory, 'corda-run.out')
        stderr = os.path.join(self.directory, 'corda-run.err')

        arguments = ['-jar', self.jar]
        if logToConsole: arguments.append('--log-to-console')
        process = self.startProcess(command=PROJECT.JAVA, displayName='corda', workingDir=self.directory,
                                    environs=self.environs, arguments=arguments, stdout=stdout, stderr=stderr, state=BACKGROUND)
        self.waitForSignal(stdout, expr='Node for.*started up and registered', timeout=180)
        self.processes.append(process)
        return self


    def stop(self, timeout=180):
        """Stop any running nodes started by this instance, by sending a soft kill via a SIGTERM.

        :param timeout: The timeout period to wait for the corda to terminate
        """
        map(lambda x: self.__stopOne(x, timeout), self.processes)


    def __stopOne(self, process, timeout):
        """Soft kill a single running process.

        :param process: A handle to the running process
        :param timeout: The timeout period to wait for the corda to terminate
        """
        if process.running():
            self.log.info('Stopping node %s with process id %d' % (self.name, process.pid))
            process.stop(timeout=timeout)
