# ############### Check Domain, IP, Hostname  ###################### #

def CheckDomain(value):
    """ Validate Domain name """
    if not validators.domain(value):
        raise argparse.ArgumentTypeError('Invalid {} domain.'.format(value))
    return value


def CheckDomainOrIP(value):
    """ Verify domain/ip  """
    if not validators.domain(value) and not validators.ip_address.ipv4(value):
        raise argparse.ArgumentTypeError('Invalid domain or ip address ({}).'.format(value))
    return value


def VerifyHostname(value):
    """ Get Domain ip address """
    try:
        ip = socket.gethostbyname(value)
        return ip
    except Exception as e:
        return False
