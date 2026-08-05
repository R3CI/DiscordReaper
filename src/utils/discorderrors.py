from src import *


class discorderrors:
    invalidjson                   = '50109'
    invalidjson2                  = '50035'
    interactionfailed             = '110000'
    bannedtoken                   = '40007'
    lockedtoken                   = '40002'
    deadaccount                   = '401'
    lockedaccount                 = 'You need to verify'
    unknownaccount                = '40001'
    limited                       = '20028'
    apiban                        = 'You are being blocked from accessing our API'
    openingdmstoofast             = '40003'
    cloudflare                    = 'Cloudflare'
    hcaptcha                      = 'captcha_key'
    automodflagged                = '200000'
    messageblockedbycontentfilter = '50022'
    noaccessnotinside             = '50001'
    missingpermissions            = '50013'
    actionnotallowed              = '50007'
    verificationtoohigh           = '50009'
    invalidserver                 = '50055'
    unknownserver                 = '10005'
    notinserver                   = 'Unknown Guild'
    serverlimitedviolatedtos      = '400002'
    maxservers                    = '30001'
    channelnotfound               = '50034'
    unknownchannel                = '10003'
    cantdothatontthischannel      = '50024'
    cannotexecuteaction           = '50003'
    notinavc                      = '50168'
    unabletosend                  = '50008'
    mutedbyserver                 = '340013'
    disableddms                   = 'Cannot send messages to this user'
    cannotdmthisuser              = '40005'
    unknownuser                   = '10004'
    unknownmember                 = '10006'
    usernotfound                  = '50031'
    invalidrecipient              = '40033'
    tokencompromised              = '40012'
    quarantinedaccount            = '40066'
    spammeraccount                = '40067'
    phoneverificationrequired     = '40032'


    @staticmethod
    def errordatabase(text):
        db = {
            discorderrors.invalidjson:                   'Invalid json',
            discorderrors.invalidjson2:                  'Invalid json',
            discorderrors.interactionfailed:             'Interaction failed',
            discorderrors.bannedtoken:                   'Token banned',
            discorderrors.lockedtoken:                   'Token locked',
            discorderrors.deadaccount:                   'Dead account',
            discorderrors.lockedaccount:                 'Account locked',
            discorderrors.unknownaccount:                'Unknown account',
            discorderrors.limited:                       'Limited',
            discorderrors.apiban:                        'API ban',
            discorderrors.openingdmstoofast:             'Opening dms too fast',
            discorderrors.cloudflare:                    'Cloudflare',
            discorderrors.hcaptcha:                      'Captcha',
            discorderrors.automodflagged:                'Automod flagged',
            discorderrors.messageblockedbycontentfilter: 'Message blocked by content filter',
            discorderrors.noaccessnotinside:             'No access',
            discorderrors.missingpermissions:            'Missing permissions',
            discorderrors.actionnotallowed:              'Action not allowed',
            discorderrors.verificationtoohigh:           'Verification too high',
            discorderrors.invalidserver:                 'Invalid server',
            discorderrors.unknownserver:                 'Unknown server',
            discorderrors.notinserver:                   'Not in server',
            discorderrors.serverlimitedviolatedtos:      'Server limited',
            discorderrors.maxservers:                    'Max servers',
            discorderrors.channelnotfound:               'Channel not found',
            discorderrors.unknownchannel:                'Unknown channel',
            discorderrors.cantdothatontthischannel:      'Cant do that on this channel',
            discorderrors.cannotexecuteaction:           'Cannot execute action',
            discorderrors.notinavc:                      'Not in a vc',
            discorderrors.unabletosend:                  'Unable to send',
            discorderrors.mutedbyserver:                 'Muted by server',
            discorderrors.disableddms:                   'Disabled dms',
            discorderrors.cannotdmthisuser:              'Cannot dm this user',
            discorderrors.unknownuser:                   'Unknown user',
            discorderrors.unknownmember:                 'Unknown member',
            discorderrors.usernotfound:                  'User not found',
            discorderrors.invalidrecipient:              'Invalid recipient',
            discorderrors.tokencompromised:              'Token compromised',
            discorderrors.quarantinedaccount:            'Account quarantined',
            discorderrors.spammeraccount:                'Account flagged as spammer',
            discorderrors.phoneverificationrequired:     'Phone verification required',
        }

        for key, message in db.items():
            if key in text:
                return message, key

        if isinstance(text, str):
            try:
                parsed = json.loads(text)
                if isinstance(parsed, dict) and 'message' in parsed:
                    return parsed['message'], None

            except Exception:
                return text, None

        if isinstance(text, dict) and 'message' in text:
            return text['message'], None

        return text, None


    @staticmethod
    def istokenfatal(etype):
        return etype in (
            discorderrors.bannedtoken,
            discorderrors.lockedtoken,
            discorderrors.lockedaccount,
            discorderrors.deadaccount,
            discorderrors.tokencompromised,
            discorderrors.quarantinedaccount,
            discorderrors.spammeraccount,
            discorderrors.phoneverificationrequired,
            discorderrors.apiban,
        )
