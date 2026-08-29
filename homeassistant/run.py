import json
import os
import secrets
import shutil
import subprocess
from pathlib import Path


ROOT = Path("/opt/moneynut/app")
DATA = Path("/data")
DATABASE = DATA / "db.sqlite3"
SECRET_FILE = DATA / "django_secret_key"
IMPORT_DATABASE = Path("/share/moneynut-db.sqlite3")


def read_options():
    try:
        with (DATA / "options.json").open(encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)


DATA.mkdir(parents=True, exist_ok=True)

if not DATABASE.exists() and IMPORT_DATABASE.exists():
    print("Importing the existing MoneyNut database from /share/moneynut-db.sqlite3")
    shutil.copy2(IMPORT_DATABASE, DATABASE)

if not SECRET_FILE.exists():
    SECRET_FILE.write_text(secrets.token_urlsafe(64), encoding="utf-8")
    SECRET_FILE.chmod(0o600)

options = read_options()
os.environ.update(
    {
        "DATABASE_PATH": str(DATABASE),
        "DJANGO_SECRET_KEY": SECRET_FILE.read_text(encoding="utf-8").strip(),
        "DJANGO_DEBUG": "false",
        "DJANGO_TIME_ZONE": options.get("timezone", "America/Edmonton"),
        "DJANGO_ALLOWED_HOSTS": options.get("allowed_hosts", "home.moneynut.xyz"),
        "DJANGO_CSRF_TRUSTED_ORIGINS": options.get(
            "csrf_trusted_origins", "https://home.moneynut.xyz"
        ),
        "DJANGO_SECURE_COOKIES": str(options.get("secure_cookies", True)).lower(),
        "EMAIL_HOST_USER": options.get("email_host_user", ""),
        "EMAIL_HOST_PASSWORD": options.get("email_host_password", ""),
    }
)

run("python", "manage.py", "migrate", "--noinput")
run("python", "manage.py", "collectstatic", "--noinput")

os.execvp(
    "gunicorn",
    [
        "gunicorn",
        "budgetapp.wsgi:application",
        "--chdir",
        str(ROOT),
        "--bind",
        "0.0.0.0:8090",
        "--workers",
        "2",
        "--timeout",
        "120",
        "--access-logfile",
        "-",
        "--error-logfile",
        "-",
    ],
)
