import threading
import time
from .thread_profiler import capture_export_thread_data
from .process_profiler import capture_print_process_details
from .mem_profiler import ycrash_memory_extract, profile_all_methods
import yaml


def init(configFilePath):
    thread_states_thread = threading.Thread(target=profile_data, args=(configFilePath,), name="yCrash.analyzer")
    thread_states_thread.start()


def profile_data(configFilePath):
    ycrashConfig = load_config(configFilePath)
    profile_all_methods()

    while True:
        capture_export_thread_data(configFilePath,ycrashConfig)
        capture_print_process_details(ycrashConfig)
        ycrash_memory_extract(ycrashConfig)
        time.sleep(ycrashConfig.get('options', {}).get('m3Frequency'))


def load_config(configFilePath):
    # Read the YAML file
    with open(configFilePath, 'r') as file:
        print(file)
        data = yaml.safe_load(file)
        global_config_data = data

    # Accessing attributes
    version = data.get('version')
    options = data.get('options', {})

    # Accessing specific attributes within options
    k = options.get('k')
    s = options.get('s')
    a = options.get('a')
    m3Frequency = options.get('m3Frequency')
    app_logs = options.get('appLogs', [])

    # Outputting the values
    print("Version:", version)
    print("k:", k)
    print("s:", s)
    print("a:", a)
    print("m3Frequency:", m3Frequency)
    print("App Logs:")
    for log_path in app_logs:
        print("  -", log_path)
    file.close()

    return data




