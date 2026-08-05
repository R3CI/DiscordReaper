from src import *
from src.utils.files import files
from curl_cffi.requests import AsyncSession as curlasyncsession, Session as curlsession


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
            self.buildnumber = 588557


    def buildsechcua(self):
        return f'"Chromium";v="{self.chromemajor}", "Google Chrome";v="{self.chromemajor}", "Not/A)Brand";v="99"'


    def buildheaders(self):
        return {
            'Accept':             '*/*',
            'Accept-Encoding':    'gzip, deflate, br, zstd',
            'Accept-Language':    'en-US,en;q=0.9',
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
        }


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


def makesession():
    return curlsession(impersonate=apistuff.impersonate, default_headers=False)


def makeasyncsession():
    return curlasyncsession(impersonate=apistuff.impersonate)


def randproxy():
    proxies = files.loadproxies()
    if not proxies:
        return None
    p = random.choice(proxies)
    if not p.startswith('http'):
        p = f'http://{p}'
    return {'http': p, 'https': p}
