import ctypes
from win32api import GetSystemMetrics
import psutil
import platform
import socket
import speedtest
import wmi
import subprocess

def get_installed_software():
    installed_software = subprocess.check_output(['wmic', 'product', 'get', 'name']).decode('utf-8').split('\n')[1:-1]
    return [software.strip() for software in installed_software]

def get_internet_speed():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # in Mbps
    upload_speed = st.upload() / 1_000_000  # in Mbps
    return download_speed, upload_speed

def get_screen_resolution():
    try:
        width = GetSystemMetrics(0)  # Get screen width
        height = GetSystemMetrics(1)  # Get screen height
        return f"{width}x{height}"
    except Exception as e:
        return "Not available"

def get_cpu_info():
    cpu_info = {}
    cpu_info['model'] = platform.processor()
    cpu_info['cores'] = psutil.cpu_count(logical=False)
    cpu_info['threads'] = psutil.cpu_count(logical=True)
    return cpu_info

def get_gpu_info():
    try:
        w = wmi.WMI()
        gpu_info = w.Win32_VideoController()[0].Caption
        return gpu_info
    except Exception as e:
        return None

def get_ram_size():
    ram_info = psutil.virtual_memory()
    return round(ram_info.total / (1024 ** 3), 2)  # Convert bytes to gigabytes

def get_screen_size():
    return "Not available"  # You may need an external library to accurately determine screen size

def get_network_info():
    interfaces = psutil.net_if_addrs()
    for interface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                if interface.lower() == 'wi-fi':
                    return f"Wi-Fi: {addr.address}"
                elif interface.lower() == 'ethernet':
                    return f"Ethernet: {addr.address}"
    return "Not available"

def get_public_ip():
    return subprocess.check_output(['curl', 'ifconfig.me']).decode('utf-8').strip()

def get_windows_version():
    return platform.version()

if __name__ == "__main__":
    print("Installed Software List:")
    for software in get_installed_software():
        print(software)

    download_speed, upload_speed = get_internet_speed()
    print(f"\nInternet Speed: Download Speed: {download_speed} Mbps, Upload Speed: {upload_speed} Mbps")

    print(f"\nScreen Resolution: {get_screen_resolution()}")

    cpu_info = get_cpu_info()
    print(f"\nCPU Model: {cpu_info['model']}")
    print(f"No. of Cores: {cpu_info['cores']}, No. of Threads: {cpu_info['threads']}")

    gpu_info = get_gpu_info()
    if gpu_info:
        print(f"\nGPU Model: {gpu_info}")
    else:
        print("\nGPU Model: Not available")

    print(f"\nRAM Size: {get_ram_size()} GB")

    print(f"\nScreen Size: {get_screen_size()}")

    print(f"\nNetwork Info: {get_network_info()}")

    print(f"\nPublic IP Address: {get_public_ip()}")

    print(f"\nWindows Version: {get_windows_version()}")
