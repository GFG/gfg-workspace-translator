import yaml

CONFIG_FILE = "app/config.yaml"

CONFIG = yaml.safe_load(open(CONFIG_FILE))

SUBSCRIPTION_ID = CONFIG['SUBSCRIPTION_ID']
SUBSCRIPTION_TYPE = CONFIG['SUBSCRIPTION_TYPE']

TOPIC_ID = CONFIG['TOPIC_ID']
EVENT_TYPES = CONFIG['EVENT_TYPES']

SCOPES = CONFIG['SCOPES']

SERVICE_ACCOUNT_FILE = CONFIG['SERVICE_ACCOUNT_FILE']
CLIENT_SECRETS_FILE = CONFIG['CLIENT_SECRETS_FILE']
TOKEN_FILE = CONFIG['TOKEN_FILE']

SUPPORTED_LANGUAGES = CONFIG['SUPPORTED_LANGUAGES']
DEFAULT = CONFIG['DEFAULT']

OPEN_MODELS = CONFIG['OPEN_MODELS']

CLOSE_MODELS = CONFIG['CLOSE_MODELS']
USING_MODEL = CONFIG['USING_MODEL']

from dotenv import load_dotenv
load_dotenv()