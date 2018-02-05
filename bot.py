import pydle

# Simple echo bot.
class MalBot(pydle.Client):
    def on_connect(self):
         self.join('#botnet')

    def on_message(self, source, target, message):
         self.message(target, message)

client = MalBot('MalBot', realname='MalBot')
client.connect('192.168.67.130', 6697, tls=True, tls_verify=False)
client.handle_forever()