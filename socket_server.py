import socket
from http.server import HTTPServer, CGIHTTPRequestHandler, BaseHTTPRequestHandler
import asyncore
import socketserver
import threading



def parse_data(Dat_As):
    if(Dat_As[0]==':'):
        n=0
        for i in  range (10):
            if(Dat_As[i]==','):
                n=i
                ADRES=Dat_As[1:i]
                print (ADRES)
                break
        for i in range (n+1, n+10):
            if(Dat_As[i]==';'):
                Parameter=Dat_As[n+1:i]
                print(Parameter)
                break







class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print(data)
            parse_data(data.decode("utf-8"))










class EchoServer(asyncore.dispatcher, BaseHTTPRequestHandler):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(50)

    def handle_accept(self):
        print("I'm Taking")
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print ('Incoming connection from %s' % repr(addr))
            handler = EchoHandler(sock)




class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    pass



#если есть подключение то, включаем сервер

web_server = ThreadingHTTPServer(('',9067),CGIHTTPRequestHandler)
server = EchoServer('', 8000)
def Main():
    thre1 = threading.Thread(target=web_server.serve_forever)
    print("start")
    thre2 = threading.Thread(target=asyncore.loop)
    print("start 2")

    thre2.start()
    thre1.start()


if __name__ == '__main__':

    thre1=threading.Thread(target = web_server.serve_forever)
    print("start")
    thre2 = threading.Thread(target = asyncore.loop)
    print("start 2")

    thre2.start()
    thre1.start()










