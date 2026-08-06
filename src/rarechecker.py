import datetime
from src import *
from src.utils.logging import logger
from src.utils.discord import discord
from src.utils.sessionmanager import client as Client


BADGE_FLAGS = {
    1:       'Staff',
    2:       'Partner',
    4:       'HypeSquad Events',
    8:       'Bug Hunter',
    64:      'HypeSquad Bravery',
    128:     'HypeSquad Brilliance',
    256:     'HypeSquad Balance',
    512:     'Early Supporter',
    16384:   'Bug Hunter 2',
    65536:   'Verified Developer',
    131072:  'Certified Moderator',
    4194304: 'Active Developer',
}


def parsebadges(flags):
    return [name for bit, name in BADGE_FLAGS.items() if flags & bit]


def rarescore(username, year, badges):
    score = 0
    n = len(username)

    if n <= 3:    score += 40
    elif n == 4:  score += 25
    elif n == 5:  score += 15
    elif n == 6:  score += 10
    elif n == 7:  score += 5

    if year <= 2015:   score += 30
    elif year == 2016: score += 20
    elif year == 2017: score += 15
    elif year == 2018: score += 10
    elif year == 2019: score += 5

    rare = {'Staff', 'Partner', 'Early Supporter', 'Bug Hunter', 'Bug Hunter 2', 'Verified Developer', 'Certified Moderator'}
    score += sum(10 for b in badges if b in rare)

    if username.isdigit():
        score += 5

    return min(score, 100)


class rarechecker:
    def __init__(self):
        self.results   = []
        self.checked   = 0
        self.total     = 0
        self.requests  = 0
        self.rare      = 0
        self.lock      = threadinglib.Lock()
        self.stopevent = threadinglib.Event()
        self.running   = False
        self.thread    = None
        self.onupdate  = None
        self.ondone    = None
        self.onresult  = None


    def setonupdate(self, fn):
        self.onupdate = fn


    def setondone(self, fn):
        self.ondone = fn


    def setonresult(self, fn):
        self.onresult = fn


    def getstats(self):
        with self.lock:
            return {
                'checked':  self.checked,
                'total':    self.total,
                'rare':     self.rare,
                'requests': self.requests,
                'running':  self.running,
            }


    def getresults(self):
        with self.lock:
            return list(self.results)


    def notify(self):
        if self.onupdate:
            try:
                self.onupdate(self.getstats())

            except Exception:
                pass


    def fetchme(self, client: Client):
        retries = max(1, int(self.settings.get('retries', 3)))
        delay   = max(0.0, float(self.settings.get('retry_delay', 1.0)))
        for attempt in range(retries):
            try:
                while True:
                    r = client.sess.get('https://discord.com/api/v9/users/@me')
                    with self.lock:
                        self.requests += 1

                    if r.status_code == 200:
                        return r.json()

                    if r.status_code == 401 or discord.DEAD_ACCOUNT in r.text:
                        return None

                    if discord.RETRY_AFTER_LIMITED in r.text:
                        try:
                            discord.sleep(min(r.json().get('retry_after', 5), 30))
                        except Exception:
                            discord.sleep(5)

                    elif discord.CLOUDFLARE in r.text:
                        discord.sleep(10)

                    else:
                        return None

            except Exception:
                if attempt < retries - 1:
                    time.sleep(delay)
        return None


    def process(self, client: Client):
        user = self.fetchme(client)

        if user is None:
            with self.lock:
                self.checked += 1
            self.notify()
            return

        uid      = user.get('id', '0')
        username = user.get('username', '?')
        flags    = user.get('public_flags', 0)

        try:
            ts      = ((int(uid) >> 22) + 1420070400000) / 1000
            dt      = datetime.datetime.utcfromtimestamp(ts)
            year    = dt.year
            created = dt.strftime('%Y-%m-%d')
        except Exception:
            year    = 2024
            created = '?'

        badges = parsebadges(flags)
        score  = rarescore(username, year, badges)
        israre = score >= 20

        if username.isdigit():
            usertype = 'numeric'
        elif username.isalpha():
            usertype = 'alpha'
        else:
            usertype = 'mixed'

        entry = {
            'token':    client.token,
            'username': username,
            'uid':      uid,
            'created':  created,
            'year':     year,
            'length':   len(username),
            'type':     usertype,
            'badges':   badges,
            'score':    score,
            'rare':     israre,
        }

        with self.lock:
            self.checked += 1

            if israre:
                self.rare += 1

            self.results.append(entry)

        logger.success(f'{client.maskedtoken} » {username}  score={score}  rare={israre}', 'RareChecker')
        self.notify()

        if self.onresult:
            try:
                self.onresult(entry)

            except Exception:
                pass


    def run(self, token, sem):
        with sem:
            if self.stopevent.is_set():
                return
            client = Client(token)
            try:
                self.process(client)
            except Exception as e:
                logger.error(f'{client.maskedtoken} » {e}', 'RareChecker')
            finally:
                client.close()


    def worker(self, tokens):
        concurrency = max(1, min(int(self.settings.get('concurrency', 50)), 1000))
        sem         = threadinglib.Semaphore(concurrency)
        threads     = []

        for token in tokens:
            t = threadinglib.Thread(target=self.run, args=(token, sem), daemon=True)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.running = False

        if self.ondone:
            try:
                self.ondone()

            except Exception:
                pass


    def start(self, tokens, settings):
        if self.running:
            return False
        self.stopevent.clear()
        self.running  = True
        self.settings = settings
        self.results  = []
        self.checked  = 0
        self.total    = len(tokens)
        self.requests = 0
        self.rare     = 0
        self.thread   = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='rarechecker')
        self.thread.start()
        logger.info(f'RareChecker started  tokens={len(tokens)}', 'RareChecker')
        return True


    def stop(self):
        self.stopevent.set()
        logger.info('RareChecker stop requested', 'RareChecker')
