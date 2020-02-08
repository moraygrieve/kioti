class DistinguisedName:
    email = 'E'
    uuid = 'UID'
    commonName = 'CN'
    title = 'T'
    orgName = 'O'
    orgUnit = 'OU'
    domainComponent = 'DC'
    street	= 'STREET'
    state = 'ST'
    postcode = 'PC'
    locality = 'L'
    country = 'C'
    hostname = 'UNSTRUCTUREDNAME'
    ip = 'UNSTRUCTUREDADDRESS'
    distName = 'DNQ'

    @classmethod
    def parseX509Name(cls, name):
        """Split an X509 name into a dictionay of key value pairs
        """
        entries = map(lambda x: x.strip(), name.split(','))
        return  dict(s.split('=') for s in entries)

    @classmethod
    def getOrganisation(cls, name):
        d = cls.parseX509Name(name)
        if d.has_key(cls.orgName): return d[cls.orgName]
        return None