from copy import deepcopy
from kioti.constants import *
from kioti.distribution.artifact import getCordaArtifact

class BootStrapper():
    """Class abstraction over the Corda bootstrapper.

    The bootstrapper takes node configuration files in a given directory, and expands to create the node
    directories ready for running in a local development network. An instance is created with the owning
    testcase, and the distribution of the bootstrapper to use. The bootstrapper bundles the main corda jar
    file, so no other dependencies are required after the bootstrap process has been run.

    """

    def __init__(self, testcase, distribution):
        """Create an instance of the bootstrapper.

        :param testcase: The parent testcase running the process
        :param distribution: The distribution of Corda to use
        """
        self.testcase = testcase
        self.log = testcase.log
        self.output = testcase.output
        self.startProcess = testcase.startProcess
        self.jar = getCordaArtifact(distribution, 'corda-tools-network-bootstrapper')


    def run(self, dir=None, copy_cordapps='FirstRunOnly', abortOnError=True):
        """Run an instance of the bootstrapper over pre-configured node configuration files.

        :param dir: The directory containing the node configuration files
        :param copy_cordapps: Valid values are FirstRunOnly, Yes, No
        :param abortOnError: Abort the test on an error bootstrapping
        """
        self.log.info('Running the network bootstrapper to create a local bootstrapped network')
        stdout = os.path.join(self.output, 'corda-bootstrap.out')
        stderr = os.path.join(self.output, 'corda-bootstrap.err')

        arguments = ['-jar', self.jar]
        arguments.extend(['--copy-cordapps', copy_cordapps])
        if dir is not None: arguments.extend(['--dir', dir])
        else: arguments.extend(['--dir', self.output])

        self.startProcess(command=PROJECT.JAVA, displayName='boostrapper', workingDir=self.output, arguments=arguments,
                          environs=deepcopy(os.environ), abortOnError=abortOnError, stdout=stdout, stderr=stderr)

        # abort the test if the bootstrapper did not pass successfully
        self.testcase.assertGrep(os.path.join(self.output, 'corda-bootstrap.out'), expr='Bootstrapping complete!', abortOnError=abortOnError)
