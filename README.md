# Discord-Minecraft-Server-Starter
A Discord bot that can start, stop, and issue commands to a Minecraft server. 

## Dependencies
- discord
- pexpect

## How to run
1.) Create a Discord bot at https://discord.com/developers/applications and copy the token.

2.) Add the bot to your server using the OAuth2 URL Generator

3.) Clone this repo
```
git clone https://github.com/Spencerv1/Discord-MC-Server-Starter
```
4.) Install dependencies
```
pip install -r requirements.txt
```
5.) Replace the placeholder text in config.txt. server_jar and ram do not have to be specified if using sh_script_override.

6.) Run
```
python main.py
```

## Commands
- $cmd    - Issues a server command
- $help   - Shows help message
- $start  - Starts the server
- $status - Shows server status
- $stop   - Stops the server
- $test   - For testing purposes

Type $help command for more info on a command.
You can also type $help category for more info on a category.
