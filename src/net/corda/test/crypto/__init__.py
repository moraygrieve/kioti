import os
from net.corda.test.constants import KEYS
from net.corda.test.model.node import CryptoServices

class Ultimaco():
    """Abstraction over connections to the Ultimaco HSM."""
    def __init__(self):
        pass

class Gemalto():
    """Abstraction over connections to the Gemalto HSM."""
    def __init__(self):
        pass

class Securosys():
    """Abstraction over connections to the Securosys HSM."""
    def __init__(self):
        pass

class FutureX:
    """Abstraction over connections to the FutureX HSM."""
    def __init__(self):
        pass

class AzureKeyVault:
    """Abstraction over connections to the AzureKeyVault HSM."""
    def __init__(self, testcase):
        self.testcase = testcase
        self.path = os.path.join(KEYS, 'azurekv.pkcs12')
        self.alias = '1'
        self.password = '4gottenMemorieS'
        self.keyVaultURL = 'https://vmqa-keyvault-01.vault.azure.net/'
        self.clientId = '972a3db2-bc29-472b-8b52-98aa65fcff98'
        self.protection = 'SOFTWARE'

    @classmethod
    def init(cls, testcase):
        instance = AzureKeyVault(testcase)
        return CryptoServices('AZURE_KEY_VAULT', instance.write(testcase))

    def write(self, testcase):
        cryptoConfig = os.path.join(testcase.output, 'az_keyvault.conf')
        with open(cryptoConfig, 'w') as fp:
            fp.write('path: %s\n' % self.path)
            fp.write('alias: "%s"\n' % self.alias)
            fp.write('password: "%s"\n' % self.password)
            fp.write('keyVaultURL: "%s"\n' % self.keyVaultURL)
            fp.write('clientId: "%s"\n' % self.clientId)
            fp.write('protection: "%s"\n' % self.protection)
        return cryptoConfig
