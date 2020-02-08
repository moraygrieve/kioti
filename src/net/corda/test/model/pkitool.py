import os
from net.corda.test.utils.jsonutils import JsonConverter

# mapping from data attributes to JSON output
JsonConverter.registerTranslation('CORDA_TLS_CRL_SIGNER', '::CORDA_TLS_CRL_SIGNER')
JsonConverter.registerTranslation('CORDA_ROOT', '::CORDA_ROOT')
JsonConverter.registerTranslation('CORDA_SUBORDINATE', '::CORDA_SUBORDINATE')
JsonConverter.registerTranslation('CORDA_IDENTITY_MANAGER', '::CORDA_IDENTITY_MANAGER')
JsonConverter.registerTranslation('CORDA_NETWORK_MAP', '::CORDA_NETWORK_MAP')
JsonConverter.registerTranslation('CORDA_SSL_ROOT', '::CORDA_SSL_ROOT')
JsonConverter.registerTranslation('CORDA_SSL_IDENTITY_MANAGER', '::CORDA_SSL_IDENTITY_MANAGER')
JsonConverter.registerTranslation('CORDA_SSL_NETWORK_MAP', '::CORDA_SSL_NETWORK_MAP')
JsonConverter.registerTranslation('CORDA_SSL_SIGNER', '::CORDA_SSL_SIGNER')

class CertificateRevocationListEntry():
    def __init__(self, idman_host, idman_port, filePath, type, indirectIssuer=None):
        self.crlDistributionUrl = 'http://%s:%s/certificate-revocation-list/%s' % (idman_host, idman_port, type)
        self.filePath = filePath
        if indirectIssuer is not None: self.indirectIssuer = indirectIssuer


class CertificateRevocationList():
    def __init__(self, idman_host, idman_port, filePath, type, indirectIssuer=None):
        self.crl = CertificateRevocationListEntry(idman_host, idman_port, filePath, type, indirectIssuer)


class Certificates():
    def __init__(self, idman_host, idman_port):
        self.CORDA_TLS_CRL_SIGNER = CertificateRevocationList(idman_host, idman_port, './crl-files/tls.crl', type='tls', indirectIssuer=True)
        self.CORDA_ROOT = CertificateRevocationList(idman_host, idman_port, './crl-files/root.crl', type='root')
        self.CORDA_SUBORDINATE = CertificateRevocationList(idman_host, idman_port, './crl-files/subordinate.crl', type='subordinate')
        self.CORDA_IDENTITY_MANAGER = {}
        self.CORDA_NETWORK_MAP = {}
        self.CORDA_SSL_ROOT = {}
        self.CORDA_SSL_IDENTITY_MANAGER = {}
        self.CORDA_SSL_NETWORK_MAP = {}
        self.CORDA_SSL_SIGNER = {}


class PKIToolConfig():

    @classmethod
    def init(self, idman_host, idman_port, defaultPassword=None):
        pkitoolConfig = PKIToolConfig()
        if defaultPassword: pkitoolConfig.defaultPassword = defaultPassword
        pkitoolConfig.certificates = Certificates(idman_host, idman_port)
        return pkitoolConfig

    def write(self, file):
        if not os.path.exists(os.path.dirname(file)): os.makedirs(os.path.dirname(file))
        JsonConverter.toFile(self, file, indent=2)
        return file