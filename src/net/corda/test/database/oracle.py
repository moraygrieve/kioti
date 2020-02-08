import wget

class Oracle11gDatabase():
    """Oracle 11g database static configuration."""
    type = 'Oracle 11g'
    dataSourceClassName = 'oracle.jdbc.pool.OracleDataSource'
    connectionPort = 1521
    connectionUrl = 'jdbc:oracle:thin:@0.0.0.0:%d:XE'
    username = 'cordauser'
    password = 'oracle_password'
    driver = 'ojdbc8-12.2.0.1.jar'

    @classmethod
    def copyDriver(cls, dir):
        url = 'https://maven.xwiki.org/externals/com/oracle/jdbc/ojdbc8/12.2.0.1/%s' % cls.driver
        wget.download(url, out=dir, bar=None)

    @classmethod
    def getMappedPort(cls, testcase):
        return testcase.getPort()

class Oracle12cDatabase():
    """Oracle 12c database static configuration."""
    type = 'Oracle 12c'
    dataSourceClassName = 'oracle.jdbc.pool.OracleDataSource'
    connectionPort = 1521
    connectionUrl = 'jdbc:oracle:thin:@0.0.0.0:%d:ORCLCDB'
    username = 'cordauser'
    password = 'oracle_password'
    driver = 'ojdbc8-12.2.0.1.jar'

    @classmethod
    def copyDriver(cls, dir):
        url = 'https://maven.xwiki.org/externals/com/oracle/jdbc/ojdbc8/12.2.0.1/%s' % cls.driver
        wget.download(url, out=dir, bar=None)

    @classmethod
    def getMappedPort(cls, testcase):
        return testcase.getPort()