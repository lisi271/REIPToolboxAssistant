import os
import sqlite3
import win32crypt
import glob

BROWSER_PATHS = {
    "chrome": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies"),
    "edge": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies"),
    "brave": os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Cookies"),
}

TOOLBOX_DOMAIN = ".3cis.net"


def decrypt_cookie(enc_value):
    try:
        return win32crypt.CryptUnprotectData(enc_value, None, None, None, 0)[1].decode()
    except:
        return None


def get_toolbox_cookie():
    for name, cookie_path in BROWSER_PATHS.items():
        if not os.path.exists(cookie_path):
            continue

        try:
            conn = sqlite3.connect(cookie_path)
            cursor = conn.cursor()

            cursor.execute(
                "SELECT name, encrypted_value FROM cookies WHERE host_key LIKE ?",
                (f"%{TOOLBOX_DOMAIN}%",)
            )

            for cookie_name, encrypted_value in cursor.fetchall():
                val = decrypt_cookie(encrypted_value)
                if val:
                    return cookie_name, val

        except Exception as e:
            continue

    return None, None
