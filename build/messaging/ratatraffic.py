from requests import Request, Session

'''

Requests helpers to consume rata.digitraffic API. Consume a single or batched calls to https://rata.digitraffic.fi/api/v1/ 


Usage:

# Single API request
trains = ratatraffic.Simple("api/v1").get(payload={})
        .onSuccess(lambda response, status, data: ())
        .onFailure(lambda response, status, data: ())
data = trains.send()


# Multiple API requests
batch = ratatraffic.Batch()
        .get("api/v1/station/KKN", payload={}, onsuccess=onsuccess1, onfailure=onfailure1)
        .get("api/v1/station/HKI", payload={}, onsuccess=onsuccess2, onfailure=onsuccess2)
        .get("api/v1/station/LPI", onsuccess=onsuccess3)

batch.send()

'''

HOSTNAME = "https://rata.digitraffic.fi/api/v1/"


__all__ = [
    'Simple',
    'Batch'
]

_default_onSuccess = lambda res, status, data : print("successful fetch: " + str(res.status_code), res.text)
_default_onFailure = lambda res, status, data : print(f"Error: {status}") if status == 400 else print(f"Internal Error: {status}"),



class Simple:
    '''
   Consume a single API request and return an immediate response. Use onSuccess() and onFailure() callbacks to
    alter the behavior of the response data.
        

    Example usage:

        livedata = rata("live-trains").get(payload={
            'arriving_trains': 5,
            'include_nonstopping': true
        })
            .onSuccess(lambda response, status, data : ())
            .onFailure(lambda response, status, data : ())).send()

        # livedata contains whatever user returns in OnSuccess() or onFailure()

    '''
    def __init__(self, route):
        self.router = HOSTNAME + route
        self.request = None
        self.session = Session()

        self._on_success = _default_onSuccess
        self._on_failure = _default_onFailure


    def onSuccess(self, func):
        if callable(func):
            self._on_success = func
        return self

    def onFailure(self, func):
        if callable(func):
            self._on_failure= func
        return self


    def get(self, payload=None, headers=None, auth=None):
        req = Request('GET', self.router, params=payload, auth=auth, headers=headers)
        self.request = self.session.prepare_request(req)
        return self

    def post(self, payload=None, headers=None, auth=None):
        req = Request('POST', self.router, data=payload, auth=auth, headers=headers)
        self.request = self.session.prepare_request(req)
        return self
        

    def send(self):
        res = self.session.send(self.request)
        if res.ok:
            return self._on_success(res, res.status_code, res.content)
        else:
            return self._on_failure(res, res.status_code, res.content)


########################################################################
###  Batch
########################################################################


class Batch:
    '''
    Consume multiple API requests in a single Session using a queue. Use onSuccess() and onFailure() callbacks to
    alter the behavior of each Request.

    '''

    def __init__(self):
        self.session = Session()
        self._queue = []


    def get(self, route, payload=None, onSuccess=_default_onSuccess, onFailure=_default_onFailure, auth=None, headers=None):
        request = self.session.prepare_request(Request('GET', HOSTNAME + route, params=payload, auth=auth, headers=headers))
        self._queue.append((request, onSuccess, onFailure))
        return self

    def post(self, route, payload=None, onSuccess=_default_onSuccess, onFailure=_default_onFailure, auth=None, headers=None):
        request = self.session.prepare_request(Request('POST', HOSTNAME + route, data=payload, auth=auth, headers=headers))
        self._queue.append((request, onSuccess, onFailure))
        return self


    def flush(self):
        self.session = Session()
        self._queue = []
        return self


    def send(self):
        for request, onSuccess, onFailure in self._queue:
            res = self.session.send(request)
            if res.ok:
                onSuccess(res, res.status_code, res.content)
            else: 
                onFailure(res, res.status_code, res.content)