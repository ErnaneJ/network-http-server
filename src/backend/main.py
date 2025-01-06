# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Base de um servidor HTTP (python 3)
#
# MODIFICADO POR: Ernane Ferreira e  Quelita Míriam

# importacao das bibliotecas
import socket
import os

# definicao do host e da porta do servidor
HOST = '' # ip do servidor (em branco)
PORT = 8080 # porta do servidor
FRONTEND_FOLDER = '../frontend'
CONTENT_TYPE = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'text/javascript',
    'json': 'application/json',
}

# cria o socket com IPv4 (AF_INET) usando TCP (SOCK_STREAM)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# permite que seja possivel reusar o endereco e porta do servidor caso seja encerrado incorretamente
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

# imprime que o servidor esta pronto para receber conexoes
print ('Serving HTTP on port %s ...' % PORT)

while True:
    # aguarda por novas conexoes
    client_connection, client_address = listen_socket.accept()
    # o metodo .recv recebe os dados enviados por um cliente atraves do socket
    request = client_connection.recv(1024)
    decoded_request = request.decode('utf-8')
    # imprime na tela o que o cliente enviou ao servidor
    print(request)
    if request == b'\r\n':
        method = 'GET'
        route = '/'
        protocol = 'HTTP/1.1'
    else:
        method, route, protocol = decoded_request.split(' ', 2)
    
    # declaracao da resposta do servidor
    if route.split('/')[-1] == '' or '.' not in route.split('/')[-1]:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FRONTEND_FOLDER, route.lstrip('/'), 'index.html') 
    else:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FRONTEND_FOLDER, route.lstrip('/'))
    print("Servidor vai tentar abrir o arquivo: ", file_path)
    if method == 'GET':
        if os.path.exists(file_path) and os.path.isfile(file_path):
            status = "200 OK"
            if file_path.split('.')[-1] in CONTENT_TYPE: 
                content_type = CONTENT_TYPE[file_path.split('.')[-1]]
            else:
                status = "400 Bad Request"
                content_type = 'text/html'
                file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FRONTEND_FOLDER, '400/index.html')
        else:
            status = "404 Not Found"
            content_type = 'text/html'
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FRONTEND_FOLDER, '404/index.html')
    else:
        status = "400 Bad Request"
        content_type = 'text/html'
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), FRONTEND_FOLDER, '400/index.html')
    
    with open(file_path, 'rb') as file:
        file_content = file.read()
    
    http_response = f"""\
HTTP/1.1 {status}
Content-Type: {content_type}
Content-Length: {len(file_content)}

{file_content.decode('utf-8')}
"""
    # servidor retorna o que foi solicitado pelo cliente (neste caso a resposta e generica)
    client_connection.send(http_response.encode('utf-8'))
    # encerra a conexao
    client_connection.close()

# encerra o socket do servidor
listen_socket.close()