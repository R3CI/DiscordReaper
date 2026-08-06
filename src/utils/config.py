from src import *

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.default_flow_style = False


class configcls:
    file      = os.path.join(APPDATA, 'config.yaml')
    inst      = None
    initlock  = threadinglib.Lock()
    iolock    = threadinglib.Lock()

    defaults = {
        'general': {
            'concurrency': (8,    'How many worker threads run in parallel'),
            'delay_min':   (1.0,  'Minimum seconds between actions per thread'),
            'delay_max':   (3.0,  'Maximum seconds between actions per thread'),
        },
        'proxies': {
            'enabled': (False, 'Route requests through proxies  format: user:pass@host:port'),
            'timeout': (15,    'Request timeout in seconds'),
        },
        'retry': {
            'count': (3,   'How many times to retry a token on exception before giving up'),
            'delay': (1.0, 'Seconds to wait between retry attempts'),
        },
        'debug': {
            'enabled': (False, 'Print extra diagnostic output'),
        },
    }

    def __new__(cls):
        if cls.inst is None:
            with cls.initlock:
                if cls.inst is None:
                    cls.inst = super().__new__(cls)

        return cls.inst


    def __init__(self):
        if not hasattr(self, 'ready'):
            with configcls.initlock:
                if not hasattr(self, 'ready'):
                    self.data = CommentedMap()
                    self.load()
                    self.ready = True


    def load(self):
        existing = {}

        if os.path.exists(self.file):
            try:
                with open(self.file, 'r', encoding='utf-8') as f:
                    raw = yaml.load(f)

                if isinstance(raw, dict):
                    for section, values in raw.items():
                        if isinstance(values, dict):
                            existing[section] = dict(values)

            except Exception:
                pass

        self.rebuild(existing)
        self.save()


    def rebuild(self, existing):
        self.data = CommentedMap()

        for idx, (section, keys) in enumerate(self.defaults.items()):
            self.data[section] = CommentedMap()

            if idx > 0:
                self.data.yaml_set_comment_before_after_key(section, before='\n')

            for k, spec in keys.items():
                if not isinstance(spec, tuple):
                    continue

                default, comment = spec
                prev = existing.get(section, {}).get(k)
                self.data[section][k] = self.cast(prev, default) if prev is not None else default
                self.data[section].yaml_add_eol_comment(comment, k)


    def cast(self, value, default):
        if value is None:
            return default

        try:
            t = type(default)

            if t is bool:
                if isinstance(value, bool):
                    return value

                return str(value).lower() in ('true', '1', 'yes', 'on')

            if t is int:
                return int(value)

            if t is float:
                return float(value)

            if t is str:
                return str(value)

            if t is list:
                return value if isinstance(value, list) else default

            return value

        except Exception:
            return default


    def get(self, section, key, fallback=None):
        return self.data.get(section, {}).get(key, fallback)


    def set(self, section, key, value):
        with configcls.iolock:
            if section in self.data:
                self.data[section][key] = self.cast(value, self.data[section].get(key))
                self.savelocked()


    def save(self):
        with configcls.iolock:
            self.savelocked()


    def savelocked(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)

        with open(self.file, 'w', encoding='utf-8') as f:
            yaml.dump(self.data, f)


class get:
    class general:
        @staticmethod
        def concurrency():
            return configcls().get('general', 'concurrency', 8)


        @staticmethod
        def delaymin():
            return configcls().get('general', 'delay_min', 1.0)


        @staticmethod
        def delaymax():
            return configcls().get('general', 'delay_max', 3.0)


    class proxies:
        @staticmethod
        def enabled():
            return configcls().get('proxies', 'enabled', False)


        @staticmethod
        def timeout():
            return configcls().get('proxies', 'timeout', 15)


    class retry:
        @staticmethod
        def count():
            return configcls().get('retry', 'count', 3)

        @staticmethod
        def delay():
            return configcls().get('retry', 'delay', 1.0)


    class debug:
        @staticmethod
        def enabled():
            return configcls().get('debug', 'enabled', False)
