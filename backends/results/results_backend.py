class ResultsBackend(object):

    def __init__(self):
        pass

    def process(self, rawdetails):
        wr = rawdetails[1]
        if wr:
            available = wr.pop('available', '')
            if available == -1:
                available = 'unavailable'
            elif available == 1:
                available = 'available'
            else:
                available = 'unknown'
            result = ' '.join(wr.pop('result', ''))
            error = ' '.join(wr.pop('error', ''))
            expiry = ''
            try:
                expiry = ' '.join(wr.pop('expiry', ''))
            except TypeError:  # found a boolean? -> just ignore
                pass
            self.write(rawdetails[0], [available, expiry, result, error])

    def write(self, domain, domain_details):
        pass