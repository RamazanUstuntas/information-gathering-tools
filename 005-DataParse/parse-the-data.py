# ##########  Parse the Results to get usefull data ############## #

def CleanHTML(results):
    """ Clean HTML tags """
    res = results
    res = re.sub('<em>', '', res)
    res = re.sub('<b>', '', res)
    res = re.sub('</b>', '', res)
    res = re.sub('</em>', '', res)
    res = re.sub('%2f', ' ', res)
    res = re.sub('%3a', ' ', res)
    res = re.sub('<strong>', '', res)
    res = re.sub('</strong>', '', res)
    res = re.sub('<wbr>', '', res)
    res = re.sub('</wbr>', '', res)
    res = re.sub('&lt;', '', res)

    return res


def GetEmails(results, value):
    """ Extract Emails """
    res = results
    res = CleanHTML(res)

    # todo this regex needs improvement per case/service
    temp = re.compile(
        '[a-zA-Z0-9.\-_+#~!$&\',;=:]+' +
        '@' +
        '[a-zA-Z0-9.-]*' +
        value)

    emails = temp.findall(res)
    final = []
    for email in emails:
        final.append(email.lower())

    return sorted(set(final))


def GetHostnames(results, value):
    """ Extract Hostnames """
    res = results
    res = CleanHTML(res)

    temp = re.compile('[a-zA-Z0-9.-]*\.' + value)
    hostnames = temp.findall(res)
    final = []
    for host in hostnames:
        final.append(host.lower())

    return sorted(set(final))


def GetHostnamesAll(results):
    """ Get All Hostnames """
    res = results
    temp = re.compile('<cite>(.*?)</cite>')
    hostname = temp.findall(res)
    vhosts = []

    for x in hostname:
        r = ''
        if x.count(':'):
            r = x.split(':')[1].split('/')[2]
        else:
            r = x.split("/")[0]
        vhosts.append(r)

    return sorted(set(vhosts))


def GetDNSDumpsterHostnames(value, results):
    tbl_regex = re.compile('<a name="hostanchor"><\/a>Host Records.*?<table.*?>(.*?)</table>',
                           re.S)
    link_regex = re.compile('<td class="col-md-4">(.*?)<br>', re.S)
    subdomains = []

    try:
        results_tbl = tbl_regex.findall(results)[0]
    except IndexError:
        results_tbl = ''
    links_list = link_regex.findall(results_tbl)
    links = list(set(links_list))

    for link in links:
        subdomain = link.strip()
        if not subdomain.endswith(value):
            continue
        if subdomain and subdomain not in subdomains and subdomain != value:
            subdomains.append(subdomain.strip())

    return sorted(set(subdomains))


def SpyseGetDomains(data):
    """
    :type data: dict
    :rtype: list
    """
    domains = []
    try:
        domains = [i['name'] for i in data['data']['items']]
    except IndexError:
        print("Unrecognised data returned by Spyse")

    return domains