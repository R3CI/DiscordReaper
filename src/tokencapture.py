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

NITRO_TYPES = {0: 'None', 1: 'Classic', 2: 'Nitro', 3: 'Basic'}

PAYMENT_TYPES = {1: 'Card', 2: 'PayPal', 8: 'Venmo', 12: 'Bank'}


def parsebadges(flags):
    return [name for bit, name in BADGE_FLAGS.items() if flags & bit]


class tokencapture:
    def __init__(self):
        self.results     = []
        self.checked     = 0
        self.total       = 0
        self.requests    = 0
        self.valid       = 0
        self.invalid     = 0
        self.locked      = 0
        self.withnitro   = 0
        self.withpayment = 0
        self.lock        = threadinglib.Lock()
        self.stopevent   = threadinglib.Event()
        self.running     = False
        self.thread      = None
        self.onupdate    = None
        self.ondone      = None
        self.onresult    = None


    def setonupdate(self, fn):
        self.onupdate = fn


    def setondone(self, fn):
        self.ondone = fn


    def setonresult(self, fn):
        self.onresult = fn


    def getstats(self):
        with self.lock:
            return {
                'checked':     self.checked,
                'total':       self.total,
                'valid':       self.valid,
                'invalid':     self.invalid,
                'locked':      self.locked,
                'withnitro':   self.withnitro,
                'withpayment': self.withpayment,
                'requests':    self.requests,
                'running':     self.running,
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
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me')
                with self.lock:
                    self.requests += 1

                if r.status_code == 200:
                    return r.json(), 'valid'

                if r.status_code == 401 or discord.DEAD_ACCOUNT in r.text:
                    return None, 'invalid'

                if (discord.LOCKED_TOKEN in r.text or discord.PHONE_VERIFICATION_REQUIRED in r.text
                        or discord.EMAIL_VERIFICATION_REQUIRED in r.text or discord.LOCKED_ACCOUNT in r.text):
                    return None, 'locked'

                if discord.RETRY_AFTER_LIMITED in r.text:
                    try:
                        discord.sleep(min(r.json().get('retry_after', 5), 30))
                    except Exception:
                        discord.sleep(5)

                elif discord.CLOUDFLARE in r.text:
                    discord.sleep(10)

                else:
                    return None, 'invalid'

            except Exception:
                return None, 'invalid'


    def fetchpayments(self, client: Client):
        while True:
            try:
                r = client.sess.get('https://discord.com/api/v9/users/@me/billing/payment-sources')
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


    def process(self, client: Client):
        user, status = self.fetchme(client)

        if status != 'valid' or user is None:
            with self.lock:
                self.checked += 1

                if status == 'locked':
                    self.locked += 1

                else:
                    self.invalid += 1

            self.notify()
            return

        uid       = user.get('id', '0')
        username  = user.get('username', '?')
        flags     = user.get('public_flags', 0)
        nitrotype = user.get('premium_type', 0)
        emailok   = bool(user.get('verified', False))
        hasphone  = bool(user.get('phone', None))
        mfa       = bool(user.get('mfa_enabled', False))

        try:
            ts      = ((int(uid) >> 22) + 1420070400000) / 1000
            created = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        except Exception:
            created = '?'

        badges   = parsebadges(flags)
        sources  = self.fetchpayments(client)
        payments = list({PAYMENT_TYPES.get(s.get('type', 0), 'Other') for s in sources if s.get('type')})

        entry = {
            'token':     client.token,
            'username':  username,
            'uid':       uid,
            'status':    status,
            'created':   created,
            'nitro':     nitrotype > 0,
            'nitrotype': NITRO_TYPES.get(nitrotype, 'Unknown'),
            'nitroval':  nitrotype,
            'payment':   payments,
            'badges':    badges,
            'email':     emailok,
            'phone':     hasphone,
            'mfa':       mfa,
        }

        with self.lock:
            self.checked += 1
            self.valid   += 1

            if nitrotype > 0:
                self.withnitro += 1

            if payments:
                self.withpayment += 1

            self.results.append(entry)

        logger.success(
            f'{client.maskedtoken} » {username}  nitro={NITRO_TYPES.get(nitrotype)}  payment={len(payments)}  badges={len(badges)}',
            'TokenCapture',
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
                logger.error(f'{client.maskedtoken} » {e}', 'TokenCapture')

            finally:
                client.close()


    def worker(self, tokens):
        concurrency = max(1, min(int(self.settings.get('concurrency', 30)), 500))
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
        self.running     = True
        self.settings    = settings
        self.results     = []
        self.checked     = 0
        self.total       = len(tokens)
        self.requests    = 0
        self.valid       = 0
        self.invalid     = 0
        self.locked      = 0
        self.withnitro   = 0
        self.withpayment = 0
        self.thread      = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='tokencapture')
        self.thread.start()
        logger.info(f'TokenCapture started  tokens={len(tokens)}', 'TokenCapture')
        return True


    def stop(self):
        self.stopevent.set()
        logger.info('TokenCapture stop requested', 'TokenCapture')
