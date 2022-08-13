from discord.ext import commands
from pathlib import Path
from asyncio.subprocess import PIPE, STDOUT
import asyncio
import discord
import configparser
import os
import platform
import threading

import pexpect


# NOTE: Run the bot with sudo to avoid have to enter it during execution - Requires packages to be installed globally

class Server():
    def __init__(self):
        self.token = ''
        self.jar_path = ''
        self.ram = ''

        self.script_path = ''
        self.ss_override = False
        
        self.server_input = None
        self.get_properties()

        self.process = None
        self.reader = None

    def get_properties(self):
        parser = configparser.ConfigParser()
        dirname = os.path.dirname(__file__)
        c_file = os.path.join(dirname, 'config_backup.txt')

        parser.read(c_file)

        self.token = parser.get('required', 'token')

        ss = parser.get('optional', 'sh_script_override')
        if not (ss.isspace() or ss == ''):
            self.ss_override = True
            self.script_path = ss
        else:
            self.jar_path = parser.get('required', 'server_jar')
            self.ram = parser.get('required', 'ram')

    async def start(self):
        print('Starting server')

        if self.ss_override:
            print(f'Run shell script: {self.script_path}')
            cd_path = Path(self.script_path).parent.absolute()
            cmd = ['sh', self.script_path] # DEPENDS ON OS
        else:
            print(f'Run server jar: {self.ram}, {self.jar_path}')
            cd_path = Path(self.jar_path).parent.absolute()
            cmd = ['java', f'-Xms{self.ram}', f'-Xmx{self.ram}', '-jar', self.jar_path, '--nogui']

                
        self.process = pexpect.spawn(' '.join(cmd), cwd=cd_path)
        print(f'Command run: {cmd}')


    def output_reader(self):
        while True:
            if server.process is None:
                continue
            try:
                line = server.process.readline()
                if not line:
                    break
                print(line)
            except Exception as e:
                print(f'Reader Exception: {e}')
    
    def start_reader(self):
        self.reader = threading.Thread(target=server.output_reader)
        self.reader.start()
    


intents = discord.Intents.default()
intents.members = True

# Use '$' as the command prefix
client = commands.Bot(command_prefix = '$')
server = Server()

    
@client.event
async def on_ready():
    print("The bot is ready.")


@client.command()
async def start(ctx):
    '''Starts the server'''

    print("Command Recieved: status")

    #try:
    if server.process is not None:
        await ctx.send(f"Server is already running.")
        return
    await ctx.send(f"{str(ctx.author)[:-5]} is starting the server.")
    asyncio.create_task(server.start())
    
    server.start_reader()


    #except Exception as e:
    #    print(f'Bot Error: {e}')
    #    await ctx.send(f"There was a problem starting the server: {e}")





    


@client.command()
async def stop(ctx):
    '''Stops the server'''

    print("Command Recieved: stop")

    if server.process is None:
        await ctx.send(f"Server is not running, can't stop.")
        return
    await ctx.send(f"{str(ctx.author)[:-5]} is stopping the server.")
    #server.process.communicate(input='stop', timeout=1E-3)
    #server.process.stdin.write("stop\n")
    server.process.write("stop\n")
    server.process = None
    server.reader.join()
    
@client.command()
async def status(ctx):
    '''Shows server status'''
    print("Command Recieved: status")

    if server.process is None:
        await ctx.send(f"Server is not running.")
    else:
       await ctx.send(f"Server is running.") 


@client.command()
async def cmd(ctx, *args):
    '''Issues a server command'''


    cmd = ' '.join(args)
    print(f"Command Recieved: command {cmd}")

    if server.process is None:
        await ctx.send("The server is not running, can't run command.")
        return
    
    if cmd == 'stop':
        await ctx.send("Stop cannot be run as server command (Use $stop)")
        return

    await ctx.send(f"{str(ctx.author)[:-5]} is executing server command: {cmd}")
    server.process.write(f"{cmd}\n")

@client.command()
async def test(ctx):
    '''For testing purposes'''
    print("Command Recieved: test")
    await ctx.send("Test command functional.")





if __name__ == '__main__':
    client.run(server.token)




