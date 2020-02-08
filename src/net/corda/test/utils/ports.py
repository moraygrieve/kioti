from requests import get

rangeAllocated = []

def getIPAddr(local):
    """Get this machines publically facing IP Address

    :return: Textual IP Address
    """
    ipaddr = 'localhost'
    if not local:
        try:
            ipaddr = get('https://api.ipify.org').text
        except: pass
    return ipaddr

