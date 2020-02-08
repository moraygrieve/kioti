from net.corda.test.container.postgres import Postgress96Container, Postgress1010Container, Postgress115Container
from net.corda.test.container.sqlserver import SQLServerContainer
from net.corda.test.container.oracle import Oracle11gContainer, Oracle12cContainer
from net.corda.test.database import Databases

class DatabaseContainers:
    """Static configuration to hold the supported database containers. """

    # map the database type to the required containe
    map = {
        Databases.postgres96.type:Postgress96Container,
        Databases.postgres1010.type:Postgress1010Container,
        Databases.postgres115.type:Postgress115Container,
        Databases.sqlserver.type:SQLServerContainer,
        Databases.oracle11g.type:Oracle11gContainer,
        Databases.oracle12c.type:Oracle12cContainer
    }

    @classmethod
    def forType(cls, database):
        """Return the container for the given database type"""
        return cls.map[database.type] if cls.map.has_key(database.type) else None