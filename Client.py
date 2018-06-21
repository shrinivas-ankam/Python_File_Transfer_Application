import pymongo
import socket
import base64

def getAndUploadFile(sock,collection):
    filename = input("Enter filename: ")
    if filename != "quit":
        sock.send(filename.encode('utf-8'))
        data = sock.recv(1024)
        message = data.decode('utf_8')
        if message[:6] == "EXISTS":
            filesize = (message[6:])
            f = open('backup_' + filename, 'wb')
            data = sock.recv(1024)
            totalRecv = len(data)
            f.write(data)
            while int(totalRecv) < int(filesize):
                data = sock.recv(1024)
                totalRecv += 1024
                f.write(data)
            print("Completed creating backup.")

            with open('backup_' + filename, "rb") as newFile:
                str = base64.b64encode(newFile.read())

            collection.insert({"filename": filename, "file": str, "description": "test"})
            print("Completed uploading into database.")
        else:
            print("File doesn't exists, try again...")
        return 0
    print("Exiting...")
    return -1


def Main():
    host = '127.0.0.1'
    port = 1000
    uri="mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(uri)
    database = client['shrini']              # this is database name
    collection = database['file_database']   # this is table name

    while True:
        s = socket.socket()
        s.connect((host, port))
        errorReturn=getAndUploadFile(s,collection)
        s.close()
        if errorReturn== -1:
            break

    print("Going to Read the database")
    files = collection.find({})
    for file in files:
        print(file)

if __name__ == '__main__':
    Main()
