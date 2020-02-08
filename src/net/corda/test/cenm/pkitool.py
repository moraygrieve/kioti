from copy import deepcopy
from net.corda.test.constants import *
from net.corda.test.distribution.artifact import getCENMArtifact
from net.corda.test.model.pkitool import PKIToolConfig

class PKIToolHelper():
    """Class abstraction over the CENM PKI tool."""

    @classmethod
    def create(cls, testcase, config=None, idman_host='localhost', idman_port='10000', version=CENM_VERSION, defaultPassword=None):
        """Create and return an instance of the class.

        :param testcase: A reference to the owning testcase
        :param idman_host: The host of the identity manager
        :param idman_port: The port of the identity manager
        :param version: The version of CENM to use
        :param defaultPassword: The default password of the trust and key stores
        :return: An instance of {PKIToolHelper}
        """
        tool = PKIToolHelper(testcase, version)

        if config is None:
            tool.config = os.path.join(testcase.output, 'pkiconf.txt')
            PKIToolConfig.init(idman_host, idman_port, defaultPassword).write(tool.config)
        else:
            tool.config = config

        tool.jar = getCENMArtifact(version, 'pki-tool')
        return tool


    def __init__(self, testcase, version=CENM_VERSION):
        """Create an instance of the bootstrapper.

        :param testcase: The parent testcase running the process
        :param version: The version of the tool to use)
        """
        self.testcase = testcase
        self.log = testcase.log
        self.output = testcase.output
        self.startProcess = testcase.startProcess


    def run(self, verbose=None, loggingLevel=None, ignoreMissingCrl=True):
        """Run an instance of the PKI tool ovr a configuration file.

        :param verbose: If set, prints logging to the console as well as to a file
        :param loggingLevel: Enable logging at this level and higher. Defaults to INFO
        :param ignoreMissingCrl: Ignore missing CRL configuration
        """
        self.log.info('Running the PKI tool to generate certificates')
        stdout = os.path.join(self.output, 'pki-tool.out')
        stderr = os.path.join(self.output, 'pki-tool.err')

        arguments = ['-jar', self.jar]
        arguments.extend(('-f', self.config))
        if verbose: arguments.append('-v')
        if loggingLevel: arguments.extrend(('--logging-level', loggingLevel))
        if ignoreMissingCrl: arguments.append('-i')
        self.startProcess(command=PROJECT.JAVA, displayName='pki-tool', workingDir=self.output, arguments=arguments, environs=deepcopy(os.environ), stdout=stdout, stderr=stderr)
