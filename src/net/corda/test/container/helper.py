import docker
from pysys.constants import *
from net.corda.test.constants import *

class DockerHelper:
    """Abstraction over running docker containers.

    This class uses the docker module to create a client using docker.from_env() and pull down and start containers.
    The docker server client should be installed and running on the host machine. Images are by default detached -
    not it is the responsibility of the owning testcase to stop the container either explicitly, or by registering
    the stop method as a cleanup function.
    """

    def __init__(self, name, testcase):
        """Class constructor.

        :param name: The logical name of the Corda node
        :param testcase: The testcase managing the Corda node
        """
        self.name = name
        self.client = docker.from_env()
        self.container = None
        self.log = testcase.log
        self.directory = os.path.join(testcase.output, name)


    def run(self, baseImage, imageTag, detach=True, environment=None, ports=None, volumes=None) :
        """Run a docker container, setting self.container to the container instance.

        :param baseImage: The base name of the image
        :param imageTag: The image tag
        :param detach: True if the container should be detached
        :param environment: The environment to pass into the container
        :param ports: Port mapping between the host and container
        :param volumes: Specify mapping of volumes between container and host
        """
        if self.container != None: raise Exception('Container already running!')
        self.log.info('Starting container for image %s' % baseImage+':'+imageTag)
        self.container = self.client.containers.run(image=baseImage+':'+imageTag, detach=detach, name=self.name, environment=environment, ports=ports, volumes=volumes)
        self.log.info('Started container with name %s' % self.container.name)


    def stop(self):
        """Stop a running docker container. """
        if self.container == None: return
        self.log.info('Stopping and removing container with name %s' % self.container.name)
        self.container.stop()
        self.container.remove(v=True)
        self.container = None