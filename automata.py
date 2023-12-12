import subprocess
import time
import os

# config.py

config_file = "py.config.txt"

# Check if the configuration file exists
if os.path.isfile(config_file):
    # Configuration file exists, source it
    exec(open(config_file).read())
else:
    # Ask the user for API keys and other configurations
    input_text1 = input("Enter Your Node 1 API: ")
    input_text2 = input("Enter Your Node 2 API: ")
    input_text3 = input("Enter Your Node 3 API (press Enter to skip): ")
    bot_token = input("Enter your Telegram Bot Token (press Enter to continue without telegram notifications): ")
    chat_id = input("Enter your Telegram Chat ID (press Enter to continue without telegram notifications): ")
    work_duration = input("Enter the work duration of each node (e.g., 6h 20m): ")
    start_time = input("Enter the desired start time in HH:MM format: ")
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    # Save the entered values to the configuration file
    with open(config_file, "w") as config:
        config.write(f'input_text1="{input_text1}"\n')
        config.write(f'input_text2="{input_text2}"\n')
        config.write(f'input_text3="{input_text3}"\n')
        config.write(f'bot_token="{bot_token}"\n')
        config.write(f'chat_id="{chat_id}"\n')
        config.write(f'work_duration="{work_duration}"\n')
        config.write(f'start_time="{start_time}"\n')

# main.py

# Source the configuration file
# exec(open("config.py").read())
start_command = ["/usr/local/bin/myria-node", "--start"]
stop_command = ["/usr/local/bin/myria-node", "--stop"]

def send_notification(notification_text):
    if bot_token and chat_id:
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        subprocess.run(["curl", "-s", "-X", "POST", telegram_url, "-d", f"chat_id={chat_id}", "-d", f"text={notification_text}"])
    else:
        print("Bot token or chat_id is not set. Skipping notification.")

def start_service(input_text):
    result = subprocess.run(start_command, input=input_text.encode(), text=True, capture_output=True)
    if result.returncode == 0:
        print("Service started successfully")
        send_notification("Service started successfully")
    else:
        print("Failed to start service")
        send_notification("Failed to start service")
        exit(1)

def stop_service(input_text):
    result = subprocess.run(stop_command, input=input_text.encode(), text=True, capture_output=True)
    if result.returncode == 0:
        print("Service stopped successfully")
        send_notification("Service stopped successfully")
    else:
        print("Failed to stop service")
        send_notification("Failed to stop service")

counter = 0

while True:
    # Get the current time in 24-hour format
    current_time = time.strftime("%H:%M")

    # Calculate the time difference in minutes
    desired_minutes = time.mktime(time.strptime(start_time, "%H:%M"))
    current_minutes = time.mktime(time.strptime(current_time, "%H:%M"))

    time_difference = int(desired_minutes - current_minutes)

    # Check if the desired time is in the future
    if time_difference > 0:
        print(f"Waiting until {start_time} to run the command...")
        time.sleep(time_difference)
    else:
        print(f"Executing your command at {start_time}")

        if input_text1:
            counter += 1
            print(f"The value of API is: {input_text1}")
            start_service(input_text1)

            if bot_token:
                output = subprocess.check_output(["/usr/local/bin/myria-node", "--status"]).decode()
                message = f"Command output:\n{output}"
                print(message)
                if chat_id:
                    send_notification(message)
                else:
                    print("Telegram chat_id is not set. Skipping notification.")
            else:
                print("Telegram bot_token is not set. Skipping notification.")

            time.sleep(work_duration)
            stop_service(input_text1)
        else:
            print("Variable1 does not exist.")

        if input_text2:
            counter += 1
            print(f"The value of API is: {input_text2}")
            start_service(input_text2)

            if bot_token:
                output = subprocess.check_output(["/usr/local/bin/myria-node", "--status"]).decode()
                message = f"Command output:\n{output}"
                print(message)
                if chat_id:
                    send_notification(message)
                else:
                    print("Telegram chat_id is not set. Skipping notification.")
            else:
                print("Telegram bot_token is not set. Skipping notification.")

            time.sleep(work_duration)
            stop_service(input_text2)
        else:
            print("Variable2 does not exist.")

        if input_text3:
            counter += 1
            print(f"The value of API is: {input_text3}")
            start_service(input_text3)

            if bot_token:
                output = subprocess.check_output(["/usr/local/bin/myria-node", "--status"]).decode()
                message = f"Command output:\n{output}"
                print(message)
                if chat_id:
                    send_notification(message)
                else:
                    print("Telegram chat_id is not set. Skipping notification.")
            else:
                print("Telegram bot_token is not set. Skipping notification.")

            time.sleep(work_duration)
            stop_service(input_text3)
        else:
            print("Variable3 does not exist.")

        # Exit the script after running the commands
        exit(0)
