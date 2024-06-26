from dotenv import load_dotenv
import os

load_dotenv()

ELASTICSEARCH_HOST = os.getenv('ELASTICSEARCH_HOST')
ELASTICSEARCH_PORT = os.getenv('ELASTICSEARCH_PORT')
