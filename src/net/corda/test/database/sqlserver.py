import wget

class SQLServerDatabase():
    """SQL Server database static configuration."""
    type = 'SQL Server'
    dataSourceClassName = 'com.microsoft.sqlserver.jdbc.SQLServerDataSource'
    connectionPort = 1433
    connectionUrl = 'jdbc:sqlserver://0.0.0.0:%s;database=master'
    username = 'sa'
    password = 'Password123!'
    driver = 'mssql-jdbc-6.4.0.jre8.jar'

    @classmethod
    def copyDriver(cls, dir):
        url = 'https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/6.4.0.jre8/%s' % cls.driver
        wget.download(url, out=dir, bar=None)

    @classmethod
    def getMappedPort(cls, testcase):
        return testcase.getPort()