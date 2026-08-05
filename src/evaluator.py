import datetime
from src import *
from src.utils.logging import logger
from src.utils.discord import discord
from src.utils.sessionmanager import client as Client


class evaluator:
    def __init__(self):
        self.results      = []
        self.checked      = 0
        self.total        = 0
        self.valid        = 0
        self.invalid      = 0
        self.requests     = 0
        self.totalguilds  = 0
        self.totaldms     = 0
        self.totalfriends = 0
        self.lock         = threadinglib.Lock()
        self.stopevent    = threadinglib.Event()
        self.running      = False
        self.thread       = None
        self.onupdate     = None
        self.ondone       = None
        self.onresult     = None


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
                'valid':    self.valid,
                'invalid':  self.invalid,
                'guilds':   self.totalguilds,
                'dms':      self.totaldms,
                'friends':  self.totalfriends,
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


    def createddate(self, uid):
        try:
            ts = ((int(uid) >> 22) + 1420070400000) / 1000
            return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        except Exception:
            return '?'


    def fetchme(self, client: Client):
        while True:
            try:
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
                return None


    def fetchguilds(self, client: Client):
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me/guilds')
                with self.lock:
                    self.requests += 1

                if r.status_code == 200:
                    return r.json()

                if r.status_code == 401:
                    return []

                if discord.RETRY_AFTER_LIMITED in r.text:
                    try:
                        discord.sleep(min(r.json().get('retry_after', 5), 30))
                    except Exception:
                        discord.sleep(5)

                elif discord.CLOUDFLARE in r.text:
                    discord.sleep(10)

                else:
                    return []

            except Exception:
                return []


    def fetchdms(self, client: Client):
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me/channels')
                with self.lock:
                    self.requests += 1

                if r.status_code == 200:
                    return [ch for ch in r.json() if ch.get('type') == 1]

                if r.status_code == 401:
                    return []

                if discord.RETRY_AFTER_LIMITED in r.text:
                    try:
                        discord.sleep(min(r.json().get('retry_after', 5), 30))
                    except Exception:
                        discord.sleep(5)

                elif discord.CLOUDFLARE in r.text:
                    discord.sleep(10)

                else:
                    return []

            except Exception:
                return []


    def fetchfriends(self, client: Client):
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me/relationships')
                with self.lock:
                    self.requests += 1

                if r.status_code == 200:
                    return [rel for rel in r.json() if rel.get('type') == 1]

                if r.status_code == 401:
                    return []

                if discord.RETRY_AFTER_LIMITED in r.text:
                    try:
                        discord.sleep(min(r.json().get('retry_after', 5), 30))
                    except Exception:
                        discord.sleep(5)

                elif discord.CLOUDFLARE in r.text:
                    discord.sleep(10)

                else:
                    return []

            except Exception:
                return []


    def process(self, client: Client):
        user = self.fetchme(client)

        if user is None:
            logger.error(f'{client.maskedtoken} » Dead/invalid', 'Evaluator')
            with self.lock:
                self.checked += 1
                self.invalid += 1
            self.notify()
            return

        uid      = user.get('id', '0')
        username = user.get('username', '?')
        created  = self.createddate(uid)

        guilds  = self.fetchguilds(client)
        dms     = self.fetchdms(client)
        friends = self.fetchfriends(client)

        entry = {
            'token':    client.token,
            'username': username,
            'uid':      uid,
            'created':  created,
            'guilds':   len(guilds),
            'dms':      len(dms),
            'friends':  len(friends),
        }

        with self.lock:
            self.checked      += 1
            self.valid        += 1
            self.totalguilds  += len(guilds)
            self.totaldms     += len(dms)
            self.totalfriends += len(friends)
            self.results.append(entry)

        logger.success(
            f'{client.maskedtoken} » {username}  guilds={len(guilds)}  dms={len(dms)}  friends={len(friends)}',
            'Evaluator',
        )
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
                logger.error(f'{client.maskedtoken} » {e}', 'Evaluator')

            finally:
                client.close()


    def worker(self, tokens):
        concurrency = max(1, min(int(self.settings.get('concurrency', 30)), 200))
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
        self.running      = True
        self.settings     = settings
        self.results      = []
        self.checked      = 0
        self.total        = len(tokens)
        self.valid        = 0
        self.invalid      = 0
        self.requests     = 0
        self.totalguilds  = 0
        self.totaldms     = 0
        self.totalfriends = 0
        self.thread       = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='evaluator')
        self.thread.start()
        logger.info(f'Evaluator started  tokens={len(tokens)}', 'Evaluator')
        return True


    def stop(self):
        self.stopevent.set()
        logger.info('Evaluator stop requested', 'Evaluator')
