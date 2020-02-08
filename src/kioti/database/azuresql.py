import wget

class AzureSQLDatabase():
    """Azure SQL database static configuration."""
    type = 'Azure SQL'
    dataSourceClassName = 'com.microsoft.sqlserver.jdbc.SQLServerDataSource'
    connectionPort = 1433
    connectionUrl = 'jdbc:sqlserver://vm-test-db-001.database.windows.net:%d;database=corda;encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30'
    username = 'sadmin'
    password = 'Password123!'
    driver = 'mssql-jdbc-6.4.0.jre8.jar'

    @classmethod
    def copyDriver(cls, dir):
        url = 'https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/6.4.0.jre8/%s' % cls.driver
        wget.download(url, out=dir, bar=None)

    @classmethod
    def getMappedPort(cls, testcase):
        return 1433

