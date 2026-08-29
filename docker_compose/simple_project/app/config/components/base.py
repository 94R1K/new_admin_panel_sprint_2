BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
