import threading
import re
from copy import deepcopy
import dns.resolver
import dns.query

import ppwhois

import dead_scrape.domain_data as data


class DomainChecker(threading.Thread):
    
    def __init__(self, thread_id, lock):
        threading.Thread.__init__(self)
        self.lock = lock
        self.cond = threading.Condition(self.lock)
        self.thread_id = thread_id
        self.dresolver = dns.resolver.get_default_resolver()
        self.dnsservers = self.dresolver.nameservers
    
    def run(self):
        more = True
        while more:
            with self.lock:
                while not data.domain_list and not data.domain_list is None:
                    self.cond.wait()
            try:
                with self.lock:
                    if data.domain_list:
                        d = data.domain_list.popleft()
                        d = re.sub(r'www\.', '', d)
                    else:
                        if data.domain_list is None:
                            more = False
                        continue
                if d and re.search(r'^[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*(\.[A-Za-z]{2,})$', d):
                    a = self.__resolve_with_authority__(d, dns.rdatatype.A)
                    top_level = re.search(r'^(com*|net|org*)*\.*[a-z]{2,}\.*$', str(a[0]))
                    if not a[1] or top_level:
                        if not top_level:
                            d = str(a[0])
                        else:
                            p = re.compile('^.*\.([^\.]+\.' + str(a[0])[:-1] + ')')
                            d = re.sub(p, r'\1', d)
                        d = re.sub(r'\.$', '', d)
                        with self.lock:
                            saddr = data.ip_addr.popleft()
                            data.ip_addr.append(saddr)
                            print('No DNS servers found for domain %s. Querying WHOIS from source address %s.' % (d, saddr))
                            retry = 5
                            while retry:
                                try:
                                    w = ppwhois.whois(query=d, source_addr=(saddr, 0), hide_disclaimers=1)
                                    retry = 0
                                except ppwhois.ConnectionReset:
                                    retry -= 1
                            data.nx_domains.append((d, w))
                        
            except IndexError:
                if data.domain_list is None:
                    print('No more domains to try. Thread %d is exiting.' % self.thread_id)
                    more = False
    
    def __resolve_with_authority__(self, name, rdtype):
        nsl = deepcopy(self.dnsservers)
        while nsl:
            nameserver = nsl.pop(0)
            query = dns.message.make_query(name, rdtype)
            try:
                response = dns.query.udp(query, nameserver, timeout=30)
            except dns.exception.Timeout:
                continue
            if response.rcode() != dns.rcode.NOERROR:
                if rdtype == dns.rdatatype.NS:
                    return (name, False)
                nsl = deepcopy(self.dnsservers)
                auth = response.authority.pop()
                if auth.name:
                    new_name = auth.name
                    if new_name == name:
                        return (name, False)
                    name = new_name
                else:
                    return (name, False)
            else:
                return (name, True)
        return (name, False)