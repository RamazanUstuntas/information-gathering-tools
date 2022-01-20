def WhoisQuery(value):
    whoisData = collections.OrderedDict()
    whoisData["name"] = ["-", "Name:"]
    whoisData["org"] = ["-", "Organization:"]
    whoisData["address"] = ["-", "Address:"]
    whoisData["city"] = ["-", "City:"]
    whoisData["zipcode"] = ["-", "Zip code:"]
    whoisData["country"] = ["-", "Country:"]
    whoisData["emails"] = ["-", "Emails:"]
    whoisData["registrar"] = ["-", "Registrar:"]
    whoisData["whois_server"] = ["-", "Whois Server:"]
    whoisData["updated_date"] = ["-", "Updated Date:"]
    whoisData["expiration_date"] = ["-", "Expiration Date:"]
    whoisData["creation_date"] = ["-", "Creation Date:"]
    whoisData["name_servers"] = ["-", "Name Servers:"]

    domain = whois.whois(value)

    for rec in whoisData:
        if domain[rec]:
            if isinstance(domain[rec], list):
                if rec == 'name_servers':
                    whoisData[rec][0] = []
                    for val in domain[rec]:
                        whoisData[rec][0].append(val + ":" + VerifyHostname(val))
                else:
                    whoisData[rec][0] = []
                    for val in domain[rec]:
                        whoisData[rec][0].append(val)
            else:
                whoisData[rec][0] = str(domain[rec])

    return whoisData


def _query(value, dnsserver, record):
    myresolver = dns.resolver.Resolver()
    myresolver.nameservers = [dnsserver]

    try:
        answers = myresolver.query(value, record)
        for answer in answers:
            # TODO check: this for loop is returning on first loop
            if record == 'NS':
                return answer.to_text() + ":" + VerifyHostname(answer.to_text())
            elif record == 'MX':
                domain_name = re.search(' (.*)\.', answer.to_text(), re.IGNORECASE).group(1)
                return answer.to_text() + ":" + VerifyHostname(domain_name)
            else:
                return answer.to_text()
    except Exception:
        return '-'

    return None  # dnsData?


def DnsQuery(value, dnsserver, record=None):
    """ Perform DNS queries  """
    dnsData = {
        "A": [],
        "CNAME": [],
        "HINFO": [],
        "MX": [],
        "NS": [],
        "PTR": [],
        "SOA": [],
        "TXT": [],
        "SPF": [],
        "SRV": [],
        "RP": []
    }

    if record is None:
        for record in dnsData:
            dnsData[record].append(_query(value, dnsserver, record))
    else:
        dnsData[record].append(_query(value, dnsserver, record))

    return dnsData


def ReverseIPQuery(value, dnsserver):
    """ IP DNS Reverse lookup """
    try:
        revname = reversename.from_address(value)
        myresolver = dns.resolver.Resolver()
        myresolver.nameservers = [dnsserver]
        return str(myresolver.query(revname, 'PTR')[0]).rstrip('.')
    except Exception as e:
        print(e)
        return ''
