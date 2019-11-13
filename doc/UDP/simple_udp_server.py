import socket
import time


def main():
    host = '127.0.0.1'
    port = 2001

    clients = {}

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.setblocking(0)
    shutdown = False
    password = "2517ShutdownServer"
    print("Server starter")

    def regclient(regdata, regaddr):

        clients[regaddr] = regdata.split(' ')[1]
        print((clients[regaddr] + " connected"))
        for regcl in clients:
            s.sendto(str(clients[regaddr] + " connected").encode(), regcl)

    def delclient(deladdr):

        print(clients[deladdr] + " quited")
        for delcl in clients:
            s.sendto(str(clients[deladdr] + " quited").encode(), delcl)
        del clients[deladdr]

    while not shutdown:
        try:
            data, addr = s.recvfrom(1024)
            data = data.decode()

            if str(data) == password:
                shutdown = True
            elif addr not in clients and data.split(' ')[0] == "connect":
                regclient(data, addr)
            elif addr in clients and data == "q":
                delclient(addr)
            elif data != 'q':
                print(time.ctime(time.time())+str(addr)+" "+str(clients[addr])+": :"+str(data))
                for client in clients:
                    if client != addr:
                        s.sendto(str(clients[addr]+' : '+data).encode(), client) #sendto(msg, ipAddress)

        except socket.error:
            pass
    s.close()


if __name__ == "__main__":
main()
