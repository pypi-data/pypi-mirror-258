from remoteio import RemoteServer


server_ip = "192.168.1.38"
server_port = 8509

remote_server = RemoteServer(server_ip, server_port)
remote_pin = remote_server.pin(7, 'b') # Use BOARD numbering
# remote_pin = remote_server.pin(4, 'g') # Use GPIO numbering
remote_pin.time(2000) # Time in ms until switch off
remote_pin.on()
# remote_pin.off()
remote_server.close()