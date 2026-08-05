#!/usr/bin/env bash
set -euo pipefail

PASS=0
FAIL=0
WARN=0

green='\033[0;32m'
red='\033[0;31m'
yellow='\033[1;33m'
nc='\033[0m'

ok()   { echo -e "  ${green}[OK]${nc}   $*";   ((PASS++)) || true; }
fail() { echo -e "  ${red}[FAIL]${nc} $*"; ((FAIL++)) || true; }
warn() { echo -e "  ${yellow}[WARN]${nc} $*"; ((WARN++)) || true; }
skip() { echo -e "  [SKIP] $*"; }

echo ""
echo " DiscordReaper - Setup Check"
echo " ----------------------------"
echo ""

DISTRO=""
PKG_MANAGER=""
if command -v apt-get &>/dev/null; then
    PKG_MANAGER="apt-get"; DISTRO="debian"
elif command -v dnf &>/dev/null; then
    PKG_MANAGER="dnf"; DISTRO="fedora"
elif command -v pacman &>/dev/null; then
    PKG_MANAGER="pacman"; DISTRO="arch"
fi

echo "[1/8] Python..."
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PYVER=$("$cmd" --version 2>&1 | awk '{print $2}')
        PYMAJ=$(echo "$PYVER" | cut -d. -f1)
        PYMIN=$(echo "$PYVER" | cut -d. -f2)
        if [ "$PYMAJ" -ge 3 ] && [ "$PYMIN" -ge 8 ]; then
            ok "Python $PYVER ($cmd)"; PYTHON="$cmd"; break
        else
            fail "Python $PYVER too old, need 3.8+ ($cmd)"
        fi
    fi
done
if [ -z "$PYTHON" ]; then
    fail "Python 3.8+ not found."
    [ "$DISTRO" = "debian" ] && echo "  sudo apt-get install python3 python3-pip"
    [ "$DISTRO" = "fedora" ] && echo "  sudo dnf install python3 python3-pip"
    [ "$DISTRO" = "arch"   ] && echo "  sudo pacman -S python python-pip"
fi

echo "[2/8] pip..."
if [ -n "$PYTHON" ]; then
    if "$PYTHON" -m pip --version &>/dev/null 2>&1; then
        PIPVER=$("$PYTHON" -m pip --version | awk '{print $2}')
        ok "pip $PIPVER"
    else
        fail "pip not found."
        [ "$DISTRO" = "debian" ] && echo "  sudo apt-get install python3-pip"
        [ "$DISTRO" = "fedora" ] && echo "  sudo dnf install python3-pip"
        [ "$DISTRO" = "arch"   ] && echo "  sudo pacman -S python-pip"
    fi
else
    skip "pip (Python not found)"
fi

echo "[3/8] System packages (GTK/WebKit2GTK)..."
MISSING_SYS=()

if [ "$DISTRO" = "debian" ]; then
    for pkg in python3-gi gir1.2-gtk-3.0 libwebkit2gtk-4.0-dev; do
        if dpkg -l "$pkg" &>/dev/null 2>&1; then
            ok "$pkg"
        else
            fail "$pkg missing"
            MISSING_SYS+=("$pkg")
        fi
    done
    if ! dpkg -l "libwebkit2gtk-4.0-dev" &>/dev/null 2>&1 && ! dpkg -l "libwebkit2gtk-4.1-dev" &>/dev/null 2>&1; then
        warn "Neither webkit2gtk 4.0 nor 4.1 found."
        MISSING_SYS+=("libwebkit2gtk-4.1-dev")
    fi
elif [ "$DISTRO" = "fedora" ]; then
    for pkg in python3-gobject webkit2gtk4.0-devel gtk3-devel; do
        if rpm -q "$pkg" &>/dev/null 2>&1; then ok "$pkg"; else fail "$pkg missing"; MISSING_SYS+=("$pkg"); fi
    done
elif [ "$DISTRO" = "arch" ]; then
    for pkg in python-gobject webkit2gtk gtk3; do
        if pacman -Q "$pkg" &>/dev/null 2>&1; then ok "$pkg"; else fail "$pkg missing"; MISSING_SYS+=("$pkg"); fi
    done
else
    warn "Unknown distro — install GTK3 + WebKit2GTK manually."
fi

if [ ${#MISSING_SYS[@]} -gt 0 ]; then
    echo "  Installing missing packages..."
    if   [ "$DISTRO" = "debian" ]; then sudo apt-get install -y "${MISSING_SYS[@]}" && ok "Installed." || fail "apt-get failed."
    elif [ "$DISTRO" = "fedora" ]; then sudo dnf install -y "${MISSING_SYS[@]}" && ok "Installed." || fail "dnf failed."
    elif [ "$DISTRO" = "arch"   ]; then sudo pacman -S --noconfirm "${MISSING_SYS[@]}" && ok "Installed." || fail "pacman failed."
    fi
fi

echo "[4/8] Requirements..."
if [ -n "$PYTHON" ]; then
    if [ ! -f "requirements.txt" ]; then
        fail "requirements.txt not found — wrong folder?"
    else
        "$PYTHON" -m pip install -r requirements.txt --quiet && ok "All packages installed." || fail "pip install failed. Run: $PYTHON -m pip install -r requirements.txt"
    fi
else
    skip "requirements (Python not found)"
fi

echo "[5/8] Imports..."
if [ -n "$PYTHON" ]; then
    for mod in webview requests ruamel.yaml curl_cffi; do
        if "$PYTHON" -c "import $mod" &>/dev/null 2>&1; then
            ok "$mod"
        else
            fail "$mod  --  $PYTHON -m pip install $mod"
        fi
    done
    if "$PYTHON" -c "import gi" &>/dev/null 2>&1; then ok "gi (PyGObject)"; else fail "gi missing — install python3-gi"; fi
else
    skip "imports (Python not found)"
fi

echo "[6/8] Display..."
if [ -n "${DISPLAY:-}" ] || [ -n "${WAYLAND_DISPLAY:-}" ]; then
    ok "Display available"
else
    warn "No DISPLAY or WAYLAND_DISPLAY — GUI won't work without a desktop session."
fi

echo "[7/8] Files..."
MISSING_FILES=0
for f in main.py src/gui.py src/spread.py src/checker.py src/admincap.py src/evaluator.py src/rarechecker.py src/tokencapture.py src/__init__.py src/utils/discord.py src/utils/files.py src/utils/config.py src/utils/sessionmanager.py src/utils/logging.py src/utils/http.py; do
    [ ! -f "$f" ] && { fail "Missing: $f"; ((MISSING_FILES++)) || true; }
done
[ "$MISSING_FILES" -eq 0 ] && ok "All files present."

echo "[8/8] Project import..."
if [ -n "$PYTHON" ]; then
    if "$PYTHON" -c "from src import *; from src.utils.files import files; from src.gui import startgui" &>/dev/null 2>&1; then
        ok "OK"
    else
        fail "Import error. Run for details:"
        echo "  $PYTHON -c \"from src import *; from src.utils.files import files; from src.gui import startgui\""
    fi
else
    skip "import check (Python not found)"
fi

echo ""
echo " $PASS passed, $FAIL failed, $WARN warnings"
if [ "$FAIL" -eq 0 ]; then
    echo -e " ${green}Ready.${nc} Run: $PYTHON main.py"
else
    echo -e " ${red}Fix the errors above then run: $PYTHON main.py${nc}"
fi
echo ""
