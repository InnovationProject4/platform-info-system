from requests import Request, Session

HOSTNAME = "https://rata.digitraffic.fi/api/v1/"


class rata:
    '''
        Requests Helper

        usage:

        live_trains = rata("live-trains").get(payload={
            'arrived_trains': 0,
            'arriving_trains': 5,
            'departing_trains': 0,
            'departed_trains': 0,
            'include_nonstopping': true
        }).onSuccess(lambda response, status, data : (
            print("success " + data)

        )).onFailure(lambda response, status, data : (
            print("failure " + data)

        )).send()

        # live_trains contains whatever user returns in OnSuccess() or onFailure() depending on
        # return status code.

    '''
    def __init__(self, route):
        self.router = HOSTNAME + route
        self.request = None
        self.session = Session()

    def _on_success(response, status, data):
        print("success " + data)


    def _on_failure(response, status, data):
        print("failure " + data)


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
        if res.status_code == 200:
            return self._on_success(res, res.status_code, res.content)
        else:
            return self._on_failure(res, res.status_code, res.content)