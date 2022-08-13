from discord.ext import commands
from server import Server
import discord
import asyncio

# NOTE: Run the bot with sudo to avoid having to enter password during execution
# ^ Requires dependencies to be installed globally ^

intents = discord.Intents.default()
intents.members = True
server = Server()
help_cmd = commands.DefaultHelpCommand(no_category='Commands')
description = "Server Starter Discord Bot\n"\
              "Developer: Spencer Verhoff\n"\
              "GitHub: https://github.com/Spencerv1/Discord-MC-Server-Starter"
client = commands.Bot(command_prefix="$", description=description, help_command=help_cmd)


@client.event
async def on_ready():
    print("The bot is ready.")


@client.command()
async def start(ctx):
    """Starts the server"""
    print("Command Recieved: status")

    if server.process is not None:
        await ctx.send(f"Server is already running.")
        return
    await ctx.send(f"{str(ctx.author)[:-5]} is starting the server.")
    asyncio.create_task(server.start())
    server.start_reader()


@client.command()
async def stop(ctx):
    """Stops the server"""
    print("Command Recieved: stop")

    if server.process is None:
        await ctx.send(f"Server is not running, can't stop.")
        return
    await ctx.send(f"{str(ctx.author)[:-5]} is stopping the server.")
    server.process.write("stop\n")
    server.process = None
    server.stop_reader = True
    server.reader.join()


@client.command()
async def status(ctx):
    """Shows server status"""
    print("Command Recieved: status")

    if server.process is None:
        await ctx.send(f"Server is not running.")
    else:
        await ctx.send(f"Server is running.")


@client.command()
async def cmd(ctx, *args):
    """Issues a server command"""
    cmd = " ".join(args)
    print(f"Command Recieved: command {cmd}")

    if server.process is None:
        await ctx.send("The server is not running, can't run command.")
        return

    if cmd == "stop":
        await ctx.send("Stop cannot be run as server command (Use $stop)")
        return

    await ctx.send(f"{str(ctx.author)[:-5]} is executing server command: {cmd}")
    server.process.write(f"{cmd}\n")


@client.command()
async def test(ctx):
    """For testing purposes"""
    print("Command Recieved: test")
    await ctx.send("Test command functional.")


if __name__ == "__main__":
    client.run(server.token)
