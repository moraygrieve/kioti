from copy import deepcopy
from pysys.utils.filecopy import filecopy
from kioti.constants import *
from kioti.cordapp.sshclient import CorDappSSHClient
from kioti.distribution.artifact import getCordaArtifact

class FinanceCorDapp():
    """Utility class around the Finance CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        for jar in cls.getjars():
            filecopy(jar, os.path.join(toDir, os.path.basename(jar)))

    @classmethod
    def getjars(cls):
        workflow = getCordaArtifact(CORDA_ENT_DISTRIBUTION, 'corda-finance-workflows')
        contract = getCordaArtifact(CORDA_OS_DISTRIBUTION, 'corda-finance-contracts')
        return workflow, contract


class FinanceCorDappSSHClient(CorDappSSHClient):
    """Utility class around the Finance CordApp SSH interaction."""

    def cashIssue(self, node, amount, reference='1234', timeout=None):
        """Perform a cash issue transaction.

        :param node: The node to execute the SSH command against
        :param amount: The transaction amount for transfer
        :param reference: A reference to the transaction
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-issue.out')
        stderr = os.path.join(node.directory, 'cash-issue.err')
        command = 'flow start CashIssueFlow amount: %s, notary: "Notary"' % amount
        command += ', issuerBankPartyRef: %s' % reference
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


    def cashPayment(self, node, amount, nodeToPay, anonymous=True, timeout=None):
        """Perform a cash payment transaction to another party.

        :param node: The node to execute the SSH command against
        :param amount: The amount in the payment, e.g. 100 USD
        :param nodeToPay: The party to send the payment to
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-payment.out')
        stderr = os.path.join(node.directory, 'cash-payment.err')
        command = 'flow start CashPaymentFlow amount: %s, recipient: "%s", anonymous: %s' % (amount, nodeToPay.config.myLegalName, anonymous)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


    def cashBalance(self, node, timeout=None):
        """Request a node to output details of it's cash balance.

        :param node: The node to execute the SSH command against
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-balance.out')
        stderr = os.path.join(node.directory, 'cash-balance.err')
        command = 'run vaultQuery contractStateType: net.corda.finance.contracts.asset.Cash$State'
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, stdout, stderr).execute(command, timeout).close()


class FinanceCorDappRPCClient():
    """Utility class around the Finance CordApp RPC client application."""

    def __init__(self, testcase, distribution=CORDA_OS_DISTRIBUTION):
        """Class constructor.

        :param testcase: A reference to the owning testcase
        """
        self.log = testcase.log
        self.startProcess = testcase.startProcess
        self.distribution = distribution
        self.environs = deepcopy(os.environ)


    def defaultArgs(self, node, command):
        """Return default arguments to the RPC client.

        :param node: The node to execute the RPC command against
        :param command: The command name
        """
        classpath = [os.path.join(CORDAPPS_DIR, 'finance', 'staging', 'finance-client.jar')]
        for jar in FinanceCorDapp.getjars(self.distribution): classpath.append(jar)

        arguments = ['-cp', os.pathsep.join(classpath)]
        arguments.append('net.corda.test.cordapps.finance.client.MainKt')
        arguments.append(command)
        arguments.append(node.config.rpcSettings.address)
        arguments.append(node.config.rpcUsers[0].username)
        arguments.append(node.config.rpcUsers[0].password)
        return arguments


    def cashIssue(self, node, amount, minimuServerProtocolVersion=None, reference=None, timeout=None):
        """Perform a cash issue transaction.

        :param node: The node to execute the RPC command against
        :param amount: The transaction amount for transfer
        :param minimuServerProtocolVersion: The minimum platform version supported
        :param reference: A reference to the transaction
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-issue.out')
        stderr = os.path.join(node.directory, 'cash-issue.err')

        args = self.defaultArgs(node, 'cash-issue')
        args.append(amount)
        if minimuServerProtocolVersion: args.extend(['--minimum-server-protocol-version', minimuServerProtocolVersion])
        if reference: args.extend(['--reference', reference])
        if timeout: args.extend(['--timeout', timeout])

        self.startProcess(command=PROJECT.JAVA, displayName='cash-issue', workingDir=node.directory, arguments=args, environs=self.environs, stdout=stdout, stderr=stderr)


    def cashBalance(self, node, minimuServerProtocolVersion=None, timeout=None):
        """Request a node to output details of it's cash balance.

        :param node: The node to execute the RPC command against
        :param minimuServerProtocolVersion: The minimum platform version supported
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-balance.out')
        stderr = os.path.join(node.directory, 'cash-balance.err')

        args = self.defaultArgs(node, 'cash-balance')
        if minimuServerProtocolVersion: args.extend(['--minimum-server-protocol-version', minimuServerProtocolVersion])
        if timeout: args.extend(['--timeout', timeout])

        self.startProcess(command=PROJECT.JAVA, displayName='cash-balance', workingDir=node.directory, arguments=args, environs=self.environs, stdout=stdout, stderr=stderr)


    def cashPayment(self, node, amount, nodeToPay, anonymous, minimuServerProtocolVersion=None, timeout=None):
        """Perform a cash payment transaction to another party.

        :param node: The node to execute the RPC command against
        :param amount: The amount in the payment, e.g. 100 USD
        :param nodeToPay: The party to send the payment to
        :param anonymous: If supplied the payment is anonymous
        :param minimuServerProtocolVersion: The minimum platform version supported
        :param timeout: The timeout for the transaction
        """
        stdout = os.path.join(node.directory, 'cash-payment.out')
        stderr = os.path.join(node.directory, 'cash-payment.err')

        args = self.defaultArgs(node, 'cash-payment')
        args.append(amount)
        args.append(nodeToPay.config.myLegalName)
        if anonymous: args.append('--anonymous')
        if minimuServerProtocolVersion: args.extend(['--minimum-server-protocol-version', minimuServerProtocolVersion])
        if timeout: args.extend(['--timeout', timeout])

        self.startProcess(command=PROJECT.JAVA, displayName='cash-payment', workingDir=node.directory, arguments=args, environs=self.environs, stdout=stdout, stderr=stderr)


    def resolveParty(self, node, nodeToResolve, minimuServerProtocolVersion=None, timeout=None):
        """Force resolution by a node of a given party.

        :param node: The node to execute the RPC command against
        :param nodeToResolve: The Corda node to resolve in the network map
        :param minimuServerProtocolVersion: The minimum platform version supported
        :param timeout: The timeout for the transation
        """
        stdout = os.path.join(node.directory, 'resolve-party.out')
        stderr = os.path.join(node.directory, 'resolve-party.err')

        args = self.defaultArgs(node, 'resolve-party')
        args.append(nodeToResolve.config.myLegalName)
        if minimuServerProtocolVersion: args.extend(['--minimum-server-protocol-version', minimuServerProtocolVersion])
        if timeout: args.extend(['--timeout', timeout])

        self.startProcess(command=PROJECT.JAVA, displayName='resolve-party', workingDir=node.directory, arguments=args, environs=self.environs, stdout=stdout, stderr=stderr)


    def uploadAttachment(self, node, jarLocation, minimuServerProtocolVersion, timeout):
        pass


    def shutdown(self, node, minimuServerProtocolVersion=None, timeout=None):
        """Force resolution by a node of a given party.

        :param node: The node to execute the RPC command against
        :param minimuServerProtocolVersion: The minimum platform version supported
        :param timeout: The timeout for the transation
        """
        stdout = os.path.join(node.directory, 'shut-down.out')
        stderr = os.path.join(node.directory, 'shut-down.err')

        args = self.defaultArgs(node, 'shut-down')
        if minimuServerProtocolVersion: args.extend(['--minimum-server-protocol-version', minimuServerProtocolVersion])
        if timeout: args.extend(['--timeout', timeout])

        self.startProcess(command=PROJECT.JAVA, displayName='shut-down', workingDir=node.directory, arguments=args, environs=self.environs, stdout=stdout, stderr=stderr)


