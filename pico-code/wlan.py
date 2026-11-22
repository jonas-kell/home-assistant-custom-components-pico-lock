import rp2
import utime as time
from environment import getEnvValue
import network

# Config Parameters

wlanSSID = getEnvValue("ssid")
wlanPW = getEnvValue("password")
rp2.country("DE")

wlan = network.WLAN(network.STA_IF)


def wlanConnect(initial=False):
    print(f"Trying to connect to ssid: {wlanSSID}")
    if initial:
        print(f"Connecting with password: {wlanPW}")
    else:
        print("Omitting password from log: ********")

    wlan.active(True)

    while not wlan.isconnected():
        print("Connecting to WLAN-Network")
        wlan.active(True)

        # Disconnect if possibly old connection
        try:
            wlan.disconnect()
        except:
            pass

        wlan.connect(wlanSSID, wlanPW)
        for i in range(10):  # wait at most 10 seconds for wifi chip to connect
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            print(".")
            time.sleep(1)

        if not wlan.isconnected():
            print(
                "No WLAN-Network Connected. Have you set the correct configurational parameters in the .env?"
            )
            print("WLAN-Status:", wlan.status())
            print()

    print("Successfully connected to WLAN-Network")
    netConfig = wlan.ifconfig()
    print("IPv4-Address:", netConfig[0])
    print()
    return netConfig[0]


def wlanIsConnected():
    return wlan.isconnected()
