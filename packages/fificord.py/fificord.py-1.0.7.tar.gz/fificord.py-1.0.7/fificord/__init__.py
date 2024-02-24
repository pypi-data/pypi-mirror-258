# __init__.py
import tls_client
from .ext import commands

class Status:
    Idle = "idle"
    Dnd = "dnd"
    Invisible = "invisible"
    Online = "online"
    Mobile = "mobile"
    Vr = "vr"

session = tls_client.Session()