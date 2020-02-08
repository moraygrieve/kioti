import time
from net.corda.test.constants import *
from net.corda.test.ssh.client import SSHClient
from net.corda.test.utils.dname import DistinguisedName

class CorDappSSHClient():
    """Utility class around the Simple Test CordApp SSH interaction."""

    def __init__(self, testcase):
        """Class constructor.

        :param testcase: A reference to the owning testcase
        """
        self.log = testcase.log
        self.waitForSignal = testcase.waitForSignal


    def createClient(self, node, stdout, stderr):
        """Return an SSH connected client to a node.

        :param node: The node to connect to
        :param stdout: Filename to store any stdout from running commands
        :param stderr: Filename to store any stderr from running commands
        :return:
        """
        username = node.config.rpcUsers[0].username
        password = node.config.rpcUsers[0].password
        port = node.config.sshd.port
        return SSHClient(username, password, port, stdout, stderr)


    def flowList(self, node, timeout=None, stdout='flow-list.out', stderr='flow-list.err'):
        """List the available flows on a node.

        :param node: The node to execute the flow list command on
        :param timeout: The timeout for the transaction
        :param stdout: Filename to store any stdout from running the command
        :param stderr: Filename to store any stderr from running the command
        """
        stdout = os.path.join(node.directory, stdout)
        stderr = os.path.join(node.directory, stderr)
        command = 'flow list'
        self.log.info('Listing available flows on the node')
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


    def vaultQuery(self, node, contractStateType, timeout=None, stdout='query-vault.out', stderr='query-vault.err'):
        """Perform a vault query.

        :param node: The node to execute the vault query on
        :param contractStateType: The fully qualified class of the state to query
        :param timeout: The timeout for the transaction
        :param stdout: Filename to store any stdout from running the command
        :param stderr: Filename to store any stderr from running the command
        """
        stdout = os.path.join(node.directory, stdout)
        stderr = os.path.join(node.directory, stderr)
        command = 'run vaultQuery contractStateType: %s' % contractStateType
        self.log.info('Querying vault on the node for %s' % contractStateType)
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


    def shutdown(self, node, graceful=True, timeout=None):
        """Shutdown a client.

        :param node: The node to execute the shutdown command against
        :param graceful: If true shutdown is requested to be graceful
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'shut-down.out')
        stderr = os.path.join(node.directory, 'shut-down.err')
        command = 'run %s' % ('gracefulShutdown' if graceful else 'shutdown')
        self.log.info('Shutting down the client via ssh command: %s' % command)
        self.createClient(node, stdout, stderr).execute(command, timeout)
        self.waitForSignal(file=node.nodeLogfile, filedir=node.nodeLogdir, expr='Shutting down ...', timeout=10).close()


    def uploadAttachment(self, node, attachment, timeout=None):
        """Upload a jar attachment to a node.

        :param node: The node to execute the upload command against
        :param attachment: The jar file to be uploaded
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'upload-attachment.out')
        stderr = os.path.join(node.directory, 'upload-attachment.err')
        command = 'run uploadAttachment jar : %s' % attachment
        self.log.info('Uploading attachment: %s' % os.path.basename(attachment))
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


    def waitForParty(self, node, nodeToResolve, timeout=30):
        """Wait for a party to be resolved in the network map.

        :param node: The node to execute the upload command against
        :param nodeToResolve: The node to resolve in the network map
        :param timeout: The timeout for the operation
        """
        client = self.createClient(node, None, None)
        command = 'run wellKnownPartyFromX500Name x500Name: "%s"' % nodeToResolve.config.myLegalName
        orgName = DistinguisedName.getOrganisation(nodeToResolve.config.myLegalName)

        startTime = time.time()
        while True:
            currentTime = time.time()
            if currentTime > startTime + timeout:
                self.log.info("Attempt to resolve party timed out after %d secs"% timeout)
                break

            _stdin, _stdout, _stderr = client.executeCommand(command, timeout=5)
            if any(orgName in s for s in _stdout.readlines()): break