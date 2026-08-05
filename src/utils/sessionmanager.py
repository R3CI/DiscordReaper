from src import *
from src.utils.files import files
from src.utils.logging import logger
from curl_cffi.requests import Session as curlsession, AsyncSession as curlasyncsession, Response

import copy

HEADER_ORDER = [
    'Accept',
    'Accept-Encoding',
    'Accept-Language',
    'Authorization',
    'Content-Type',
    'Cookie',
    'Origin',
    'Priority',
    'Referer',
    'Sec-Ch-Ua',
    'Sec-Ch-Ua-Mobile',
    'Sec-Ch-Ua-Platform',
    'Sec-Fetch-Dest',
    'Sec-Fetch-Mode',
    'Sec-Fetch-Site',
    'User-Agent',
    'X-Captcha-Key',
    'X-Captcha-Rqtoken',
    'X-Captcha-Session-Id',
    'X-Context-Properties',
    'X-Debug-Options',
    'X-Discord-Locale',
    'X-Discord-Timezone',
    'X-Super-Properties',
]


def reorderheaders(headers):
    normalized = {k.lower(): v for k, v in headers.items()}
    headermap  = {k.lower(): k for k in HEADER_ORDER}

    ordered = {}
    for canonical in HEADER_ORDER:
        key = canonical.lower()
        if key in normalized:
            ordered[canonical] = normalized[key]

    for key_lower, value in normalized.items():
        if key_lower not in headermap:
            title = '-'.join(word.capitalize() for word in key_lower.split('-'))
            ordered[title] = value

    return ordered


class apistuffcls:
    chromemajor   = '146'
    chromeversion = '146.0.7151.69'

    def __init__(self):
        self.impersonate = 'chrome146'
        self.useragent   = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{self.chromeversion} Safari/537.36'
        self.sechcua     = self.buildsechcua()
        self.fetchdata()
        self.headers     = self.buildheaders()

    def fetchdata(self):
        try:
            data = requests.get('https://api.sockets.lol/discord/build', timeout=5).json()
            self.buildnumber = data['clients']['Discord']['decoded']['client_build_number']
        except Exception:
            self.buildnumber = 507104

    def buildsechcua(self):
        return f'"Chromium";v="{self.chromemajor}", "Google Chrome";v="{self.chromemajor}", "Not/A)Brand";v="99"'

    def buildheaders(self):
        return reorderheaders({
            'Accept':             '*/*',
            'Accept-Encoding':    'gzip, deflate, br, zstd',
            'Accept-Language':    'en-US,en;q=0.9',
            'Authorization':      None,
            'Content-Type':       'application/json',
            'Origin':             'https://discord.com',
            'Priority':           'u=1, i',
            'Referer':            'https://discord.com/channels/@me',
            'Sec-Ch-Ua':          self.sechcua,
            'Sec-Ch-Ua-Mobile':   '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest':     'empty',
            'Sec-Fetch-Mode':     'cors',
            'Sec-Fetch-Site':     'same-origin',
            'User-Agent':         self.useragent,
            'X-Debug-Options':    'bugReporterEnabled',
            'X-Discord-Locale':   'en-US',
            'X-Discord-Timezone': 'America/New_York',
            'X-Super-Properties': None,
        })

    def makexsuper(self):
        props = OrderedDict([
            ('os',                       'Windows'),
            ('browser',                  'Chrome'),
            ('device',                   ''),
            ('system_locale',            'en-US'),
            ('has_client_mods',          False),
            ('browser_user_agent',       self.useragent),
            ('browser_version',          self.chromeversion),
            ('os_version',               '10'),
            ('referrer',                 ''),
            ('referring_domain',         ''),
            ('referrer_current',         'https://discord.com/'),
            ('referring_domain_current', 'discord.com'),
            ('release_channel',          'stable'),
            ('client_build_number',      self.buildnumber),
            ('client_event_source',      None),
            ('client_launch_id',         str(uuid.uuid4())),
            ('launch_signature',         str(uuid.uuid4())),
            ('client_app_state',         'focused'),
        ])
        return base64.b64encode(json.dumps(props, separators=(',', ':')).encode()).decode()

    def encode(self, data):
        return base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()


apistuff = apistuffcls()


def randproxy():
    proxies = files.loadproxies()
    if not proxies:
        return None
    p = random.choice(proxies)
    if not p.startswith('http'):
        p = f'http://{p}'
    return {'http': p, 'https': p}


def makesession():
    return curlsession(impersonate=apistuff.impersonate, default_headers=False)


def makeasyncsession():
    return curlasyncsession(impersonate=apistuff.impersonate)


class sessionwrapper:
    def __init__(self, clientinstance):
        self.client  = clientinstance
        self.session = makesession()

    def _inject(self, kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.client.headers
        if 'headers' in kwargs and kwargs['headers']:
            kwargs['headers'] = {k: v for k, v in kwargs['headers'].items() if v is not None}
        if 'proxies' not in kwargs:
            proxy = randproxy()
            if proxy:
                kwargs['proxies'] = proxy
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 15
        return kwargs

    def _dispatch(self, method, *args, **kwargs):
        injected = self._inject(kwargs)
        fn = getattr(self.session, method)
        return fn(*args, **injected)

    def get(self, *args, **kwargs) -> Response:
        return self._dispatch('get', *args, **kwargs)

    def post(self, *args, **kwargs) -> Response:
        return self._dispatch('post', *args, **kwargs)

    def put(self, *args, **kwargs) -> Response:
        return self._dispatch('put', *args, **kwargs)

    def delete(self, *args, **kwargs) -> Response:
        return self._dispatch('delete', *args, **kwargs)

    def patch(self, *args, **kwargs) -> Response:
        return self._dispatch('patch', *args, **kwargs)

    def close(self):
        try:
            self.session.close()
        except Exception:
            pass


class client:
    def __init__(self, token=None):
        self.token       = token
        self.maskedtoken = token[:25] if token else None

        self.useragent = apistuff.useragent
        self.headers   = copy.deepcopy(apistuff.headers)
        self.sess      = sessionwrapper(self)

        if token:
            self.settoken(token)
            self.addxsup(apistuff.makexsuper())

    def _removeheader(self, name):
        lower = name.lower()
        for key in list(self.headers.keys()):
            if key.lower() == lower:
                self.headers.pop(key, None)

    def _setheader(self, name, value):
        self._removeheader(name)
        self.headers[name] = value
        self.headers = reorderheaders(self.headers)

    def addxsup(self, xsuper):
        self._setheader('X-Super-Properties', xsuper)

    def setreferrer(self, referer):
        self._setheader('Referer', referer)

    def addxcontent(self, xcontent):
        self._setheader('X-Context-Properties', apistuff.encode(xcontent))

    def cleanxcontent(self):
        self._removeheader('X-Context-Properties')
        self.headers = reorderheaders(self.headers)

    def cleancaptchastuff(self):
        for header in ('X-Captcha-Session-Id', 'X-Captcha-Rqtoken', 'X-Captcha-Key'):
            self._removeheader(header)
        self.headers = reorderheaders(self.headers)

    def settoken(self, token):
        if token:
            self._setheader('Authorization', token)

    def close(self):
        self.sess.close()
