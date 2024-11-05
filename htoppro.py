#!/usr/bin/env python3

import os
import subprocess
import time
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Function to display the header with stylized ASCII art and a red to white gradient
def header():
    os.system('clear')
    
    # ASCII art with a gradient from red to white
    ascii_art = [
        r" __ __  ______   ___   ____  ____  ____   ___  ",
        r"|  |  ||      | /   \ |    \|    \|    \ /   \ ",
        r"|  |  ||      ||     ||  o  )  o  )  D  )     |",
        r"|  _  ||_|  |_||  O  ||   _/|   _/|    /|  O  |",
        r"|  |  |  |  |  |     ||  |  |  |  |    \|     |",
        r"|  |  |  |  |  |     ||  |  |  |  |  .  \     |",
        r"|__|__|  |__|   \___/ |__|  |__|  |__|\_|\___/ ",
        r"                                               "
    ]
    
    colors = [Fore.RED, Fore.LIGHTRED_EX, Fore.WHITE]  # Gradient from red to white
    
    for i, line in enumerate(ascii_art):
        # Transition from red to white as we go down each line
        color = colors[min(i, len(colors) - 1)]
        print(color + Style.BRIGHT + line)

    print(Fore.YELLOW + "Welcome to htoppro - Advanced Process Manager for Arch Linux")
    print(Fore.YELLOW + "=" * 60)

# Display help information
def show_help():
    header()
    print(Fore.GREEN + "Options:")
    print("    1. " + Fore.CYAN + "View processes (htop)")
    print("    2. " + Fore.CYAN + "Filter processes by name or user")
    print("    3. " + Fore.CYAN + "Manage a process by PID (kill, suspend, resume)")
    print("    4. " + Fore.CYAN + "Show system stats (CPU & Memory)")
    print("    5. " + Fore.CYAN + "View credits")
    print("    6. " + Fore.CYAN + "Quit htoppro")
    print("    help - " + Fore.CYAN + "Show this help message")
    print(Fore.YELLOW + "=" * 60)
    input("Press Enter to return to menu...")

# Function to create credits file
def create_credits_file():
    with open("credits.txt", "w") as f:
        f.write("This program was developed with the help of ChatGPT. It was a fun learning experience!\n")
        f.write("Thank you for using htoppro!\n")

# Display credits with cowsay animation
def show_cowsay_animation():
    messages = ["I", "Love", "You"]
    for msg in messages:
        os.system('clear')
        os.system(f"cowsay {msg}")
        time.sleep(1)  # Pause for a second between messages
    os.system('clear')

# Main menu function with colorized options
def main_menu():
    header()
    print(Fore.GREEN + "1. View processes (htop)")
    print(Fore.GREEN + "2. Filter processes")
    print(Fore.GREEN + "3. Manage a process by PID")
    print(Fore.GREEN + "4. Show system stats")
    print(Fore.GREEN + "5. View credits")
    print(Fore.GREEN + "6. Quit")
    print(Fore.YELLOW + "=" * 60)
    return input(Fore.CYAN + "Select an option (or type 'help' for assistance): ")

# Function to filter processes
def filter_processes():
    filter_term = input(Fore.CYAN + "Enter process name or user to filter: ")
    header()
    print(Fore.YELLOW + f"Processes matching '{filter_term}':")
    os.system(f"ps aux | grep -i '{filter_term}' | grep -v 'grep'")
    input(Fore.CYAN + "Press Enter to continue...")

# Function to manage processes by PID with colorized options
def manage_process_by_pid():
    while True:
        pid = input(Fore.CYAN + "Enter PID to manage (or type 'back' to return to menu): ")
        if pid.lower() == 'back':
            return
        
        print(Fore.YELLOW + "Options for PID " + pid + ":")
        print("1. Kill")
        print("2. Suspend")
        print("3. Resume")
        print("4. Back to menu")
        action = input(Fore.CYAN + "Select an action: ")

        if action == '1':
            if os.system(f"kill -9 {pid}") == 0:
                print(Fore.RED + f"Process {pid} killed.")
            else:
                print(Fore.RED + f"Failed to kill process {pid}.")
        elif action == '2':
            if os.system(f"kill -STOP {pid}") == 0:
                print(Fore.RED + f"Process {pid} suspended.")
            else:
                print(Fore.RED + f"Failed to suspend process {pid}.")
        elif action == '3':
            if os.system(f"kill -CONT {pid}") == 0:
                print(Fore.RED + f"Process {pid} resumed.")
            else:
                print(Fore.RED + f"Failed to resume process {pid}.")
        elif action == '4':
            return
        else:
            print(Fore.RED + "Invalid option.")
        input(Fore.CYAN + "Press Enter to continue...")

# Function to show system stats
def system_stats():
    header()
    print(Fore.YELLOW + "System Stats (CPU & Memory):")
    os.system("top -b -n1 | head -n 10 | grep -E 'Cpu|Mem'")
    input(Fore.CYAN + "Press Enter to return to menu...")

# Main loop
def main():
    create_credits_file()  # Create the credits file at the start
    while True:
        choice = main_menu()
        if choice == '1':
            # Open htop in a new Tilix window
            os.system("tilix -e htop")
        elif choice == '2':
            filter_processes()
        elif choice == '3':
            manage_process_by_pid()
        elif choice == '4':
            system_stats()
        elif choice == '5':
            show_cowsay_animation()
        elif choice == '6':
            print(Fore.CYAN + "Exiting htoppro...")
            break
        elif choice.lower() == 'help':
            show_help()
        else:
            print(Fore.RED + "Invalid option. Type 'help' for options.")

if __name__ == "__main__":
    # Check if the script is run as root
    if os.geteuid() != 0:
        print(Fore.RED + "Please run as root: sudo ./htoppro.py")
        exit(1)
    
    # Check dependencies
    for cmd in ['htop', 'tilix', 'cowsay']:
        if subprocess.call(["which", cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            print(Fore.RED + f"{cmd} is required. Install it with: sudo pacman -S {cmd}")
            exit(1)
    
    main()
