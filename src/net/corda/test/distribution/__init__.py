import collections

Distribution = collections.namedtuple('Distribution', 'groupId repositoryId product requireAuthentication')

class MidstackType:
    """Class for the supported Midstack distribution types.

    Allows for differentiating between Midstack components, such as Tokens and Accounts
    SDK.
    """
    os_tokens = Distribution('com.r3.corda.lib.tokens', 'corda-lib-dev', 'OS', False)
    os_accounts = Distribution('com.r3.corda.lib.accounts', 'corda-lib-dev', 'OS', False)
    os_confid = Distribution('com.r3.corda.lib.ci', 'corda-lib-dev', 'OS', False)

    components = {'tokens-workflows':os_tokens,
                   'tokens-contracts':os_tokens,
                   'tokens-selection':os_tokens,
                   'tokens-money':os_tokens,
                   'accounts-workflows':os_accounts,
                   'accounts-contracts':os_accounts,
                   'ci-workflows':os_confid
                  }

    @classmethod
    def lookup(cls, artifact):
        if not cls.components.has_key(artifact):
            raise Exception('Unknown artifact for Midstack distribution')
        else: return cls.components[artifact]


class CENMType:
    """Class for the supported CENM distribution types.

    Allows for differentiating between CENM services and tools. Note that there is
    no open source release of CENM, and snapshot releases are stored next to normal
    released versions.
    """
    enterprise_services = Distribution('com.r3.enm.services', 'r3-enterprise-network-manager', 'ENT', True)
    enterprise_tools = Distribution('com.r3.enm.tools', 'r3-enterprise-network-manager', 'ENT', True)

    components = {'pki-tool':enterprise_tools,
                   'crr-submission-tool':enterprise_tools,
                   'identitymanager':enterprise_services,
                   'networkmap':enterprise_services,
                   'signer':enterprise_services}

    @classmethod
    def lookup(cls, artifact):
        if not cls.components.has_key(artifact):
            raise Exception('Unknown artifact for CENM distribution')
        else: return cls.components[artifact]


class CordaType:
    """Class for the supported Corda distribution types.

    Allows for differentiating against enterprise and open source versions of Corda,
    and also for versioned releases vs snapshot releases. This is because there are
    a total of four separate locations in artifactory where these are located i.e.
    corda-releases/net/corda and corda-dev/net/corda for open source released versions
    and snapshot versions respectively, and r3-corda-releases/com/r3/corda and
    r3-corda-dev/com/r3/corda for enterprise.
    """
    os = Distribution('net.corda', 'corda-releases', 'OS', False)
    os_snapshot = Distribution('net.corda', 'corda-dev', 'OS', False)
    enterprise = Distribution('com.r3.corda', 'r3-corda-releases', 'ENT', True)
    enterprise_snapshot = Distribution('com.r3.corda', 'r3-corda-dev', 'ENT', True)

    @classmethod
    def forType(cls, type):
        if type == 'OS': return cls.os
        if type == 'OS_SNAPSHOT': return cls.os_snapshot
        if type == 'ENT': return cls.enterprise
        if type == 'ENT_SNAPSHOT': return cls.enterprise_snapshot


class CordaDistribution():
    """Class to hold distribution details (type and version) of a Corda release. """

    def __init__(self, type, version):
        """Class constructor.

        :param type: The Corda distribution type
        :param version: The version string for the release
        """
        self.type = type
        self.version = version
        self.major = self.parseMajor(version)


    def parseMajor(self, version):
        """Get the major release version.

        :param version: The textual version e.g. OS-4.1-RC03
        :return: An integer representation of the major version
        """
        return (version.split('-')[0]).split('.')[0]


    def isOS(self):
        """Return true if this is an open source type of product."""
        return self.type.product ==  'OS'
