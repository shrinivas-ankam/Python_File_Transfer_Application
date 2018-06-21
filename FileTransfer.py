import socket
import os

def sendFile(sock):
    filename = sock.recv(1024).decode('utf-8')
#   print("File Name is:" + filename)

    if (os.path.isfile(filename)):
#       print('File is present.')
        message = "EXISTS" + str(os.path.getsize(filename))
        sock.send(message.encode('utf-8'))

        with open(filename,'rb') as f:
#           print("Opened the file")
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
            while f.read(1):
                f.seek(-1,1)
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
            f.close()
#           print('Closed the file')
    else:
        message = "Error"
        sock.send(message.encode('utf-8'))
    sock.close()
    print("Returning from function")


def Main():
    host='127.0.0.1'
    port = 1000

    s = socket.socket()
    s.bind((host,port))
    s.listen(5)

    os.chdir("C:\Shrini\Python_Practice\Project2\Destination_path")
    print("Server is Listing")

    while True:
        print("Inside while loop")
        c, addr = s.accept()
        print("Client connected " + str(addr))
        sendFile(c)
        print("At end of while loop")
        
    s.close()

if __name__ == '__main__':
    Main()
