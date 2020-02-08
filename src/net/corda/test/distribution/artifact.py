import os, zipfile
from artifactory import ArtifactoryPath
from pysys import log
from pysys.constants import PROJECT
from net.corda.test.constants import REMOTE_STAGING, ARTIFACTORY_URL
from net.corda.test.distribution import CENMType, MidstackType

def getCordaArtifact(distribution, artifact):
    """Download a Corda artifact from artifactory and store in the staging area.

    If the artifact already exists in the staging area, this method will not over-write
    with a new download.

    :param distribution: The version of the artifact
    :param artifact: The name of the artifact
    :return: The path to the downloaded artifact
    """
    download_dir = os.path.join(REMOTE_STAGING, 'corda', distribution.type.product)
    target = os.path.join(download_dir, '%s-%s.jar' % (artifact, distribution.version))

    if not os.path.exists(download_dir): os.makedirs(download_dir)

    if not os.path.exists(target):
        log.info('Downloading artifact %s-%s.jar' % (artifact, distribution.version))

        baseurl = '%s/%s/%s' % (ARTIFACTORY_URL, distribution.type.repositoryId, distribution.type.groupId.replace('.', '/'))
        url = '%s/%s/%s/%s-%s.jar' % (baseurl, artifact, distribution.version, artifact, distribution.version)
        path = ArtifactoryPath(url, auth=(PROJECT.CORDA_ARTIFACTORY_USERNAME, PROJECT.CORDA_ARTIFACTORY_PASSWORD))
        with path.open() as fd:
            with open(target, 'wb') as out:
                out.write(fd.read())
    return target


def getCENMArtifact(version, artifact):
    """Download a CENM artifact from artifactory and store in the staging area.

    If the artifact already exists in the staging area, this method will not over-write
    with a new download.

    :param version: The version of the artifact
    :param artifact: The name of the artifact
    :return: The path to the downloaded artifact
    """
    download_dir = os.path.join(REMOTE_STAGING, 'cenm', artifact.replace('-',''))
    target = os.path.join(download_dir, '%s-%s.zip' % (artifact, version))

    if not os.path.exists(download_dir): os.makedirs(download_dir)

    if not os.path.exists(target):
        log.info('Downloading artifact %s-%s.zip' % (artifact, version))

        type = CENMType.lookup(artifact)
        baseurl = '%s/%s/%s' % (ARTIFACTORY_URL, type.repositoryId, type.groupId.replace('.', '/'))
        url = '%s/%s/%s/%s-%s.zip' % (baseurl, artifact, version, artifact, version)
        path = ArtifactoryPath(url, auth=(PROJECT.CORDA_ARTIFACTORY_USERNAME, PROJECT.CORDA_ARTIFACTORY_PASSWORD))
        with path.open() as fd:
            with open(target, 'wb') as out:
                out.write(fd.read())
        with zipfile.ZipFile(target, 'r') as zip_ref:
            zip_ref.extractall(download_dir)
    return os.path.join(download_dir, '%s.jar' % artifact.replace('-',''))


def getMidStackArtifact(version, artifact):
    """Download a midstack artifact from artifactory and store in the staging area.

    If the artifact already exists in the staging area, this method will not over-write
    with a new download.

    :param version: The version of the artifact
    :param artifact: The name of the artifact
    """
    download_dir = os.path.join(REMOTE_STAGING, 'midstack')
    target = os.path.join(download_dir, '%s-%s.jar' % (artifact, version))

    if not os.path.exists(download_dir): os.makedirs(download_dir)

    if not os.path.exists(target):
        log.info('Downloading artifact %s-%s.jar' % (artifact, version))

        type = MidstackType.lookup(artifact)
        baseurl = '%s/%s/%s' % (ARTIFACTORY_URL, type.repositoryId, type.groupId.replace('.', '/'))
        url = '%s/%s/%s/%s-%s.jar' % (baseurl, artifact, version, artifact, version)
        path = ArtifactoryPath(url, auth=(PROJECT.CORDA_ARTIFACTORY_USERNAME, PROJECT.CORDA_ARTIFACTORY_PASSWORD))
        with path.open() as fd:
            with open(target, 'wb') as out:
                out.write(fd.read())
    return target