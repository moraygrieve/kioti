import os
from pysys import log
from kioti.constants import REMOTE_STAGING
from kioti.database.postgres import Postgress96Database, Postgress1010Database, Postgress115Database
from kioti.database.sqlserver import SQLServerDatabase
from kioti.database.oracle import Oracle11gDatabase, Oracle12cDatabase
from kioti.database.azuresql import AzureSQLDatabase

class Databases:
    """Class to hold static information on the supported databases."""
    azuresql = AzureSQLDatabase
    sqlserver = SQLServerDatabase
    postgres96 = Postgress96Database
    postgres1010 = Postgress1010Database
    postgres115 = Postgress115Database
    oracle11g = Oracle11gDatabase
    oracle12c = Oracle12cDatabase


def getDriver(database):
    """Downloads database drivers to the staging area, and return the full path to the driver."""
    download_dir = os.path.join(REMOTE_STAGING, 'drivers')
    target = os.path.join(download_dir, database.driver)

    if not os.path.exists(download_dir): os.makedirs(download_dir)

    if not os.path.exists(target):
        log.info('Downloading driver %s' % database.driver)
        database.copyDriver(download_dir)
    return target
