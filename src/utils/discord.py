from src import *

import re
import string


class discord:
    INVALID_JSON                          = '50109'
    INVALID_JSON_2                        = '50035'
    INTERACTION_FAILED                    = '110000'
    BANNED_TOKEN                          = '40007'
    LOCKED_TOKEN                          = '40002'
    DEAD_ACCOUNT                          = '401'
    LOCKED_ACCOUNT                        = 'You need to verify'
    UNKNOWN_ACCOUNT                       = '40001'
    LIMITED                               = '20028'
    RETRY_AFTER_LIMITED                   = 'retry_after'
    API_BAN                               = 'You are being blocked from accessing our API'
    OPENING_DMS_TOO_FAST                  = '40003'
    CLOUDFLARE                            = 'Cloudflare'
    HCAPTCHA                              = 'captcha_key'
    AUTOMOD_FLAGGED                       = '200000'
    MESSAGE_BLOCKED_BY_CONTENT_FILTER     = '50022'
    NO_ACCESS_NOT_INSIDE                  = '50001'
    MISSING_PERMISSIONS                   = '50013'
    ACTION_NOT_ALLOWED                    = '50007'
    VERIFICATION_TOO_HIGH                 = '50009'
    INVALID_SERVER                        = '50055'
    UNKNOWN_SERVER                        = '10005'
    NOT_IN_SERVER                         = 'Unknown Guild'
    SERVER_LIMITED_VIOLATED_TOS           = '400002'
    MAX_SERVERS                           = '30001'
    ALREADY_A_MEMBER                      = '150009'
    UNKNOWN_INVITE                        = 'Unknown Invite'
    INVALID_INVITE                        = '10006'
    EXPIRED_INVITE                        = '50020'
    CHANNEL_NOT_FOUND                     = '50034'
    UNKNOWN_CHANNEL                       = '10003'
    CANT_DO_THAT_ON_THIS_CHANNEL          = '50024'
    CANNOT_EXECUTE_ACTION                 = '50003'
    NOT_IN_A_VC                           = '50168'
    UNABLE_TO_SEND                        = '50008'
    UNKNOWN_MESSAGE                       = '10008'
    CANT_SEND_EMPTY_MESSAGE               = '50046'
    NO_PENDING_APPLICATION_FOR_THIS_USER  = '150003'
    INVALID_MESSAGE_TYPE                  = '50018'
    INVALID_MESSAGE_CONTENT               = '40004'
    CANNOT_DELETE_MESSAGE_BY_ANOTHER_USER = '50016'
    MAX_MESSAGE_PINS_ON_THAT_CHANNEL      = '30007'
    MUTED_BY_SERVER                       = '340013'
    DISABLED_DMS                          = 'Cannot send messages to this user'
    CANNOT_DM_THIS_USER                   = '40005'
    UNKNOWN_USER                          = '10004'
    UNKNOWN_MEMBER                        = '10006'
    USER_NOT_FOUND                        = '50031'
    INVALID_RECIPIENT                     = '40033'
    CANT_SELF_FRIEND                      = '80003'
    MAXIMUM_NUMBER_OF_FRIENDS_REACHED     = '30003'
    UNKNOWN_EMOJI                         = '10014'
    MAX_REACTIONS_ON_MESSAGE              = '30010'
    REACTION_WAS_BLOCKED                  = '40060'
    INVALID_FILE_UPLOADED                 = '50045'
    INVALID_STICKER                       = '50033'
    EMBED_DISABLED                        = '40006'
    INVALID_WEBHOOK_TOKEN                 = '40034'
    ONBOARDING_NOT_NEEDED                 = 'Onboarding responses are not valid'
    TOKEN_COMPROMISED                     = '40012'
    QUARANTINED_ACCOUNT                   = '40066'
    SPAMMER_ACCOUNT                       = '40067'
    PHONE_VERIFICATION_REQUIRED           = '40032'
    EMAIL_VERIFICATION_REQUIRED           = 'email_verification_required'

    def cleaninvite(invite):
        invite = invite.strip()
        m = re.search(r'discord(?:app)?\.(?:gg|com)/(?:invite/)?([a-zA-Z0-9\-_]+)', invite, re.IGNORECASE)
        if m:
            return m.group(1)
        return invite.split('/')[-1]

    def sleep(tosleep):
        time.sleep(tosleep)

    def getid(token):
        period = token.find('.')
        if period != -1:
            cut = token[:period]
        return base64.b64decode(cut + '==').decode()

    def getnonce():
        discord_epoch = 1420070400000
        timestamp = int(time.time() * 1000)
        nonce = (timestamp - discord_epoch) << 22
        return str(nonce)

    def makepings(ids, amt):
        if amt == 0:
            return ''
        shuffled = ids[:]
        random.shuffle(shuffled)
        selected = shuffled[:min(amt, len(shuffled))]
        return ' '.join(f'<@{userid}>' for userid in selected)

    def getemoji(length):
        emoji_ranges = [
            (0x1F600, 0x1F64F),
            (0x1F300, 0x1F5FF),
            (0x1F680, 0x1F6FF),
            (0x1F700, 0x1F77F),
            (0x1F900, 0x1F9FF),
        ]
        emojis = [chr(code) for start, end in emoji_ranges for code in range(start, end + 1)]
        return ''.join(random.choices(emojis, k=length))

    def getstring(length):
        return ''.join(random.choices(string.digits, k=length))

    def parsechannellink(link):
        match = re.search(r'channels/(\d+)/(\d+)', link or '')
        if not match:
            return '', ''
        return match.group(1), match.group(2)

    def parsemessagelink(link):
        match = re.search(r'channels/(\d+)/(\d+)/(\d+)', link or '')
        if not match:
            return '', '', ''
        return match.group(1), match.group(2), match.group(3)

    def errordatabase(text):
        db = {
            discord.INVALID_JSON:                         'Invalid JSON',
            discord.INVALID_JSON_2:                       'Invalid JSON',
            discord.INTERACTION_FAILED:                   'Interaction failed',
            discord.BANNED_TOKEN:                         'Banned token',
            discord.LOCKED_TOKEN:                         'Account locked',
            discord.DEAD_ACCOUNT:                         'Dead account',
            discord.LOCKED_ACCOUNT:                       'Locked account',
            discord.UNKNOWN_ACCOUNT:                      'Unknown account',
            discord.LIMITED:                              'Limited',
            discord.RETRY_AFTER_LIMITED:                  'Limited',
            discord.API_BAN:                              'API BAN',
            discord.OPENING_DMS_TOO_FAST:                 'Opening DMS too fast',
            discord.CLOUDFLARE:                           'Cloudflare',
            discord.HCAPTCHA:                             'Hcaptcha',
            discord.AUTOMOD_FLAGGED:                      'Automod flagged',
            discord.MESSAGE_BLOCKED_BY_CONTENT_FILTER:    'Message blocked by content filter',
            discord.NO_ACCESS_NOT_INSIDE:                 'No access',
            discord.MISSING_PERMISSIONS:                  'Missing permissions',
            discord.ACTION_NOT_ALLOWED:                   'Action not allowed',
            discord.VERIFICATION_TOO_HIGH:                'Verification too high',
            discord.INVALID_SERVER:                       'Invalid server',
            discord.UNKNOWN_SERVER:                       'Unknown server',
            discord.NOT_IN_SERVER:                        'Not in server',
            discord.SERVER_LIMITED_VIOLATED_TOS:          'Server limited',
            discord.MAX_SERVERS:                          'Max servers',
            discord.ALREADY_A_MEMBER:                     'Already a member',
            discord.UNKNOWN_INVITE:                       'Unknown invite',
            discord.INVALID_INVITE:                       'Invalid invite',
            discord.EXPIRED_INVITE:                       'Expired invite',
            discord.CHANNEL_NOT_FOUND:                    'Channel not found',
            discord.UNKNOWN_CHANNEL:                      'Unknown channel',
            discord.CANT_DO_THAT_ON_THIS_CHANNEL:         'Cant do that on this channel',
            discord.CANNOT_EXECUTE_ACTION:                'Cannot execute action',
            discord.NOT_IN_A_VC:                          'Not in a VC',
            discord.UNABLE_TO_SEND:                       'Unable to send',
            discord.UNKNOWN_MESSAGE:                      'Unknown message',
            discord.CANT_SEND_EMPTY_MESSAGE:              'Cant send empty message',
            discord.NO_PENDING_APPLICATION_FOR_THIS_USER: 'No pending application for this user',
            discord.INVALID_MESSAGE_TYPE:                 'Invalid message type',
            discord.INVALID_MESSAGE_CONTENT:              'Invalid message content',
            discord.CANNOT_DELETE_MESSAGE_BY_ANOTHER_USER:'Cannot delete message authored by another user',
            discord.MAX_MESSAGE_PINS_ON_THAT_CHANNEL:     'Max message pins on that channel',
            discord.MUTED_BY_SERVER:                      'Muted by server',
            discord.DISABLED_DMS:                         'Disabled DMS',
            discord.CANNOT_DM_THIS_USER:                  'Cannot DM this user',
            discord.UNKNOWN_USER:                         'Unknown user',
            discord.UNKNOWN_MEMBER:                       'Unknown member',
            discord.USER_NOT_FOUND:                       'User not found',
            discord.INVALID_RECIPIENT:                    'Invalid recipient',
            discord.CANT_SELF_FRIEND:                     'Cant self friend',
            discord.MAXIMUM_NUMBER_OF_FRIENDS_REACHED:    'Maximum number of friends reached',
            discord.UNKNOWN_EMOJI:                        'Unknown emoji',
            discord.MAX_REACTIONS_ON_MESSAGE:             'Max reactions on message',
            discord.REACTION_WAS_BLOCKED:                 'Reaction was blocked',
            discord.INVALID_FILE_UPLOADED:                'Invalid file uploaded',
            discord.INVALID_STICKER:                      'Invalid sticker',
            discord.EMBED_DISABLED:                       'Embed disabled',
            discord.ONBOARDING_NOT_NEEDED:                'No need to bypass onboarding',
            discord.TOKEN_COMPROMISED:                    'Token compromised',
            discord.QUARANTINED_ACCOUNT:                  'Account quarantined',
            discord.SPAMMER_ACCOUNT:                      'Account flagged as spammer',
            discord.PHONE_VERIFICATION_REQUIRED:          'Phone verification required',
            discord.EMAIL_VERIFICATION_REQUIRED:          'Email verification required',
        }

        for key, message in db.items():
            if key in text:
                return message, key

        if isinstance(text, str):
            try:
                text = json.loads(text)
            except Exception:
                return text, None

        if isinstance(text, dict) and 'message' in text:
            return text['message'], None

        return text, None
