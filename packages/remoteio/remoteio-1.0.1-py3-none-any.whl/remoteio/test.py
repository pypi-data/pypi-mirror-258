from remoteio_client import RemoteServer
from time import sleep

server_ip = "192.168.0.90"
server_port = 8509
time = 2000
pin=8
ns='b'
remote_server = RemoteServer(server_ip, server_port)
remote_pin = remote_server.pin(pin, ns)

print(f"On(time=2000) - Pin {pin}({ns})")
remote_pin.on(time_ms=time)
sleep(time/1000)
print(f"Blink() - Pin {pin}({ns})")
remote_pin.blink()
sleep(time/1000)
print(f"On() - Pin {pin}({ns})")
remote_pin.on()
sleep(time*2/1000)
print(f"Off() - Pin {pin}({ns})")
remote_pin.off()
remote_server.close()