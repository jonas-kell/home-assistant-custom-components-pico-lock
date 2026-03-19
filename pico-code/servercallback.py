from lock import triggerUnlock
from led import blink
from server import parseUrl
from signing import generate_nonce, verify
from environment import getEnvValue

BLINK = True  # SET TO True FOR DEBUG

nonce = None


def callback(method, url):
    global nonce

    url, params = parseUrl(url)

    blink(1, BLINK)  # show that communication happened

    if method == "GET":
        if url == "/check_connect":
            return '{"status": "success"} \n'
        if url == "/get_nonce":
            nonce = generate_nonce()
            return f'{{"status": "success", "nonce": "{nonce}"}} \n'

    if method == "POST":
        if url == "/open":
            if nonce is not None:
                signature = params.get("signature")
                if signature is not None:

                    if verify(nonce, signature, getEnvValue("secret")):
                        # trigger the action
                        triggerUnlock()
                        nonce = None
                        return '{"status": "success"} \n'

                    return '{"status": "wrong signature"} \n'

                return '{"status": "unsigned"} \n'

            return '{"status": "uninitialized"} \n'

    return '{"status": "forbidden"} \n'
