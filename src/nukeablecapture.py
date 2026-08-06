from src import *
from src.utils.logging import logger
from src.utils.discord import discord
from src.utils.sessionmanager import client as Client


class admincap:
    ADMIN_BIT = 0x8

    def __init__(self):
        self.results   = []
        self.checked   = 0
        self.total     = 0
        self.requests  = 0
        self.found     = 0
        self.guilds    = 0
        self.lock      = threadinglib.Lock()
        self.stopevent = threadinglib.Event()
        self.running   = False
        self.thread    = None
        self.onupdate  = None
        self.ondone    = None
        self.onresult  = None

    def setonupdate(self, fn): self.onupdate = fn
    def setondone(self, fn):   self.ondone   = fn
    def setonresult(self, fn): self.onresult = fn

    def getstats(self):
        with self.lock:
            return {
                'checked':  self.checked,
                'total':    self.total,
                'found':    self.found,
                'guilds':   self.guilds,
                'requests': self.requests,
                'running':  self.running,
            }

    def getresults(self):
        with self.lock:
            return list(self.results)

    def _notify(self):
        if self.onupdate:
            try:
                self.onupdate(self.getstats())
            except Exception:
                pass

    def fetchguilds(self, c):
        while True:
            try:
                r = c.sess.get('https://discord.com/api/v9/users/@me/guilds?with_counts=false')
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
                    return []
            except Exception:
                return []

    def process(self, token):
        client = Client(token)
        try:
            guilds = self.fetchguilds(client)
            if guilds is None:
                logger.error(f'{client.maskedtoken} » Dead', 'NukableCap')
                with self.lock:
                    self.checked += 1
                self._notify()
                return

            adminguilds = []
            for g in guilds:
                try:
                    if int(g.get('permissions', 0)) & self.ADMIN_BIT:
                        adminguilds.append({'guild_id': g['id'], 'guild_name': g.get('name', g['id'])})
                except Exception:
                    pass

            with self.lock:
                self.checked += 1
                if adminguilds:
                    self.found  += 1
                    self.guilds += len(adminguilds)
                    for ag in adminguilds:
                        self.results.append({'token': token, **ag})
                    logger.success(f'{client.maskedtoken} » Admin in {len(adminguilds)} guild(s)', 'NukableCap')
                else:
                    logger.info(f'{client.maskedtoken} » No admin guilds', 'NukableCap')

            self._notify()
            if self.onresult and adminguilds:
                for ag in adminguilds:
                    try:
                        self.onresult(token, ag['guild_name'], ag['guild_id'])
                    except Exception:
                        pass

        except Exception as e:
            logger.error(f'{client.maskedtoken} » {e}', 'NukableCap')
        finally:
            client.close()

    def run(self, token, sem):
        with sem:
            if self.stopevent.is_set():
                return

            retries = max(1, int(self.settings.get('retries', 3)))
            delay   = max(0.0, float(self.settings.get('retry_delay', 1.0)))

            for attempt in range(retries):
                if self.stopevent.is_set():
                    return
                try:
                    self.process(token)
                    return
                except Exception as e:
                    if attempt < retries - 1:
                        logger.warning(f'{token[:24]}... » retry {attempt+2}/{retries}: {e}', 'NukableCap')
                        time.sleep(delay)
                    else:
                        logger.error(f'{token[:24]}... » failed after {retries} tries: {e}', 'NukableCap')

    def worker(self, tokens):
        concurrency = max(1, min(int(self.settings.get('concurrency', 50)), 1000))
        sem = threadinglib.Semaphore(concurrency)
        threads = []
        for token in tokens:
            if self.stopevent.is_set():
                break
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
        self.found    = 0
        self.guilds   = 0
        self.thread   = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='admincap')
        self.thread.start()
        logger.info(f'NukableCap started  tokens={len(tokens)}', 'NukableCap')
        return True

    def stop(self):
        self.stopevent.set()
        logger.info('NukableCap stop requested', 'NukableCap')
