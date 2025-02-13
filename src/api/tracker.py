import os

from dotenv import load_dotenv
from yandex_tracker_client import TrackerClient

load_dotenv(".env")

client = TrackerClient(token=os.getenv("OAUTH_TOKEN"), org_id=os.getenv("ORG_ID"))
