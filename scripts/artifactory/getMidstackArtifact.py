#!/usr/bin/env python 

import os, collections
from artifactory import ArtifactoryPath

ARTIFACTORY_URL = 'https://ci-artifactory.corda.r3cev.com/artifactory'

Distribution = collections.namedtuple('Distribution', 'groupId repositoryId product requireAuthentication')

class Type:
    TOKENS_LIB = Distribution('com.r3.corda.lib.tokens', 'corda-lib', 'OS', False)
    CI_LIB_DEV = Distribution('com.r3.corda.lib.ci', 'corda-lib-dev', 'OS', False)
    CI_LIB = Distribution('com.r3.corda.lib.ci', 'corda-lib', 'OS', False)

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
    getArtifact(Type.CI_LIB_DEV, '1.0-RC04', 'ci-workflows', os.getcwd())
