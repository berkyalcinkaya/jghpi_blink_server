from os import name
from comm import send_command_open_comm

if __name__ == "__main__":
    send_command_open_comm("dio set DO_G0 0 inactive")