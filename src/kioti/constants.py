import os
from pysys.constants import PROJECT
from kioti.distribution import CordaType, CordaDistribution
from kioti.network import Networks

ARTIFACTORY_URL = 'https://ci-artifactory.corda.r3cev.com/artifactory'
CORDAPPS_DIR = PROJECT.CORDAPPS_DIR
REMOTE_STAGING = os.path.join(PROJECT.root, 'resources', 'staging')
KEYS = os.path.join(PROJECT.root, 'resources', 'keys')

# default environment unless explicitly stated is nigtwatch
ENVIRONMENT = Networks.default

# default open source and enterprise distributions
CORDA_OS_DISTRIBUTION  = CordaDistribution(CordaType.os, '4.3')
CORDA_ENT_DISTRIBUTION  = CordaDistribution(CordaType.enterprise, '4.3')
CORDA_DISTRIBUTION = CORDA_ENT_DISTRIBUTION

# default enterprise version of CENM (there is no open source version)
CENM_VERSION = '1.1'

# default version of MidStack (Token and Account SDK)
TOKENS_SDK_VERSION = '1.1'
CONFID_SDK_VERSION = '1.0'
ACCOUNTS_SDK_VERSION = '1.0'
