import socket, select

def send_global (sock, message):
	for socket in connection_list:
		if socket != server_socket and socket != sock :
			try :
				socket.send(message)
			except :
				socket.close()
				connection_list.remove(socket)

if __name__ == "__main__":
	name=""
	record={}
	connection_list = []
	buffer = 4096
	port = 5001

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	server_socket.bind(("localhost", port))
	server_socket.listen(10) 

	connection_list.append(server_socket)

	print "\33[32m \t\t\t\tBat Papo Ta Online\33[0m" 

	while 1:
		rList,wList,error_sockets = select.select(connection_list,[],[])

		for sock in rList:
			if sock == server_socket:
				sockfd, dd = server_socket.accept()
				name=sockfd.recv(buffer)
				connection_list.append(sockfd)
				record[dd]=""
				                
				if name in record.values():
					sockfd.send("\r\33[31m\33[1m Shhh ja pegeram esse user!\n\33[0m")
					del record[dd]
					connection_list.remove(sockfd)
					sockfd.close()
					continue
				else:
					record[dd]=name
					print "Client (%s, %s) conectado" % dd," [",record[dd],"]"
					sockfd.send("\33[32m\r\33[1m Bem vindo. digite 'bye' para sair\n\33[0m")
					sockfd.send("\33[36m\r\33[1m Digite 'list' para saber quem ta aqui\n\33[0m")
					send_global(sockfd, "\33[32m\33[1m\r "+name+" entrou no papo \n\33[0m")

			else:
				try:
					data1 = sock.recv(buffer)
					data=data1[:data1.index("\n")]
                    
					i,p=sock.getpeername()
					if data == "bye":
						msg="\r\33[1m"+"\33[31m "+record[(i,p)]+" saiu da conversa :c \33[0m\n"
						send_global(sock,msg)
						print "Client (%s, %s) ta offline" % (i,p)," [",record[(i,p)],"]"
						connection_list.remove(sock)
						sock.close()
						continue

					elif data == "list":
						for sock in rList:
							name=sockfd.recv(buffer)
							# record[dd]=""
							msg = "Client (%s, %s) conectado" % dd," [",record[dd],"]"
						send_global(msg)
					else:
						msg="\r\33[1m"+"\33[35m "+record[(i,p)]+": "+"\33[0m"+data+"\n"
						send_global(sock,msg)
            
				except:
					(i,p)=sock.getpeername()
					send_global(sock, "\r\33[31m \33[1m"+record[(i,p)]+" caiu :c \33[0m\n")
					print "Client (%s, %s) ta offline (error)" % (i,p)," [",record[(i,p)],"]\n"
					del record[(i,p)]
					connection_list.remove(sock)
					sock.close()
					continue

	server_socket.close()

