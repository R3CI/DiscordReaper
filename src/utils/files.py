from src import *


class files:
    tokensfile  = os.path.join(APPDATA, 'tokens.txt')
    proxiesfile = os.path.join(APPDATA, 'proxies.txt')


    @staticmethod
    def check():
        os.makedirs(APPDATA, exist_ok=True)

        for f in (files.tokensfile, files.proxiesfile):
            if not os.path.exists(f):
                open(f, 'w', encoding='utf-8').close()


    @staticmethod
    def readlines(path):
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]

        except Exception:
            return []


    @staticmethod
    def writelines(path, lines):
        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))


    @staticmethod
    def loadtokens():
        return files.readlines(files.tokensfile)


    @staticmethod
    def loadproxies():
        return files.readlines(files.proxiesfile)
