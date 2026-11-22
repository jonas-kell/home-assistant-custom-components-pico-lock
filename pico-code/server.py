import socket
from wlan import wlanConnect, wlanIsConnected


# url_callback: provided function, that takes the following inputs:
#     the method of the request
#     the url of the request
#
#     and that returns the result-string to be echoed back to the client
def startServer(ipv4, url_callback):
    keyboardInterrupt = False
    while not keyboardInterrupt:

        # HTTP-Server starten
        print("Start Server")
        addr = socket.getaddrinfo(ipv4, 80)[0][-1]
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(addr)
        server.listen(1)
        server.settimeout(5)
        print("Server is listening to ", addr)
        print()

        # Auf eingehende Verbindungen hören
        while wlanIsConnected():
            try:
                conn, addr = server.accept()
                print("HTTP-Request recieved from Client", addr)
                request = conn.recv(1024)
                request = str(request)
                request = request.split()

                print(request)

                method = request[0].lstrip("'b")
                url = request[1].lstrip("'b")

                print("METHOD:", method)
                print("URL:", url)

                # Process by user defined function:
                resp = url_callback(method, url)

                conn.send(
                    "HTTP/1.0 200 OK\r\nContent-type: application/json; charset=utf-8\r\n\r\n"
                )
                conn.send(resp)
                conn.close()

                print("Sent HTTP-Response")
                print()
            except OSError as _e:
                # Timeout or connection lost
                if not wlanIsConnected():
                    print("WLAN Verbindung verloren")
                    break
            except KeyboardInterrupt:
                keyboardInterrupt = True
                server.close()
                break

        server.close()

        if not keyboardInterrupt:
            # Reconnect and restart server
            ipv4 = wlanConnect()


# //TODO more robust version that can decode urlencoded stuff.
# first returns the url_string, then the parameters as object
def parseUrl(url):
    parameters = {}
    url_string = url.split("?")[0] if "?" in url else url
    query_string = url.split("?")[1] if "?" in url else ""

    if query_string:
        pairs = query_string.split("&")
        for pair in pairs:
            key_value = pair.split("=")
            if len(key_value) == 2:
                key = key_value[0]
                value = key_value[1]
                parameters[key] = value

    return url_string, parameters
