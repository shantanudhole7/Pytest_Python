import os
from dotenv import load_dotenv
from configparser import ConfigParser
from pathlib import Path

load_dotenv()

_INI_PATH = Path(__file__).with_name("config.ini")
_ini = ConfigParser(interpolation=None)  # no %-interpolation, so values are read exactly as written
if not _ini.read(_INI_PATH, encoding="utf-8"):
    raise FileNotFoundError(f"Config file not found: {_INI_PATH}")

# region BROWSER
HEADLESS=_ini.getboolean("browser", "headless")
SLOWMO=_ini.getint("browser", "slow_mo")
# endregion BROWSER

# region URLS
BASEURL = _ini.get("url", "base_url")
INVENTORYPATH = _ini.get("url", "inventory_path")
PRACTICEURL = _ini.get("url", "practice_url")
POPUPSPATH = _ini.get("url", "popups_path")
WINDOWOPERATIONSPATH = _ini.get("url", "window_operations_path")
IFRAMEPATH = _ini.get("url", "iframe_path")
WEBFORMURL = _ini.get("url", "web_form_url")
# endregion URLS

# region API URLS
APIBASEURL = _ini.get("api", "base_url")
# endregion API URLS

# region Credentials
APPUSERNAME = _ini.get("credentials", "app_username")
LOCKEDUSERNAME = _ini.get("credentials", "locked_username")
PASSWORD = _ini.get("credentials", "password")
WRONGPASSWORD = _ini.get("credentials", "wrong_password")
# endregion Credentials

# region API Credentials
APIUSEREMAIL = os.getenv("APIUSEREMAIL")
APIUSERPASSWORD = os.getenv("APIUSERPASSWORD")
# endregion API Credentials

# region Error Alerts
LOGINERROR = _ini.get("messages", "login_error")
LOCKEDUSERERROR = _ini.get("messages", "locked_user_error")
# endregion Errors

# region Page Titles
HOMEPAGEHEADING = _ini.get("messages", "home_page_heading")
# endregion Page Titles

# region API Message
APILOGINSUCCESSMESSAGE = _ini.get("messages", "api_login_success")
APIORDERPLACEDMESSAGE = _ini.get("messages", "api_order_placed")
APIPRODUCTADDEDMESSAGE = _ini.get("messages", "api_product_added")
APIPRODUCTDELETEMESSAGE = _ini.get("messages", "api_product_deleted")
# endregion API Message

# region Email
EMAILENABLED = _ini.getboolean("email", "enabled")
SMTPHOST = _ini.get("email", "smtp_host")
SMTPPORT = _ini.getint("email", "smtp_port")
SMTPUSER = os.getenv("SMTPUSER")
SMTPPASSWORD = os.getenv("SMTPPASSWORD")
EMAILFROM = os.getenv("EMAILFROM")
EMAILTO = os.getenv("EMAILTO")
# endregion Email

# region Report
REPORTLOGO = _ini.get("report", "logo", fallback="")
REPORTTABTITLE = _ini.get("report", "tab_title", fallback="")
# endregion Report
