from pysys.utils.filecopy import filecopy
from net.corda.test.constants import *
from net.corda.test.cordapp.sshclient import CorDappSSHClient
from net.corda.test.distribution.artifact import getCordaArtifact, getMidStackArtifact

class ConfidentitiesCorDapp():
    """Utility class around the Confidential Identities SDK only Test CorDapp application."""

    @classmethod
    def copyjars(cls, toDir):
        jars = [os.path.join(CORDAPPS_DIR, 'confidentities', 'staging', 'confidentities-contracts.jar')]
        jars.append(os.path.join(CORDAPPS_DIR, 'confidentities', 'staging', 'confidentities-workflows.jar'))
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), jars)
        map(lambda x: filecopy(x, os.path.join(toDir, os.path.basename(x))), cls.getjars())

    @classmethod
    def getjars(cls):
        oldci = getCordaArtifact(CORDA_DISTRIBUTION, 'corda-confidential-identities')
        newci = getMidStackArtifact(CONFID_SDK_VERSION, 'ci-workflows')
        return (oldci, newci)


class ConfidentitiesSSHClient(CorDappSSHClient):
    """Abstraction over ssh command interaction with the Confidential Identities SDK only Test CorDapp."""

    def blowWhistle(self, node, badcompany, investigator, flow='BlowWhistleFlow', timeout=None, stdout=None, stderr=None):
        """Run a flow to blow the whilst on a company.

        :param node: The node executing the blow whistler
        :param badcompany: The bad company being reported
        :param investigator: The company that will investigate
        :param flow: The name of the blow whistle flow (BlowWhistleFlow | BlowWhistleFlowNew | BlowWhistleFlowOld)
        :param timeout: The timeout on the flow command
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :return:
        """
        fstdout = os.path.join(node.directory, 'blow.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'blow.err' if stderr is None else stderr)
        command = 'flow start %s badCompany: "%s"' % (flow, badcompany.config.myLegalName)
        command += ', investigator: "%s"' %  (investigator.config.myLegalName)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()


    def blowWhistleList(self, node, flow='BlowWhistleFlowList', timeout=None, stdout=None, stderr=None):
        """Run a flow to blow the whilst on a company.

        :param node: The node executing the blow whistler
        :param timeout: The timeout on the flow command
        :param flow: The name of the list flow (BlowWhistleFlowList | BlowWhistleFlowNewList | BlowWhistleFlowOldList)
        :param stdout: Filename for stdout
        :param stderr: Filename for stderr
        :return:
        """
        fstdout = os.path.join(node.directory, 'list.out' if stdout is None else stdout)
        fstderr = os.path.join(node.directory, 'list.err' if stderr is None else stderr)
        command = 'flow start %s' % (flow)
        self.log.info('Performing ssh command: %s' % command)
        self.createClient(node, fstdout, fstderr).execute(command, timeout).close()