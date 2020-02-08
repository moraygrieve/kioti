from net.corda.test.container.helper import DockerHelper

class SQLServerContainer(DockerHelper):
    """Container for MS SQ Server Database. """
    baseImage = 'microsoft/mssql-server-linux'
    imageTag = '2017-latest'

    def __init__(self, name, testcase, database, port):
        """Create an instance of the container.

        :param name: The name of the container
        :param testcase: A reference to the owning testcase
        :param database: The database type
        :param port: The database connection port
        """
        DockerHelper.__init__(self, name, testcase)
        self.env = {'ACCEPT_EULA':'Y', 'SA_PASSWORD': database.password }
        self.ports = {'%d/tcp' % database.connectionPort: port}

    def run(self):
        """Run an instance of the container."""
        DockerHelper.run(self, self.baseImage, self.imageTag, environment=self.env, ports=self.ports)
        for log in self.container.logs(stream=True):
            if log.find('SQL Server is now ready for client connections') >= 0: break
        self.log.info('SQL Server container is ready for connections')



