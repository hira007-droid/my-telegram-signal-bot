# check_setup.py
# ------------------------------------------------------------------
# A helper that CHECKS everything and tells you, in plain words,
# what is fine and what to fix. Run it by double-clicking
# 2_check.bat. It changes nothing except: if config.py does not
# exist yet, it creates one for you.
# ------------------------------------------------------------------
import asyncio
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
problems = []


def ok(text):
    print("  [ OK ]       " + text)


def note(text):
    print("  [ NOTE ]     " + text)


def bad(text, todo):
    problems.append(text)
    print("  [ PROBLEM ]  " + text)
    print("               WHAT TO DO: " + todo)


CONFIG_TEMPLATE = '''# config.py - your PRIVATE settings. Never share this file with anyone.

# 1) Paste your token from BotFather between the quotation marks:
BOT_TOKEN = "PASTE_YOUR_TOKEN_HERE"

# 2) Your Telegram ID. Leave 0 for now. The bot will tell you the number to put here.
ALLOWED_USER_ID = 0

# 3) Paste your free API key from twelvedata.com (Dashboard -> API Keys):
TWELVE_DATA_KEY = "PASTE_YOUR_TWELVEDATA_KEY_HERE"
'''

print()
print("=== Checking your Signal Bot setup ===")
print()

# ---- 1. Python version ----
if sys.version_info >= (3, 9):
    ok("Python %d.%d.%d is installed." % sys.version_info[:3])
else:
    bad("Your Python is too old (%d.%d)." % sys.version_info[:2],
        "Install the newest Python from python.org (tick 'Add python.exe to PATH').")

# ---- 2. The program files ----
for name in ("bot.py", "texts.py", "db.py", "timing.py", "pairs.py", "data.py"):
    if os.path.exists(os.path.join(HERE, name)):
        ok("Found file " + name)
    else:
        bad("The file " + name + " is missing from this folder.",
            "Download it again and put it in the same folder as this file: " + HERE)

# ---- 3. config.py (create it if missing) ----
config_path = os.path.join(HERE, "config.py")
if not os.path.exists(config_path):
    with open(config_path, "w", encoding="utf-8") as f:
        f.write(CONFIG_TEMPLATE)
    note("config.py did not exist, so I created it for you.")

# ---- 4. The Telegram library ----
telegram_ok = False
try:
    import telegram
    ok("Telegram library is installed (version %s)." % telegram.__version__)
    telegram_ok = True
except ImportError:
    bad("The Telegram library is not installed yet.",
        "Double-click 1_install.bat, wait until it says Finished, then run this check again.")

# ---- 5b. The "requests" library (used to fetch live prices) ----
try:
    import requests
    ok("The 'requests' library (for live prices) is installed.")
except ImportError:
    bad("The 'requests' library is not installed yet.",
        "Double-click 1_install.bat, wait until it says Finished, then run this check again.")

# ---- 5. Paris time data ----
try:
    from zoneinfo import ZoneInfo
    ZoneInfo("Europe/Paris")
    ok("Paris time data is available.")
except Exception:
    bad("Paris time data is missing (Windows needs an extra package).",
        "Double-click 1_install.bat, wait until it says Finished, then run this check again.")

# ---- 6. Your settings in config.py ----
token = ""
owner = None
try:
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    token = str(getattr(config, "BOT_TOKEN", "")).strip()
    owner = getattr(config, "ALLOWED_USER_ID", None)
except Exception as error:
    bad("config.py has a typing mistake: %s" % error,
        "Open config.py with Notepad. It must have exactly two lines like this:\n"
        '                 BOT_TOKEN = "123456789:ABCdef..."\n'
        "                 ALLOWED_USER_ID = 0\n"
        "               Keep the quotation marks around the token, and none around the number.")
    token = None

token_looks_ok = False
if token is not None:
    if token == "" or token == "PASTE_YOUR_TOKEN_HERE":
        bad("You have not pasted your bot token into config.py yet.",
            "Right-click config.py > Open with > Notepad. Replace PASTE_YOUR_TOKEN_HERE with the "
            "token from BotFather (keep the quotation marks). Press Ctrl+S to save.")
    elif not re.fullmatch(r"\d{6,}:[A-Za-z0-9_-]{30,}", token):
        bad("The token in config.py does not look right.",
            "A token looks like 123456789:ABCdefGhIJK... with no spaces. Copy it again from "
            "BotFather (send /mybots, choose your bot, press API Token).")
    else:
        ok("The token in config.py looks correct.")
        token_looks_ok = True

    if isinstance(owner, int) and owner > 0:
        ok("Your Telegram ID is set (%d). Only you can use the bot." % owner)
    else:
        note("Your Telegram ID is not set yet (ALLOWED_USER_ID = 0). This is normal the first "
             "time. The bot will tell you the number when you send it /start.")

    twelve_key = str(getattr(config, "TWELVE_DATA_KEY", "")).strip()
    if twelve_key in ("", "PASTE_YOUR_TWELVEDATA_KEY_HERE"):
        bad("You have not pasted your Twelve Data key into config.py yet.",
            "Register free at twelvedata.com (no card needed), go to Dashboard > API Keys, "
            "copy the key, and paste it into config.py in place of "
            "PASTE_YOUR_TWELVEDATA_KEY_HERE. Keep the quotation marks.")
    else:
        ok("A Twelve Data key is present in config.py.")
        try:
            import data as data_module
            quote = data_module.fetch_quote("EUR/USD", twelve_key)
            ok("Twelve Data answered: EUR/USD = %s (measured %ss ago)."
               % (quote["price"], quote["latency_seconds"]))
        except Exception as error:
            bad("Could not get a live price from Twelve Data: %s" % error,
                "If it says the key was rejected, copy it again from the dashboard. If it "
                "mentions a limit, wait a minute and run this check again.")

# ---- 7. Can we save files in this folder? ----
try:
    test_file = os.path.join(HERE, "_write_test.tmp")
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
    ok("The bot can save its memory file in this folder.")
except Exception:
    bad("The bot cannot save files in this folder.",
        "Move the whole folder to C:\\signalbot (not inside Program Files or Downloads) and try again.")

# ---- 8. Does Telegram accept the token? (needs internet) ----
if telegram_ok and token_looks_ok:
    async def ask_telegram():
        bot = telegram.Bot(token)
        async with bot:
            return await bot.get_me()
    try:
        me = asyncio.run(ask_telegram())
        ok("Telegram accepted your token. Your bot is @%s" % me.username)
    except Exception as error:
        kind = type(error).__name__
        if kind in ("InvalidToken",):
            bad("Telegram says the token is wrong.",
                "Copy the token again from BotFather (/mybots > your bot > API Token) and paste "
                "it into config.py.")
        elif kind in ("NetworkError", "TimedOut", "ConnectError", "ConnectTimeout"):
            bad("I could not reach Telegram from this computer.",
                "Check your internet. If you use a VPN, firewall or antivirus, allow Python, "
                "then run this check again.")
        else:
            bad("Telegram check failed (%s: %s)." % (kind, error),
                "Run this check again. If it repeats, copy this whole window and send it to me.")

# ---- Summary ----
print()
if problems:
    print("RESULT: %d problem(s) found. Fix them from the TOP one down, then run this check again."
          % len(problems))
else:
    print("RESULT: Everything is fine. Now double-click 3_start_bot.bat")
print()
