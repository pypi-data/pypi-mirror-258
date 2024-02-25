import subprocess
import os
import pexpect


def run_command(command):
    """
    Execute a system command and return its output and return code.

    Args:
    - command: str or list. The command to be executed. If it's a string, it will be passed to the shell for execution.

    Returns:
    - output: str. The output of the command.
    - return_code: int. The return code of the command.
    """
    try:
        if isinstance(command, str):
            output = subprocess.check_output(command, shell=True, universal_newlines=True)
        elif isinstance(command, list):
            output = subprocess.check_output(command, universal_newlines=True)
        else:
            raise ValueError("Invalid command type. Must be a string or list.")

        return_code = 0  # Success
    except subprocess.CalledProcessError as e:
        output = e.output
        return_code = e.returncode

    return output.strip(), return_code


def get_current_pid():
    """
    Get the current process ID (PID).

    Returns:
    - pid: int. The current process ID.
    """
    return os.getpid()



def run_interactive_command(command):
    # Run the 'top' command with the specified PID
    process = pexpect.spawn(command)

    # Wait for the 'top' process to start and print output until it's time to send "Enter"
    process.expect('\n')

    # Send "Enter" key press to the subprocess
    process.send('\r')

    # Capture output
    output = process.read().decode('utf-8')

    # Return the captured output
    return output

def getKey(config):
    return config.get('options', {}).get('k')

def getServerUrl(config):
    return config.get('options', {}).get('s')