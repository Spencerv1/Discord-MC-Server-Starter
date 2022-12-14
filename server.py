import pexpect
from pexpect import popen_spawn
from pexpect.exceptions import TIMEOUT
from pathlib import Path
from multiprocessing import Process
import configparser
import os
import sys
from time import sleep


class Server:
    def __init__(self):
        self.token = ""
        self.jar_path = ""
        self.ram = ""
        self.script_path = ""
        self.ss_override = False
        self.get_properties()
        self.process = None
        self.reader = None
        self.stop_reader = False

    def get_properties(self):
        parser = configparser.ConfigParser()
        dirname = os.path.dirname(__file__)
        c_file = os.path.join(dirname, "config_backup.txt")
        parser.read(c_file)

        self.token = parser.get("required", "token")

        ss = parser.get("optional", "sh_script_override")
        if not (ss.isspace() or ss == ""):
            self.ss_override = True
            self.script_path = ss
        else:
            self.jar_path = parser.get("required", "server_jar")
            self.ram = parser.get("required", "ram")

    async def start(self):
        print("Starting server")

        if self.ss_override:
            print(f"Run shell script: {self.script_path}")
            cd_path = Path(self.script_path).parent.absolute()
            cmd = ["sh", self.script_path]  # DEPENDS ON OS
        else:
            print(f"Run server jar: {self.ram}, {self.jar_path}")
            cd_path = Path(self.jar_path).parent.absolute()
            cmd = [
                "java",
                f"-Xms{self.ram}",
                f"-Xmx{self.ram}",
                "-jar",
                self.jar_path,
                "--nogui",
            ]

        if 'win' in sys.platform:
            self.process = popen_spawn.PopenSpawn(" ".join(cmd), cwd=cd_path)
        else:
            self.process = pexpect.spawn(" ".join(cmd), cwd=cd_path)
        print(f"Command run: {cmd}")


    def output_reader(self):
        while True:
            '''
            if self.stop_reader:
                print('Stop reader')
                self.stop_reader = False
                break
            '''
            #if self.process is None: # Probably change this - Keeps stop message from appearing
            #    continue
            try:
                line = self.process.readline()
                if line:
                    print(str(line))
            except AttributeError:
                pass
            except TIMEOUT:
                print('Output reader timeout')
            #except Exception as e:
            #    print(f"Reader Exception: {e}")
            sleep(0.01)

