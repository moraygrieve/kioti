import wget

class PostgressDatabase():
    """PostgreSQL database static configuration."""
    dataSourceClassName = 'org.postgresql.ds.PGSimpleDataSource'
    connectionPort = 5432
    connectionUrl = 'jdbc:postgresql://0.0.0.0:%d/corda'
    username = 'postgresuser'
    password = 'secretpassword'
    driver = 'postgresql-42.2.5.jar'

    @classmethod
    def copyDriver(cls, dir):
        url = 'https://repo1.maven.org/maven2/org/postgresql/postgresql/42.2.5/%s' % cls.driver
        wget.download(url, out=dir, bar=None)

    @classmethod
    def getMappedPort(cls, testcase):
        return testcase.getPort()


class Postgress96Database(PostgressDatabase):
    """PostgreSQL 9.6 database static configuration."""
    type = 'Postgres 9.6'


class Postgress1010Database(PostgressDatabase):
    """PostgreSQL 10.10 database static configuration."""
    type = 'Postgres 10.10'


class Postgress115Database(PostgressDatabase):
    """PostgreSQL 11.5 database static configuration."""
    type = 'Postgres 11.5'