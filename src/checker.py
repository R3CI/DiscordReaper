from src import *
from src.utils.logging import logger
from src.utils.discord import discord
from src.utils.sessionmanager import client as Client


class checker:
    def __init__(self):
        self.alive     = []
        self.dead      = []
        self.locked    = []
        self.checked   = 0
        self.total     = 0
        self.requests  = 0
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
                'alive':    len(self.alive),
                'dead':     len(self.dead),
                'locked':   len(self.locked),
                'requests': self.requests,
                'running':  self.running,
            }


    def notify(self):
        if self.onupdate:
            try:
                self.onupdate(self.getstats())

            except Exception:
                pass


    def checktoken(self, client: Client):
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me')
                with self.lock:
                    self.requests += 1

                if r.status_code == 200:
                    return 'alive'

                if r.status_code == 401 or discord.DEAD_ACCOUNT in r.text:
                    return 'dead'

                if (discord.LOCKED_TOKEN in r.text or discord.PHONE_VERIFICATION_REQUIRED in r.text
                        or discord.EMAIL_VERIFICATION_REQUIRED in r.text or discord.LOCKED_ACCOUNT in r.text):
                    return 'locked'

                if discord.RETRY_AFTER_LIMITED in r.text:
                    try:
                        discord.sleep(min(r.json().get('retry_after', 5), 30))
                    except Exception:
                        discord.sleep(5)

                elif discord.CLOUDFLARE in r.text:
                    discord.sleep(10)

                else:
                    return 'dead'

            except Exception:
                return 'dead'


    def process(self, client: Client):
        status = self.checktoken(client)

        with self.lock:
            self.checked += 1

            if status == 'alive':
                self.alive.append(client.token)
                logger.success(f'{client.maskedtoken} » Alive', 'Checker')

            elif status == 'locked':
                self.locked.append(client.token)
                logger.warning(f'{client.maskedtoken} » Locked', 'Checker')

            else:
                self.dead.append(client.token)
                logger.error(f'{client.maskedtoken} » Dead', 'Checker')

        self.notify()

        if self.onresult:
            try:
                self.onresult(client.token, status)

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
                logger.error(f'{client.maskedtoken} » {e}', 'Checker')

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
        self.alive    = []
        self.dead     = []
        self.locked   = []
        self.checked  = 0
        self.total    = len(tokens)
        self.requests = 0
        self.thread   = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='checker')
        self.thread.start()
        logger.info(f'Checker started  tokens={len(tokens)}', 'Checker')
        return True


    def stop(self):
        self.stopevent.set()
        logger.info('Checker stop requested', 'Checker')
