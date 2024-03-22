"""
this is only avaliable for Windows.

DISCLAIMER:
If you use this discord tools not in TOS like, spamming, nukeing, raiding, etc your account can get BANNED 
and I(the creator) won't care about the aftermath of it.
"""
import os, sys
import typing
import additional
import discord, asyncio
import config, msvcrt
from collections import deque
term_size = os.get_terminal_size()
TOKEN = 'YOUR_TOKEN_HERE'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

mess_history:deque[discord.Message] = deque([])
servers = deque([])
channels = deque([])
current_server_index = -1
current_channel_index = -1

async def list_servers():
    global current_server_index, current_channel_index, servers, channels
    servers = deque([])
    for server in client.guilds:
        servers.append(server.name)
    return

async def list_channels():
    global current_server_index, current_channel_index, servers, channels
    server = client.guilds[current_server_index]
    channels = deque([])
    for chan in server.text_channels:
        channels.append(chan.name)
    return

async def send_message(message):
    global current_server_index, current_channel_index, servers, channels
    server = client.guilds[current_server_index]
    channel = list(server.text_channels)[current_channel_index]
    await channel.send(message)

@client.event
async def on_ready():
    activity = discord.Game(name = "discli.py")
    await client.change_presence(status=discord.Status.online, activity=activity)
    await main()

input_txt = ""
async def display_message(msg:typing.Union[discord.Message, None]):
        global input_txt
        if msg is not None and isinstance(msg, discord.Message):
            os.system("cls") if os.name == "nt" else os.system("clear")
            if len(mess_history) == term_size[1]-1:
                mess_history.popleft()
            mess_history.append(f"{msg.author}: {msg.content}\n")
            sys.stdout.write(f"{config.AnsiCode.Style.RESET_ALL}{config.AnsiCode.Fore.WHITE}")
            for message in mess_history:
                sys.stdout.write(message)
        elif mess_history == deque([]):
            sys.stdout.write(f"{config.AnsiCode.Style.RESET_ALL}{config.AnsiCode.Fore.WHITE}")
            history = client.guilds[current_server_index].text_channels[current_channel_index].history(limit=term_size[1]-1)
            async for message in history:
                mess_history.appendleft(f"{message.author}: {message.content}\n")
            for message in mess_history:
                sys.stdout.write(f"{message}")

        await asyncio.sleep(0)  # currently fixed heartbeat got blocked. code by chatgpt ofc.
        
        sys.stdout.write(f"\x1b[2K\r\033[{term_size[1]}B{config.AnsiCode.Style.BRIGHT}{config.AnsiCode.Fore.LY}{input_txt}")
        if msvcrt.kbhit():
            char = msvcrt.getch()
            if char == b"\r":
                if input_txt.strip() != "":
                    await client.guilds[current_server_index].text_channels[current_channel_index].send(input_txt)
                input_txt=""
                sys.stdout.write("\x1b[2K\r")
            elif char == b"\b":
                input_txt = input_txt[:-1]
                sys.stdout.write("\b \b") if input_txt != "" else 0
            elif char == b"\000" or char == b"\xe0":
                char = msvcrt.getch()
                del char
            else:
                input_txt += char.decode("utf-8")
                sys.stdout.write(char.decode("utf-8"))
        sys.stdout.flush()


@client.event
async def on_message(msg:discord.Message):
    global current_server_index, current_channel_index, servers, channels
    if current_channel_index != -1 and current_server_index != -1 and msg.channel.name == channels[current_channel_index]:
        await display_message(msg)

async def main():
    global current_server_index, current_channel_index, servers, channels
    while True:
        try:
            await list_servers()
            prmt_servers = servers
            prmt_servers.append("QUIT")

            current_server_index = additional.arrow_key_menu(prmt_servers, "Servers:")

            if current_server_index+1 < len(servers):
                while True:
                    try:
                        await list_channels()
                        prmt_channels = channels
                        prmt_channels.append("--Go Back--")

                        current_channel_index = additional.arrow_key_menu(prmt_channels, f"Channels in {client.guilds[current_server_index].name}:")
                        if current_channel_index+1 < len(channels):
                            os.system("cls") if os.name == "nt" else os.system("clear")
                            while True:
                                try:
                                    await display_message(None)
                                except Exception as e:
                                    print(f"Error: {e}"); quit(-1)
                        else: current_channel_index=-1;break
                    except Exception as e:
                        print(f"Error: {e}"); quit(-1)
            else:
                await client.close()
                quit(0)
        except Exception as e:
            print(f"Error: {e}"); quit(-1)

client.run(TOKEN)
