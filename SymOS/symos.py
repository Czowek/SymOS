import os
import platform
import psutil
import getpass
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

ROOT_FOLDER = os.getcwd()  # Set the root folder to the current working directory
PASSWORDS_FOLDER = "passwords"  # Folder to store passwords
USERS_FOLDER = "users"  # Folder to store user information
SYSTEM_LOG_FILE = "system_log.txt"  # File to store system logs
PASSWORDS_FILE = "passwords.txt"  # File to store passwords
PASSWORDS_PATH = os.path.join(ROOT_FOLDER, PASSWORDS_FOLDER, PASSWORDS_FILE)
USERS_PATH = os.path.join(ROOT_FOLDER, USERS_FOLDER)
SYSTEM_LOG_PATH = os.path.join(ROOT_FOLDER, SYSTEM_LOG_FILE)
PASSWORDS = {}  # Dictionary to store passwords

def about_symos():
    about = print(f"{Fore.GREEN}SymOS{Style.RESET_ALL} {Fore.CYAN}is a fun little project that I'm working on right now. It is and always will be Open-Source. \n"
                  f"It's suppoused to simulate a text based operating system (Linux-like). \n"
                  f"Features: \n"
                  f"- Basic file and directory management. \n"
                  f"- System information display. \n"
                  f"- User authentication and password protection. \n"
                  f"- System logging (on your pc only). \n"
                  f"- User logging (on your pc only). \n"
                  f"- Command line interface. \n"

                  f"This project is a result of a boredom and willingness to learn how to operate in python. \n"

                  f"Created by: Czowek \n"
                  f"Github: https://github.com/Czowek \n"
                  f"Version: 1.0 \n"
                  f"License: MIT \n"
                  f"Last update: 26.12.2023 01:35 AM \n"
                  f"{Fore.LIGHTBLUE_EX}Thanks for using SymOS!{Style.RESET_ALL} \n"
                  f"{Fore.GREEN}Enjoy!{Style.RESET_ALL}")
def create_passwords_folder():
    passwords_folder_path = os.path.join(ROOT_FOLDER, PASSWORDS_FOLDER)
    if not os.path.exists(passwords_folder_path):
        os.mkdir(passwords_folder_path)
        # Create an empty __init__.py file to indicate that "passwords" is a package
        with open(os.path.join(passwords_folder_path, "__init__.py"), 'w'):
            pass

def create_users_folder():
    users_folder_path = os.path.join(ROOT_FOLDER, USERS_FOLDER)
    if not os.path.exists(users_folder_path):
        os.mkdir(users_folder_path)

def create_user_folder(username):
    user_folder_path = os.path.join(USERS_PATH, username)
    if not os.path.exists(user_folder_path):
        os.mkdir(user_folder_path)
        # Create an empty user_log.txt file to store user events
        with open(os.path.join(user_folder_path, "user_log.txt"), 'a'):
            pass
    else:
        print(f"{Fore.RED}User '{username}' already exists. Logging in...")
        log_system_event(f"User '{username}' logged in.")

def create_system_log():
    with open(SYSTEM_LOG_PATH, 'a'):
        pass

def log_system_event(event):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(SYSTEM_LOG_PATH, 'a') as log_file:
        log_file.write(f"{timestamp} - {event}\n")

def load_passwords():
    if os.path.exists(PASSWORDS_PATH):
        with open(PASSWORDS_PATH, 'r') as file:
            for line in file:
                username, password = line.strip().split(':')
                PASSWORDS[username] = password

def save_passwords():
    with open(PASSWORDS_PATH, 'w') as file:
        for username, password in PASSWORDS.items():
            file.write(f"{username}:{password}\n")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_commands():
    print(f"{Fore.GREEN}SymOS Commands:")
    print(f"{Fore.CYAN}1. dir - List files in the current directory")
    print(f"{Fore.CYAN}2. goto <directory> - Change current directory")
    print(f"{Fore.CYAN}3. mkdir <directory> - Create a new directory")
    print(f"{Fore.CYAN}4. del <file/directory> - Delete a file or directory")
    print(f"{Fore.CYAN}5. rename <old_name> <new_name> - Rename a file or directory")
    print(f"{Fore.CYAN}6. create <file_name> - Create a new text file")
    print(f"{Fore.CYAN}7. edit <file_name> - Add content to a text file")
    print(f"{Fore.CYAN}8. open <file_name> - Display the content of a text file")
    print(f"{Fore.CYAN}9 sysinfo - Display system information")
    print(f"{Fore.CYAN}9. help - Display this")
    print(f"{Fore.CYAN}10. showtime - Display time")
    print(f"{Fore.CYAN}11. exit - Exit SymOS")
    print(f"{Fore.CYAN}12. clear - Clear the screen")
    print(f"{Fore.CYAN}13. about - Display information about SymOS")
    print(Style.RESET_ALL)

def get_system_info():
    system_info = f"Operating System: {platform.system()} {platform.release()}\n"
    system_info += f"Python Version: {platform.python_version()}\n"
    system_info += f"Current Directory: {os.getcwd()}\n"
    system_info += f"Total Users: {len(PASSWORDS)}\n"
    system_info += f"System Log: {SYSTEM_LOG_PATH}\n"
    system_info += f"Available Disk Space: {get_available_disk_space()} MB\n"
    return system_info

def get_available_disk_space():
    disk = psutil.disk_usage(os.getcwd())
    return disk.free // (1024 * 1024)  # Convert to MB

def delete_file(file_name):
    try:
        os.remove(file_name)
        print(f"{Fore.GREEN}File '{file_name}' deleted.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"{Fore.RED}Error: Access denied. Make sure you have the necessary permissions.")
    print(Style.RESET_ALL)

def log_user_event(username, event):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_log_path = os.path.join(USERS_PATH, username, "user_log.txt")
    with open(user_log_path, 'a') as log_file:
        log_file.write(f"{timestamp} - {event}\n")


def rename_item(username, old_name, new_name):
    try:
        old_path = os.path.join(username, old_name)
        new_path = os.path.join(username, new_name)
        os.rename(old_path, new_path)
        print(f"{Fore.GREEN}Successfully renamed '{old_name}' to '{new_name}'.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File or directory '{old_name}' not found.")
    except FileExistsError:
        print(f"{Fore.RED}Error: '{new_name}' already exists.")
    print(Style.RESET_ALL)

def create_file(file_name, username):
    try:
        with open(file_name, 'w') as file:
            print(f"{Fore.GREEN}File '{file_name}' created.")
    except PermissionError:
        print(f"{Fore.RED}Error: Access denied. Make sure you have the necessary permissions.")
    print(Style.RESET_ALL)

def open_file(file_name, username):
    try:
        with open(file_name, 'r') as file:
            print(f"{Fore.CYAN}Content of '{file_name}':")
            print(file.read())
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"{Fore.RED}Error: Access denied. Make sure you have the necessary permissions.")
    print(Style.RESET_ALL)

def edit_file(file_name, username):
    try:
        with open(file_name, 'a') as file:
            content = input(f"{Fore.CYAN}Enter text to add to the file (press Enter to finish):\n")
            file.write(content + '\n')
            print(f"{Fore.GREEN}Content added to '{file_name}'.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"{Fore.RED}Error: Access denied. Make sure you have the necessary permissions.")
    print(Style.RESET_ALL)

def delete_file(file_name, username):
    try:
        os.remove(file_name)
        print(f"{Fore.GREEN}File '{file_name}' deleted.")
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_name}' not found.")
    except PermissionError:
        print(f"{Fore.RED}Error: Access denied. Make sure you have the necessary permissions.")
    print(Style.RESET_ALL)


def set_password(username, password, user_who_set_password=None):
    PASSWORDS[username] = password
    save_passwords()
    if user_who_set_password:
        log_system_event(f"User '{user_who_set_password}' set a password for '{username}'.")
        log_user_event(user_who_set_password, f"Set a password for '{username}'.")
    else:
        log_system_event(f"Password set for '{username}'.")


def verify_password(username):
    if username in PASSWORDS:
        entered_password = getpass.getpass(f"{Fore.CYAN}Enter password for '{username}': ")
        return entered_password == PASSWORDS[username]
    else:
        create_user(username)
        print(f"{Fore.GREEN}User '{username}' created.")
        log_system_event(f"User created: {username}")

        entered_password = getpass.getpass(f"{Fore.CYAN}Enter password for '{username}': ")
        PASSWORDS[username] = entered_password
        save_passwords()
        return True

def create_user(username):
    password = getpass.getpass(f"{Fore.CYAN}Create a password for '{username}': ")
    PASSWORDS[username] = password
    save_passwords()
    create_user_folder(username)

def authenticate_user(username):
    if username not in PASSWORDS:
        print(f"{Fore.YELLOW}User '{username}' not found. Creating a new user...")
        create_user_folder(username)
        set_password(username, getpass.getpass(f"{Fore.CYAN}Create a password for '{username}': "), username)
        print(f"{Fore.GREEN}User '{username}' created. Logging in...")
        log_system_event(f"New user '{username}' created and logged in.")
        return True  # Log in the newly created user
    else:
        print(f"{Fore.CYAN}Welcome, {username}!")
        attempts = 3
        while attempts > 0:
            if verify_password(username):
                print(f"{Fore.GREEN}Authentication successful. Welcome, {username}!")
                log_system_event(f"User '{username}' logged in.")
                return True
            else:
                attempts -= 1
                print(f"{Fore.RED}Incorrect password. {attempts} attempts remaining.")
        print(f"{Fore.RED}Authentication failed. Exiting SymOS.")
        log_system_event(f"Authentication failed for user: {username}")
        exit()

def SymOS():
    create_passwords_folder()
    create_users_folder()
    load_passwords()
    username = input(f"{Fore.CYAN}Enter your username: ")
    if authenticate_user(username):  # Check if the user was just created
        os.chdir(os.path.join(USERS_PATH, username))
        current_dir = os.getcwd()
        print(f"{Fore.GREEN}Welcome to SymOS, {username}! You are now in your home directory.")
        log_system_event(f"User '{username}' logged in and moved to their home directory.")
    else:
        print(f"{Fore.RED}User authentication failed. Exiting SymOS.")
        exit()

    while True:
        user_input = input(f"{Fore.YELLOW}[{username}@{os.path.basename(current_dir)}]>{Style.RESET_ALL} ")
        
        if user_input.lower() == 'exit':
            print(f"{Fore.GREEN}Exiting SymOS. Goodbye!")
            log_system_event(f"User '{username}' exited SymOS.")
            save_passwords()
            break
        elif user_input.lower() == 'dir':
            try:
                print(f"{Fore.CYAN}Listing files in the current directory:")
                files = os.listdir(current_dir)
                for file in files:
                    file_path = os.path.join(current_dir, file)
                    created_timestamp = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    last_modified_timestamp = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                    print(f"{Fore.GREEN}{file}\tCreated: {created_timestamp}\tLast Modified: {last_modified_timestamp}")
                print(Style.RESET_ALL)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
                print(Style.RESET_ALL)
        elif user_input.lower().startswith('goto '):
            try:
                new_dir = user_input[5:]
                target_dir = os.path.join(current_dir, new_dir)
                if os.path.relpath(target_dir, current_dir).startswith('..'):
                    print(f"{Fore.RED}Error: Cannot navigate outside of the current directory.")
                else:
                    os.chdir(target_dir)
                    current_dir = os.getcwd()
                    log_system_event(f"User '{username}' moved to '{current_dir}' using 'goto' command.")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('mkdir '):
            try:
                new_dir = user_input[6:]
                os.mkdir(new_dir)
                print(f"{Fore.GREEN}Directory '{new_dir}' created.")
                log_system_event(f"User '{username}' created directory '{new_dir}'.")
                log_user_event(username, f"Created directory '{new_dir}'.")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('del '):
            try:
                item_to_delete = user_input[4:]
                delete_file(item_to_delete, username)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('rename '):
            try:
             _, old_name, new_name = user_input.split()
             rename_item(username, old_name, new_name)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('create '):
            try:
                file_to_create = user_input[7:]
                create_file(file_to_create, username)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('edit '):
            try:
                file_to_edit = user_input[5:]
                edit_file(file_to_edit, username)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower().startswith('open '):
            try:
                file_to_open = user_input[5:]
                open_file(file_to_open, username)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower() == 'sysinfo':
            try:
                print(f"{Fore.CYAN}System Information:")
                print(get_system_info())
                print(Style.RESET_ALL)
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower() == 'showtime':
            try:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{Fore.CYAN}Current system time: {current_time}")
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
            print(Style.RESET_ALL)
        elif user_input.lower() == 'about':
            about_symos()
        elif user_input.lower() == 'help':
            show_commands()
        elif user_input.lower() == 'cls' or user_input.lower() == 'clear':
            clear_screen()
        else:
            print(f"{Fore.RED}Error: Unknown command '{user_input}'. Type 'help' for a list of commands.")
            print(Style.RESET_ALL)

if __name__ == "__main__":
    clear_screen()
    print(f"{Fore.GREEN}Welcome to SymOS!")
    SymOS()
