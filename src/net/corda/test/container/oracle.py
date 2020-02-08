import cx_Oracle, time, os
from pysys.constants import PLATFORM
from net.corda.test.container.helper import DockerHelper

class OracleContainer(DockerHelper):

    def __init__(self, name, testcase, database, port):
        """Create an instance of the container.

        :param name: The name of the container
        :param testcase: A reference to the owning testcase
        :param database: The database type
        :param port: The database connection port
        """
        DockerHelper.__init__(self, name, testcase)
        self.database = database
        self.port = port

    def waitForConnection(self, sid, timeout=120):
        """Wait for the connection to become available, return the connection reference when successful.

        :param timeout: The timeout to wait for the connection
        """
        con_string='system/oracle@0.0.0.0:%d/%s' % (self.port, sid)
        self.log.info('Using connection string %s' % con_string)

        connection = None
        startTime = time.time()
        while connection == None:
            currentTime = time.time()
            if currentTime > startTime + timeout:
                self.log.info("Oracle service not available within the timeout period %d secs"% timeout)
                return None
            try:
                connection = cx_Oracle.connect(con_string)
            except:
                time.sleep(2)
        self.log.info("Oracle service startup took %d secs"% (time.time() - startTime))
        return connection

    def grantPermissions(self, connection, alterSession=False):
        """Grant required permissions for a corda node to use the database.

        :param connection: The connection reference
        :param alterSession: If true alter the session to set set ORACLE_SCRIPT to true
        """
        cursor = connection.cursor()
        if alterSession: cursor.execute('ALTER SESSION SET \"_ORACLE_SCRIPT\"=true')
        cursor.execute('CREATE USER %s IDENTIFIED BY %s' % (self.database.username, self.database.password))
        cursor.execute('GRANT CREATE SESSION TO %s' % self.database.username)
        cursor.execute('GRANT CREATE TABLE TO %s' % self.database.username)
        cursor.execute('GRANT CREATE VIEW TO %s' % self.database.username)
        cursor.execute('GRANT CREATE SEQUENCE TO %s' % self.database.username)
        cursor.execute('GRANT ALL PRIVILEGES TO %s' % self.database.username)
        cursor.close()
        connection.close()


class Oracle11gContainer(OracleContainer):
    """Container for Oracle 11g Database. """
    baseImage = 'oracleinanutshell/oracle-xe-11g'
    imageTag = 'latest'

    def __init__(self, name, testcase, database, port):
        """Create an instance of the container.

        :param name: The name of the container
        :param testcase: A reference to the owning testcase
        :param database: The database type
        :param port: The database connection port
        """
        OracleContainer.__init__(self, name, testcase, database, port)
        self.env = {'ORACLE_ALLOW_REMOTE': 'true'}
        self.vol = {'/etc/timezone': {'bind': '/etc/timezone', 'mode': 'rw'}} if PLATFORM != 'darwin' else {}
        self.ports = {'%d/tcp' % database.connectionPort: port}

    def run(self):
        """Run the container instance."""
        DockerHelper.run(self, self.baseImage, self.imageTag, environment=self.env, ports=self.ports, volumes=self.vol)
        ready=False
        for log in self.container.logs(stream=True):
            if log.find('Starting Oracle Database 11g Express Edition instance') >= 0 and not ready: ready = True
            if ready and log.find('System altered') >= 0: break
        self.log.info('Oracle 11g container is ready for connections ... running initialisation actions')

        connection = self.waitForConnection(sid='XE')
        if connection is not None: self.grantPermissions(connection)


class Oracle12cContainer(OracleContainer):
    """Container for Oracle 12c Database. """
    baseImage = 'store/oracle/database-enterprise'
    imageTag = '12.2.0.1-slim'

    def __init__(self, name, testcase, database, port):
        """Create an instance of the container.

        :param name: The name of the container
        :param testcase: A reference to the owning testcase
        :param database: The database type
        :param port: The database connection port
        """
        OracleContainer.__init__(self, name, testcase, database, port)
        oracle_log = os.path.join(testcase.output, 'oracle-%s' % name)
        self.env =  {'DB_PASSWD': 'oracle'}
        self.vol = {'/etc/timezone': {'bind': '/etc/timezone', 'mode': 'rw'}} if PLATFORM != 'darwin' else {}
        self.ports = {'%d/tcp' % database.connectionPort: port}
        os.makedirs(oracle_log)

    def run(self):
        """Run the container instance."""
        DockerHelper.run(self, self.baseImage, self.imageTag, environment=self.env, ports=self.ports, volumes=self.vol)
        for log in self.container.logs(stream=True):
            if log.find('Docker DB configuration is complete') >=0: break
        self.log.info('Oracle 12c container is ready for connections ... running initialisation actions')

        connection = self.waitForConnection(sid='ORCLCDB.localdomain')
        if connection is not None: self.grantPermissions(connection, alterSession=True)

