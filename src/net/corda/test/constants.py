import os
from pysys.constants import PROJECT
from net.corda.test.distribution import CordaType, CordaDistribution
from net.corda.test.network import Networks

ARTIFACTORY_URL = 'https://ci-artifactory.corda.r3cev.com/artifactory'
CORDAPPS_DIR = PROJECT.CORDAPPS_DIR
REMOTE_STAGING = os.path.join(PROJECT.root, 'resources', 'staging')
KEYS = os.path.join(PROJECT.root, 'resources', 'keys')

# default environment unless explicitly stated is nigtwatch
ENVIRONMENT = Networks.nightwatch

# default open source and enterprise distributions
CORDA_OS_DISTRIBUTION  = CordaDistribution(CordaType.os, '4.3')
CORDA_ENT_DISTRIBUTION  = CordaDistribution(CordaType.enterprise, '4.3-RC03')
CORDA_DISTRIBUTION = CORDA_ENT_DISTRIBUTION

# default enterprise version of CENM (there is no open source version)
CENM_VERSION = '1.0'

# default version of MidStack (Token and Account SDK)
TOKENS_SDK_VERSION = '1.1-RC07-PRESIGN'
CONFID_SDK_VERSION = '1.0-RC04'
ACCOUNTS_SDK_VERSION = '1.0-RC04'
