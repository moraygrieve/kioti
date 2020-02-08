#!/usr/bin/env python 

import os, collections
from artifactory import ArtifactoryPath

ARTIFACTORY_URL = 'https://ci-artifactory.corda.r3cev.com/artifactory'

Distribution = collections.namedtuple('Distribution', 'groupId repositoryId product requireAuthentication')

class Type:
    OS = Distribution('net.corda', 'corda-releases', 'OS', False)
    OS_SNAPSHOT = Distribution('net.corda', 'corda-dev', 'OS', False)
    ENTERPRISE = Distribution('com.r3.corda', 'r3-corda-releases', 'ENT', False)
    ENTERPRISE_SNAPSHOT = Distribution('com.r3.corda', 'r3-corda-dev', 'ENT', True)

def getArtifact(type, version, artifact, dest):
    target = os.path.join(dest, '%s-%s.jar' % (artifact, version))
    if not os.path.exists(target):
        print('Downloading artifact %s-%s.jar' % (artifact, version))

        baseurl = '%s/%s/%s' % (ARTIFACTORY_URL, type.repositoryId, type.groupId.replace('.', '/'))
        url = '%s/%s/%s/%s-%s.jar' % (baseurl, artifact, version, artifact, version)
        path = ArtifactoryPath(url, auth=(os.environ.get('CORDA_ARTIFACTORY_USERNAME'), os.environ.get('CORDA_ARTIFACTORY_PASSWORD')))
        with path.open() as fd:
            with open(target, 'wb') as out:
                out.write(fd.read())
    return target

if __name__ == '__main__':
    getArtifact(Type.OS, '4.3', 'corda-tools-network-bootstrapper', os.getcwd())
