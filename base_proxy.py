import datetime
import logging
import socket
import sys
from _thread import start_new_thread


LISTENING_PORT = 8001
MAX_CONNECTIONS = 5
BUFFER_SIZE = 8192


def start():
    try:
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object.bind(("", LISTENING_PORT))
        socket_object.listen(MAX_CONNECTIONS)
        print("[*] Initializing sockets ... done")
        print("[*] Socket binded successfully ...")
        print("[*] Server started successfully [%d]\n" % LISTENING_PORT)
    except Exception as e:
        print(f"Exception: {e}")
        print("[*] Unable to initialize socket")
        sys.exit(2)

    while True:
        try:
            connection, connection_address = socket_object.accept()
            connection_data = connection.recv(BUFFER_SIZE)
            start_new_thread(
                connection_string, (connection, connection_data, connection_address)
            )
        except KeyboardInterrupt:
            socket_object.close()
            print("\n[*] Proxy server shutting down ...")
            print("Proxy server has been shut down")
            sys.exit(1)


def connection_string(connection, request_data, connection_address):
    """
    Function to process incoming requests

    Args:
        connection: Connection Stream
        request_data: Clients data from browser request
        connection_address: Address from the connection

    """

    try:
        first_line = request_data.split("\n")[0]
        url = first_line.split(" ")[1]
        http_position = url.find("://")
        if http_position == 1:
            temp = url
        else:
            temp = url[(http_position + 3):]

        port_position = temp.find(":")
        webserver_position = temp.find("/")

        if webserver_position == 1:
            webserver_position = len(temp)

        if port_position == 1 or webserver_position < port_position:
            port = 80
            webserver = temp[:port_position]
        else:
            port = int(
                temp[(port_position + 1):][:webserver_position - port_position - 1]
            )
            webserver = temp[:port_position]

        proxy_server(
            webserver=webserver, webserver_port=port, connection=connection,
            request_data=request_data, connection_address=connection_address
        )

    except Exception as e:
        pass


def proxy_server(
        webserver, webserver_port, connection, request_data, connection_address
):
    """
    Function handling connection proxying

    Args:
        webserver: Host address
        webserver_port: Webserver port
        connection: Connection Stream
        request_data: Clients data from browser request
        connection_address: Address from the connection

    Returns:
        Response from a server request to is made
    """

    try:
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object.connect((webserver, webserver_port))
        socket_object.send(data=request_data)

        while True:
            response = socket_object.recv(BUFFER_SIZE)

            if response:
                connection.send(response)
                response_size = "%.3s KB" % str(float(len(response) / 1024))
                response_data = (
                    datetime.datetime.now(), str(connection_address[0]), response_size
                )
                message = "%s [*] %s OK => %s <=" % response_data
                print(message)
                logging.info(message)

            else:
                break
            socket_object.close()
            connection.close()

    except socket.error as e:
        response_data = (datetime.datetime.now(), str(connection_address[0]), e)
        message = "%s [*] %s ERROR => %s" % response_data
        print(message)
        logging.error(message)
        connection.close()
        sys.exit(1)

    socket_object.close()


start()
