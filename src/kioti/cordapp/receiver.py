from copy import deepcopy
from pysys.utils.filecopy import filecopy
from kioti.constants import *
from kioti.cordapp.sshclient import CorDappSSHClient

class ReceiverCorDapp():
    """Utility class around the Simple Test CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        jar = os.path.join(CORDAPPS_DIR, 'receiver', 'staging', 'receiver-workflows.jar')
        filecopy(jar, os.path.join(toDir, os.path.basename(jar)))


class ReceiverCorDappSSHClient(CorDappSSHClient):
    """Abstraction over ssh command interaction with the Receiver Flow test CorDapp."""

    def startFlow(self, node, otherNode, initiator='ReceiveFlow', timeout=None):
        """Run a miniflow.

        :param node: The node to execute the SSH command against
        :param otherNode: The other node to communicate to
        :param timeout: The timeout on the ssh call
        """
        stdout = os.path.join(node.directory, 'receive-flow.out')
        stderr = os.path.join(node.directory, 'receive-flow.err')
        command = 'flow start %s toParty: "%s"' % (initiator,otherNode.config.myLegalName)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


class ReceiverCorDappRPCClient():
    """Utility class around the Test Receiver CordApp RPC client application."""

    def __init__(self, testcase):
        """Class constructor.

        :param testcase: A reference to the owning testcase
        :param distribution: The distribution
        """
        self.log = testcase.log
        self.startProcess = testcase.startProcess


    def defaultArgs(self, node):
        """Return default arguments to the RPC client.

        :param node: The node to execute the RPC command against
        """
        arguments = ['-jar', os.path.join(CORDAPPS_DIR, 'receiver', 'staging', 'receiver-client.jar')]
        arguments.append(node.config.rpcSettings.address)
        arguments.append(node.config.rpcUsers[0].username)
        arguments.append(node.config.rpcUsers[0].password)
        return arguments


    def run(self, node, timeout=None):
        """Perform a cash issue transaction.
        """
        stdout = os.path.join(node.directory, 'receiver-run.out')
        stderr = os.path.join(node.directory, 'receiver-run.err')
        args = self.defaultArgs(node)
        args.append(node.config.myLegalName)
        self.startProcess(command=PROJECT.JAVA, displayName='ReceiverCorDappRPCClient', workingDir=node.directory, arguments=args, environs=deepcopy(os.environ), stdout=stdout, stderr=stderr)

