from socket      import socket, AF_INET, SOCK_STREAM
from threading   import Thread

from jsonpickle  import decode

from db_handler  import DBHandler
from api_handler import APIHandler


IP = "127.0.0.1"
PORT = 12345
CLIENTS_LIMIT = 10

server = socket(AF_INET, SOCK_STREAM)
server.bind((IP, PORT))
server.listen(CLIENTS_LIMIT)

clients: list[Thread] = []
waiting: int = 0


def client_logic(thread_index:int, conn:socket) -> None:
    client_uuid = None
    current_image_animal = None
    current_image_url = None

    try:
     while True:
      match conn.recv(1024).decode():

        case 'log_in':
            data = decode(conn.recv(1024))

            login    = data['login']
            password = data['password']

            res = DBHandler.log_in(login, password)

            if res: client_uuid = res

            conn.send(b'1' if res else b'0')

        case 'sign_up':
            data = decode(conn.recv(1024))

            login    = data['login']
            password = data['password']

            res = DBHandler.sign_up(login, password)

            if res: client_uuid = res

            conn.send(b'1' if res else b'0')

        case 'get_img':
          match conn.recv(1024).decode():
            case 'cat':
                res = APIHandler.get_rand_cat()
                if not res: conn.send(b'0'); continue
                img_binary, img_url = res
                DBHandler.log_user_act(client_uuid, f'cat image request', img_url)
                conn.sendall(img_binary+b'<!>')
                current_image_url = img_url
                current_image_animal = 'cat'

            case 'dog':
                res = APIHandler.get_rand_dog()
                if not res: conn.send(b'0'); continue
                img_binary, img_url = res
                DBHandler.log_user_act(client_uuid, f'dog image request', img_url)
                conn.sendall(img_binary+b'<!>')
                current_image_url = img_url
                current_image_animal = 'dog'

            case 'bird':
                res = APIHandler.get_rand_bird()
                if not res: conn.send(b'0'); continue
                img_binary, img_url = res
                DBHandler.log_user_act(client_uuid, f'bird image request', img_url)
                conn.sendall(img_binary+b'<!>')
                current_image_url = img_url
                current_image_animal = 'bird'

        case 'downloading':
            DBHandler.log_user_act(client_uuid, f'downloading {current_image_animal} image', current_image_url)

        case 'end':
            break

    except ConnectionResetError:
        ...
    except Exception as error:
        print(f'CLIENT ERROR: {error.__str__()}')
        for i in __import__('traceback').extract_tb(error.__traceback__):
            file = i.filename.split('\\')[-1]
            print(f'line: {i.lineno:3} file: {file} path: {i.filename}')

    conn.close()
    thread_end(thread_index)


def thread_end(thread_index:int) -> None:
    global clients, waiting

    clients.pop(thread_index)

    if not waiting:
        new_thread()


def new_thread() -> None:
    global clients, waiting

    waiting += 1
    conn = server.accept()[0]
    waiting -= 1

    new_thread_ = Thread(target=client_logic,
                        args=(len(clients), conn),
                        daemon=True)
    new_thread_.start()

    clients.append(new_thread_)

    if len(clients) < CLIENTS_LIMIT:
        new_thread()


new_thread()