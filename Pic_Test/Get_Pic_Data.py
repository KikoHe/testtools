import json, pytz, hashlib, zipfile, os, requests, fitz
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry