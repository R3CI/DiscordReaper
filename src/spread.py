import re
import string
from src import *
from src.utils.files import files
from src.utils.logging import logger
from src.utils.discord import discord
from src.utils.sessionmanager import client as Client


class spread:
    def __init__(self):
        self.svtext    = ''
        self.dmtext    = ''
        self.settings  = {}
        self.sent      = 0
        self.failed    = 0
        self.dead      = 0
        self.locked    = 0
        self.died      = 0
        self.dms       = 0
        self.channels  = 0
        self.requests  = 0
        self.total     = 0
        self.checked   = 0
        self.lock      = threadinglib.Lock()
        self.stopevent = threadinglib.Event()
        self.running   = False
        self.thread    = None
        self.onupdate  = None
        self.ondone    = None


    def resolvetext(self, text, recipid=None):
        _chars = string.ascii_letters + string.digits
        def sub(m):
            tok = m.group(1)
            if tok == 'ping:everyone':
                return '@everyone'
            if tok == 'ping:here':
                return '@here'
            if tok == 'ping:dm':
                return f'<@{recipid}>' if recipid else ''
            if tok.startswith('ping:user:'):
                uid = tok[len('ping:user:'):]
                return f'<@{uid}>' if uid else ''
            if tok.startswith('random:'):
                try:
                    n = max(1, min(int(tok[7:]), 500))
                    return ''.join(random.choices(_chars, k=n))
                except Exception:
                    return ''
            if tok.startswith('file:') or tok.startswith('image:'):
                return ''
            return m.group(0)
        return re.sub(r'\{([^}]+)\}', sub, text).strip()


    def setonupdate(self, fn):
        self.onupdate = fn


    def setondone(self, fn):
        self.ondone = fn


    def getstats(self):
        with self.lock:
            return {
                'sent':     self.sent,
                'failed':   self.failed,
                'dead':     self.dead,
                'locked':   self.locked,
                'died':     self.died,
                'dms':      self.dms,
                'channels': self.channels,
                'requests': self.requests,
                'total':    self.total,
                'checked':  self.checked,
            }


    def notify(self):
        if self.onupdate:
            try:
                self.onupdate(self.getstats())

            except Exception:
                pass


    def hasperm(self, chan, gid, member, uid, needeveryone=False):
        sendperm     = 0x800
        viewperm     = 0x400
        adminperm    = 0x8
        everyoneperm = 0x20000

        guildperms = int(member.get('permissions', '0'))
        if guildperms & adminperm:
            return True
        perms      = guildperms
        overwrites = chan.get('permission_overwrites', [])
        roles      = member.get('roles', [])
        for ow in overwrites:
            if ow.get('type') == 0 and ow.get('id') == gid:
                perms = (perms & ~int(ow.get('deny', '0'))) | int(ow.get('allow', '0'))
                break
        ra, rd = 0, 0
        for rid in roles:
            for ow in overwrites:
                if ow.get('type') == 0 and ow.get('id') == rid:
                    ra |= int(ow.get('allow', '0'))
                    rd |= int(ow.get('deny', '0'))
        perms = (perms & ~rd) | ra
        for ow in overwrites:
            if ow.get('type') == 1 and ow.get('id') == uid:
                perms = (perms & ~int(ow.get('deny', '0'))) | int(ow.get('allow', '0'))
                break
        if needeveryone and not (perms & everyoneperm):
            return False
        return bool(perms & viewperm) and bool(perms & sendperm)


    def setdnd(self, client: Client):
        try:
            while True:
                r = client.sess.patch(
                    'https://discord.com/api/v9/users/@me/settings',
                    headers=client.headers,
                    json={'status': 'dnd'},
                )

                if r.status_code == 200:
                    return True

                elif r.status_code == 401:
                    return False

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » DND {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » DND cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    return True

        except Exception:
            return True


    def fetchguilds(self, client: Client):
        try:
            while True:
                r = client.sess.get(
                    'https://discord.com/api/v9/users/@me/guilds',
                    headers=client.headers,
                )

                if r.status_code == 200:
                    return r.json()

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Guilds {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Guilds cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    e, etype = discord.errordatabase(r.text)
                    logger.error(f'{client.maskedtoken} » Failed to get guilds » {e}', 'Spread')
                    return []

        except Exception as e:
            logger.error(f'{client.maskedtoken} » Failed to get guilds » {e}', 'Spread')
            return []


    def fetchchannels(self, client: Client, gid):
        try:
            while True:
                r = client.sess.get(
                    f'https://discord.com/api/v9/guilds/{gid}/channels',
                    headers=client.headers,
                )

                if r.status_code == 200:
                    return r.json()

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Channels {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Channels cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    e, etype = discord.errordatabase(r.text)
                    logger.error(f'{client.maskedtoken} » Failed to get channels » {e}', 'Spread')
                    return []

        except Exception as e:
            logger.error(f'{client.maskedtoken} » Failed to get channels » {e}', 'Spread')
            return []


    def fetchmember(self, client: Client, gid):
        try:
            while True:
                r = client.sess.get(
                    f'https://discord.com/api/v9/users/@me/guilds/{gid}/member',
                    headers=client.headers,
                )

                if r.status_code == 200:
                    return r.json()

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Member {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Member cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    return False

        except Exception:
            return False


    def sendmessage(self, client: Client, chanid, text):
        try:
            with self.lock:
                self.requests += 1

            while True:
                r = client.sess.post(
                    f'https://discord.com/api/v9/channels/{chanid}/messages',
                    headers=client.headers,
                    json={'content': text, 'flags': 0, 'mobile_network_type': 'unknown'},
                )

                if r.status_code == 200:
                    return True, r.text

                elif r.status_code == 401:
                    return False, r.text

                elif r.status_code == 429 or 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Send {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Send cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    return False, r.text

        except Exception as e:
            return False, str(e)


    def fetchdms(self, client: Client):
        try:
            while True:
                r = client.sess.get(
                    'https://discord.com/api/v9/users/@me/channels',
                    headers=client.headers,
                )

                if r.status_code == 200:
                    return r.json()

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » DMs {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » DMs cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    e, etype = discord.errordatabase(r.text)
                    logger.error(f'{client.maskedtoken} » Failed to get DMs » {e}', 'Spread')
                    return []

        except Exception as e:
            logger.error(f'{client.maskedtoken} » Failed to get DMs » {e}', 'Spread')
            return []


    def fetchfriends(self, client: Client):
        try:
            while True:
                r = client.sess.get(
                    'https://discord.com/api/v9/users/@me/relationships',
                    headers=client.headers,
                )

                if r.status_code == 200:
                    return [rel for rel in r.json() if rel.get('type') == 1]

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Friends {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Friends cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    e, etype = discord.errordatabase(r.text)
                    logger.error(f'{client.maskedtoken} » Failed to get friends » {e}', 'Spread')
                    return []

        except Exception as e:
            logger.error(f'{client.maskedtoken} » Failed to get friends » {e}', 'Spread')
            return []


    def createdm(self, client: Client, userid):
        try:
            while True:
                r = client.sess.post(
                    'https://discord.com/api/v9/users/@me/channels',
                    headers=client.headers,
                    json={'recipient_id': userid},
                )

                if r.status_code == 200:
                    return r.json().get('id')

                elif r.status_code == 401:
                    return None

                elif 'retry_after' in r.text:
                    ratelimit = r.json().get('retry_after', 5)
                    logger.ratelimit(f'{client.maskedtoken} » Open DM {ratelimit}s', 'Spread')
                    discord.sleep(min(float(ratelimit), 30))

                elif 'Cloudflare' in r.text:
                    logger.ratelimit(f'{client.maskedtoken} » Open DM cloudflare 10s', 'Spread')
                    discord.sleep(10)

                else:
                    e, etype = discord.errordatabase(r.text)
                    logger.error(f'{client.maskedtoken} » Failed to open DM » {e}', 'Spread')
                    return False

        except Exception as e:
            logger.error(f'{client.maskedtoken} » Failed to open DM » {e}', 'Spread')
            return False


    def muteserver(self, client: Client, gid):
        try:
            client.sess.patch(
                'https://discord.com/api/v9/users/@me/guilds/settings',
                headers=client.headers,
                json={'guilds': {gid: {'muted': True, 'mute_config': {'selected_time_window': -1, 'end_time': None}}}},
            )

        except Exception:
            pass


    def mutechan(self, client: Client, chanid):
        try:
            client.sess.patch(
                'https://discord.com/api/v9/users/@me/guilds/@me/settings',
                headers=client.headers,
                json={'channel_overrides': {chanid: {'muted': True, 'mute_config': {'selected_time_window': -1, 'end_time': None}}}},
            )

        except Exception:
            pass


    def process(self, client: Client):
        try:
            uid = discord.getid(client.token)

        except Exception:
            uid = None

        died       = False
        locked_flg = False
        local_sent = 0

        if self.settings.get('dnd'):
            alive = self.setdnd(client)
            if not alive:
                died = True

        if not died and self.settings.get('servers'):
            blind     = self.settings.get('blindsend', False)
            pingevery = '{ping:everyone}' in self.svtext
            muteafter = self.settings.get('muteafter', False)

            guilds = self.fetchguilds(client)
            if guilds is None:
                died = True

            elif guilds:
                logger.info(f'{client.maskedtoken} » Servers found={len(guilds)}', 'Spread')

                for guild in guilds:
                    if died or self.stopevent.is_set():
                        break

                    gid       = guild.get('id')
                    gname     = guild.get('name', gid)
                    member    = None
                    skipguild = False
                    sentthis  = False

                    if not blind:
                        member = self.fetchmember(client, gid)
                        if member is None:
                            died = True
                            break

                        if member is False:
                            continue

                    channels = self.fetchchannels(client, gid)
                    if channels is None:
                        died = True
                        break

                    for chan in [c for c in channels if c.get('type') == 0]:
                        if died or skipguild or self.stopevent.is_set():
                            break

                        if not blind and not self.hasperm(chan, gid, member, uid, needeveryone=pingevery):
                            continue

                        text     = self.resolvetext(self.svtext)
                        ok, body = self.sendmessage(client, chan['id'], text)
                        channame = chan.get('name', chan['id'])

                        if ok:
                            with self.lock:
                                self.sent     += 1
                                self.channels += 1
                            local_sent += 1
                            sentthis = True
                            logger.success(f'{client.maskedtoken} » Sent server={gname} channel=#{channame}', 'Spread')

                        elif discord.DEAD_ACCOUNT in body or discord.LOCKED_TOKEN in body or discord.BANNED_TOKEN in body or discord.TOKEN_COMPROMISED in body or '401' in body:
                            died     = True
                            if discord.LOCKED_TOKEN in body:
                                locked_flg = True
                            e, etype = discord.errordatabase(body)
                            logger.warning(f'{client.maskedtoken} » Token died » {e}', 'Spread')
                            break

                        elif discord.NO_ACCESS_NOT_INSIDE in body or discord.VERIFICATION_TOO_HIGH in body or discord.UNKNOWN_SERVER in body or discord.NOT_IN_SERVER in body or discord.INVALID_SERVER in body or discord.SERVER_LIMITED_VIOLATED_TOS in body or discord.ACTION_NOT_ALLOWED in body:
                            skipguild = True
                            e, etype  = discord.errordatabase(body)
                            logger.warning(f'{client.maskedtoken} » Server skip={gname} reason={e}', 'Spread')
                            break

                        else:
                            with self.lock:
                                self.failed += 1
                            e, etype = discord.errordatabase(body)
                            logger.error(f'{client.maskedtoken} » Send failed server={gname} channel=#{channame} » {e}', 'Spread')

                        self.notify()

                    if muteafter and sentthis and not died:
                        self.muteserver(client, gid)

        if not died and self.settings.get('dms'):
            muteafter = self.settings.get('muteafter', False)
            dmed      = set()

            dmlist = self.fetchdms(client)
            if dmlist is None:
                died = True

            elif dmlist:
                opendms = [d for d in dmlist if d.get('type') == 1]
                logger.info(f'{client.maskedtoken} » Open DMs found={len(opendms)}', 'Spread')

                for dm in opendms:
                    if died or self.stopevent.is_set():
                        break

                    chanid   = dm['id']
                    recipids = [u.get('id') for u in dm.get('recipients', []) if u.get('id')]
                    recip    = dm.get('recipients', [{}])[0].get('username', chanid)
                    recipid  = recipids[0] if recipids else None
                    text     = self.resolvetext(self.dmtext, recipid=recipid)

                    ok, body = self.sendmessage(client, chanid, text)

                    if ok:
                        with self.lock:
                            self.sent += 1
                            self.dms  += 1
                        local_sent += 1
                        logger.success(f'{client.maskedtoken} » Sent DM to={recip}', 'Spread')
                        if muteafter:
                            self.mutechan(client, chanid)

                    elif discord.DEAD_ACCOUNT in body or discord.LOCKED_TOKEN in body or discord.BANNED_TOKEN in body or discord.TOKEN_COMPROMISED in body or '401' in body:
                        died     = True
                        if discord.LOCKED_TOKEN in body:
                            locked_flg = True
                        e, etype = discord.errordatabase(body)
                        logger.warning(f'{client.maskedtoken} » Token died » {e}', 'Spread')
                        break

                    else:
                        e, etype = discord.errordatabase(body)
                        if discord.DISABLED_DMS in body or discord.CANNOT_DM_THIS_USER in body or discord.UNKNOWN_USER in body or discord.CANNOT_EXECUTE_ACTION in body:
                            logger.info(f'{client.maskedtoken} » DM skip user={recip} reason={e}', 'Spread')

                        else:
                            with self.lock:
                                self.failed += 1
                            logger.error(f'{client.maskedtoken} » DM failed user={recip} » {e}', 'Spread')

                    for u in dm.get('recipients', []):
                        if u.get('id'):
                            dmed.add(u['id'])

                    self.notify()

            if not died:
                friends = self.fetchfriends(client)
                if friends is None:
                    died = True

                elif friends:
                    unsent = [f for f in friends if f.get('id') and f['id'] not in dmed]
                    logger.info(f'{client.maskedtoken} » Friends to DM={len(unsent)}', 'Spread')

                    for rel in unsent:
                        if died or self.stopevent.is_set():
                            break

                        fuid  = rel['id']
                        fname = rel.get('user', {}).get('username', fuid)

                        chanid = self.createdm(client, fuid)
                        if chanid is None:
                            died = True
                            break

                        if not chanid:
                            continue

                        text     = self.resolvetext(self.dmtext, recipid=fuid)
                        ok, body = self.sendmessage(client, chanid, text)

                        if ok:
                            with self.lock:
                                self.sent += 1
                                self.dms  += 1
                            local_sent += 1
                            logger.success(f'{client.maskedtoken} » Sent DM(friend) to={fname}', 'Spread')
                            if muteafter:
                                self.mutechan(client, chanid)

                        elif discord.DEAD_ACCOUNT in body or discord.LOCKED_TOKEN in body or discord.BANNED_TOKEN in body or discord.TOKEN_COMPROMISED in body or '401' in body:
                            died     = True
                            if discord.LOCKED_TOKEN in body:
                                locked_flg = True
                            e, etype = discord.errordatabase(body)
                            logger.warning(f'{client.maskedtoken} » Token died » {e}', 'Spread')
                            break

                        else:
                            e, etype = discord.errordatabase(body)
                            if discord.DISABLED_DMS in body or discord.CANNOT_DM_THIS_USER in body or discord.UNKNOWN_USER in body or discord.CANNOT_EXECUTE_ACTION in body:
                                logger.info(f'{client.maskedtoken} » DM(friend) skip user={fname} reason={e}', 'Spread')

                            else:
                                with self.lock:
                                    self.failed += 1
                                logger.error(f'{client.maskedtoken} » DM(friend) failed user={fname} » {e}', 'Spread')

                        dmed.add(fuid)
                        self.notify()

        with self.lock:
            self.checked += 1
            if died:
                if locked_flg:
                    self.locked += 1
                elif local_sent > 0:
                    self.died   += 1
                else:
                    self.dead   += 1

        if died:
            logger.warning(f'{client.maskedtoken} » Done (died)', 'Spread')

        else:
            logger.success(f'{client.maskedtoken} » Done', 'Spread')

        self.notify()


    def run(self, token, sem):
        with sem:
            if self.stopevent.is_set():
                return

            c = Client(token)

            try:
                self.process(c)

            except Exception as e:
                logger.error(f'{c.maskedtoken} » {e}', 'Spread')

            finally:
                c.close()


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


    def start(self, tokens, svtext, dmtext, settings):
        if self.running:
            return
        self.stopevent.clear()
        self.running  = True
        self.svtext   = svtext
        self.dmtext   = dmtext
        self.settings = settings
        self.sent     = 0
        self.failed   = 0
        self.dead     = 0
        self.locked   = 0
        self.died     = 0
        self.dms      = 0
        self.channels = 0
        self.requests = 0
        self.total    = len(tokens)
        self.checked  = 0
        self.thread   = threadinglib.Thread(target=self.worker, args=(tokens,), daemon=True, name='spread')
        self.thread.start()
        logger.info(f'Spread started tokens={len(tokens)}', 'Spread')


    def stop(self):
        self.stopevent.set()
        logger.info('Spread stop requested', 'Spread')


    def isrunning(self):
        return self.running


spreadhandler = spread
