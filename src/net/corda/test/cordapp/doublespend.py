from copy import deepcopy
from pysys.utils.filecopy import filecopy
from net.corda.test.constants import *
from net.corda.test.cordapp.sshclient import CorDappSSHClient

class DoublespendCorDapp():
    """Utility class around the Doublespend Test CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        jars = [os.path.join(CORDAPPS_DIR, 'doublespend', 'staging', 'doublespend-contracts.jar')]
        jars.append(os.path.join(CORDAPPS_DIR, 'doublespend', 'staging', 'doublespend-workflows.jar'))
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), jars)


class DoublespendSSHClient(CorDappSSHClient):
    """Abstraction over ssh command interaction with the Doublespend Test CorDapp."""

    pass


class DoublespendRPCClient():
    """Utility class around the Doublespend CordApp RPC client application."""

    def __init__(self, testcase, distribution=CORDA_OS_DISTRIBUTION):
        """Class constructor.

        :param testcase: A reference to the owning testcase
        """
        self.log = testcase.log
        self.startProcess = testcase.startProcess
        self.distribution = distribution


    def defaultArgs(self, node, command):
        """Return default arguments to the RPC client.

        :param node: The node to execute the RPC command against
        :param command: The command name
        """
        arguments = ['-jar', os.path.join(CORDAPPS_DIR, 'doublespend', 'staging', 'doublespend-client.jar')]
        arguments.append(command)
        arguments.append(node.config.rpcSettings.address)
        arguments.append(node.config.rpcUsers[0].username)
        arguments.append(node.config.rpcUsers[0].password)
        return arguments


    def run(self, node, doubleSpendRatio=None, numberOfSpends=None, rngSeed=None, notary=None, timeout=None):
        """

        :param node: The node to execute the RPC command against
        :param doubleSpendRatio: The ratio of double spend attempts to spends, default 0.0 (no double spending)
        :param numberOfSpends: The number of spend operations, default 1
        :param rngSeed: The random number generator seed, default 23
        :param timeout: When the RPC call triggering the double spend flow times out in seconds, default 300 seconds
        :return:
        """
        stdout = os.path.join(node.directory, 'double-spend.out')
        stderr = os.path.join(node.directory, 'double-spend.err')

        args = self.defaultArgs(node, 'double-spend')
        if doubleSpendRatio: args.extend(['--double-spend-ratio', doubleSpendRatio])
        if numberOfSpends: args.extend(['--number-of-spends', numberOfSpends])
        if rngSeed: args.extend(['--rng-seed',rngSeed])
        if notary: args.extend(['--notary', notary.config.myLegalName])
        if timeout: args.extend(['--timeout',timeout])
        self.startProcess(command=PROJECT.JAVA, displayName='double-spend', workingDir=node.directory, arguments=args, environs=deepcopy(os.environ), stdout=stdout, stderr=stderr)

