import os, uuid
from net.corda.test.utils.jsonutils import JsonConverter
from net.corda.test.utils.ports import getIPAddr

class Notary():
    def __init__(self, validating):
        self.validating = validating

class CryptoServices():
    def __init__(self, name, conf):
        self.name = name
        self.conf = conf

class NetworkServices():
    def __init__(self, networkMapURL, doormanURL):
        self.networkMapURL = networkMapURL
        self.doormanURL = doormanURL

class RPCUser():
    def __init__(self, username, password, permissions):
        self.username = username
        self.password = password
        self.permissions = permissions

class RPCSettings:
    def __init__(self, address, adminAddress, useSsl=False, standAloneBroker=False):
        self.useSsl = useSsl
        self.standAloneBroker = standAloneBroker
        self.address = address
        self.adminAddress = adminAddress

class SSHD():
    def __init__(self, port):
        self.port = port

class DataSourceProperties:
    def __init__(self, database, port):
        self.dataSourceClassName = database.dataSourceClassName
        self.dataSource = DataSource(database, port)

class DataSource:
    def __init__(self, database, port):
        self.url = database.connectionUrl % port
        self.user = database.username
        self.password = database.password

class Database:
    def __init__(self, isOS):
        self.transactionIsolationLevel = 'READ_COMMITTED'
        if isOS: self.initialiseSchema = True
        else: self.runMigration = True


class NodeConfig():

    @classmethod
    def init(self, name, testcase, devMode=False):
        nodeConfig = NodeConfig()
        nodeConfig.myLegalName = "O=%s-%s,L=London,C=GB" % (name, str(uuid.uuid4()))
        nodeConfig.devMode = devMode
        nodeConfig.p2pAddress = "%s:%d" % (getIPAddr(devMode), testcase.getPort((12000,12999)))
        nodeConfig.sshd = SSHD(testcase.getPort())
        nodeConfig.rpcUsers = [RPCUser("corda", "S0meS3cretW0rd", ["ALL"])]
        nodeConfig.rpcSettings = RPCSettings("localhost:%d" % testcase.getPort(), "localhost:%d" % testcase.getPort())

        if not devMode:
            nodeConfig.keyStorePassword = "cordacadevpass"
            nodeConfig.trustStorePassword = "trustpass"
            nodeConfig.crlCheckSoftFail = True
            nodeConfig.cordappSignerKeyFingerprintBlacklist = []

        return nodeConfig

    def withDatabase(self, testcase, isOS, database=None, port=None):
        if database is None:
            self.h2port = testcase.getPort()
        else:
            self.dataSourceProperties = DataSourceProperties(database, port if port is not None else testcase.getPort())
            self.database = Database(isOS)
        return self

    def withNetworkServices(self, environment):
        self.networkServices = NetworkServices(environment.networkMapURL, environment.doormanUrl)
        return self

    def withCryptoService(self, name, config):
        self.cryptoServiceName = name
        self.cryptoServiceConf = config
        return self

    def withNotary(self, validating):
        self.notary = Notary(validating)
        return self

    def write(self, file):
        if not os.path.exists(os.path.dirname(file)): os.makedirs(os.path.dirname(file))
        JsonConverter.toFile(self, file, indent=2)