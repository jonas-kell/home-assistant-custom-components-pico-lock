from lock import triggerUnlock
from led import blink
from server import parseUrl

BLINK = False  # SET TO True FOR DEBUG

def callback(method, url):
    global states

    url, params = parseUrl(url)

    blink(1, BLINK)  # show that communication happened

    if method == "GET":
        if url == "/check_connect":
            return '{"status": "success"} \n'

    if method == "POST":
        if url == "/open":            
            # trigger the action
            triggerUnlock()

            return '{"status": "success"} \n'

    return '{"status": "forbidden"} \n'