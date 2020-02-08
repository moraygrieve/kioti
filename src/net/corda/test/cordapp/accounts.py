from pysys.utils.filecopy import filecopy
from net.corda.test.constants import *
from net.corda.test.cordapp.sshclient import CorDappSSHClient
from net.corda.test.distribution.artifact import getMidStackArtifact

class AccountsCorDapp():
    """Utility class around the Accounts SDK only Test CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        jars = [os.path.join(CORDAPPS_DIR, 'accounts', 'staging', 'accounts-test-cordapp-workflows.jar')]
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), jars)
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), cls.getjars())

    @classmethod
    def getjars(cls):
        cw = getMidStackArtifact(ACCOUNTS_SDK_VERSION, 'accounts-workflows')
        cc = getMidStackArtifact(ACCOUNTS_SDK_VERSION, 'accounts-contracts')
        return (cw, cc)


class AccountsSSHClient(CorDappSSHClient):
    """Abstraction over ssh command interaction with the Accounts SDK only Test CorDapp."""

    def createAccount(self, node, name, timeout=None, stdout=None, stderr=None, logOut=True):
        """Run a flow to create a new account on the supplied node.

        :param node: The node acting as the issuer
        :param name: The name of the account to create
        :param timeout: The timeout on the flow command
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :param logOut: Log out the command being run if true
        :return:
        """
        fstdout = os.path.join(node.directory, 'issue-cash.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'issue-cash.err' if stderr is None else stderr)
        command = 'flow start net.corda.test.tokens.flows.CreateAccount name: "%s"' % (name)
        if logOut: self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()
