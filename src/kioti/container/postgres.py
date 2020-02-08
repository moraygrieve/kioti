from kioti.container.helper import DockerHelper

class PostgressContainer(DockerHelper):
    """Container for Postgres Database. """
    baseImage = 'postgres'
    imageTag = '9.6'

    def __init__(self, name, testcase, database, port):
        """Create an instance of the container.

        :param name: The name of the container
        :param testcase: A reference to the owning testcase
        :param database: The database type
        :param port: The database connection port
        """
        DockerHelper.__init__(self, name, testcase)
        self.env = {'POSTGRES_USER':database.username, 'POSTGRES_PASSWORD':database.password, 'POSTGRES_DB':'corda'}
        self.ports = {'%d/tcp' % database.connectionPort: port}

    def run(self):
        """Run an instance of the container."""
        DockerHelper.run(self, self.baseImage, self.imageTag, environment=self.env, ports=self.ports)
        ready=False
        for log in self.container.logs(stream=True):
            if not ready and log.find('PostgreSQL init process complete; ready for start up') >=0 : ready=True
            if ready and log.find('database system is ready to accept connections') >= 0: break
        self.log.info('Postgres container is ready for connections')




class Postgress96Container(PostgressContainer):
    """Container for Postgres 9.6 Database. """
    imageTag = '9.6'


class Postgress1010Container(PostgressContainer):
    """Container for Postgres 10.10 Database. """
    imageTag = '10.10'


class Postgress115Container(PostgressContainer):
    """Container for Postgres 11.10 Database. """
    imageTag = '11.5'