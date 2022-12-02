import socket
import sys 
import os

# -- DEFINE CONSTANTS -- #
END_INTERACTION = "close"
CONTINUE_INTERACTION = "keep-alive"
OK = 200
REDIRECT = 301
ERROR = 404
# -- DEFINE CONSTANTS -- #


# -- DEBUGG PRINTS -- #
def pretty_print_folder(dirpath, dirnames, filenames):
    print(
    f"Root: {dirpath}\n"
    f"Sub-directories: {dirnames}\n"
    f"Files: {filenames}\n"
)
def prettty_print_data(data, file, con_stat):
    print('Originaly recieved: ', data)
    print('Extracted Filename: ', file)
    print('Connections Status: ', con_stat)
# -- DEBUGG PRINTS -- #


def valid_port(port):
    return True

def phrase_data(data):
    empty_req = "GET / HTTP/1.1"

    connection_string = data.split("\n")[2]
    connection_status = connection_string.split(" ")[1]

    req = data.split("\r\n", 1)[0]
    if(req == empty_req):
        file = "/index.html"
    else:    
        splitted_req = req.split(" ")
        file = splitted_req[1].split(" ")[0]

    return file, connection_status

def redirect(file, client_socket, client_address):
    return REDIRECT

"""
    Returns True if the file is inside the current Directory.
    If not, returns False.
"""
def is_exist(file):
    current_dir = os.getcwd() + "/files"
    path = current_dir + file
    return os.path.exists(path) 

def get_content(file):
    pass

def build_req(content, is_exist):
    pass

def get_full_path(file):
    current_dir = os.getcwd() + "/files"
    path = current_dir + file
    return path


def handle(file, client_socket, client_address):
    if file == "redirect":
        return redirect(file, client_socket, client_address)
    if is_exist(file):
        file_path = get_full_path(file)
        print(file_path)
        #content = get_content(file)
        #client_socket.send(build_req(content, True))
        return OK
    else:
        print(f'file "{file}" does not exist')
        #content = ''
        #client_socket.send(build_req(content,False))
        return ERROR    

def main():

    # Get port and validate it
    port = int(sys.argv[1])
    if not valid_port(port):
        print("Not a valid port")
        exit()

    # Set up server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(5)


    while True:

        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)

        data = bytes.decode(client_socket.recv(100))
        print(data)

        file, con_stat = phrase_data(data)

        # req_stat can be 200, 301 or 404
        req_stat = handle(file, client_socket, client_address)
        if req_stat == REDIRECT or req_stat == ERROR:
            client_socket.close()
            print('Client disconnected')
        else:
            if con_stat == END_INTERACTION:
                client_socket.close()
                print('Client disconnected')

        #client_socket.send(data.upper())



if __name__ == "__main__":
    main()