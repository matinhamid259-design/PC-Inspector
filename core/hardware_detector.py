import platform
import socket
import os
import subprocess
import json
import winreg

try:
    import wmi
except ImportError:
    wmi = None


def safe_get(value, default="Unavailable"):
    return value if value not in (None, "", "Unknown") else default


def get_cpu_info():
    try:
        return {
            "manufacturer": safe_get(platform.processor()),
            "model": safe_get(platform.uname().processor or platform.machine()),
            "architecture": safe_get(platform.architecture()[0]),
            "cores": safe_get(os.cpu_count()),
            "threads": safe_get(os.cpu_count()),
            "frequency": "Unavailable",
        }
    except Exception:
        return {
            "manufacturer": "Unavailable",
            "model": "Unavailable",
            "architecture": "Unavailable",
            "cores": "Unavailable",
            "threads": "Unavailable",
            "frequency": "Unavailable",
        }


def get_ram_info():
    try:
        import psutil
        total = psutil.virtual_memory().total
        return {
            "total": total,
            "available": psutil.virtual_memory().available,
            "used": psutil.virtual_memory().used,
            "percent": psutil.virtual_memory().percent,
            "type": "Unavailable",
            "speed": "Unavailable",
        }
    except Exception:
        return {"total": "Unavailable", "available": "Unavailable", "used": "Unavailable", "percent": "Unavailable", "type": "Unavailable", "speed": "Unavailable"}


def get_gpu_info():
    try:
        if wmi:
            c = wmi.WMI()
            gpu = c.Win32_VideoController()[0]
            return {
                "name": safe_get(gpu.Name),
                "manufacturer": safe_get(gpu.AdapterCompatibility),
                "driver_version": safe_get(gpu.DriverVersion),
                "dedicated_memory": safe_get(gpu.AdapterRAM),
                "shared_memory": "Unavailable",
            }
    except Exception:
        pass
    return {"name": "Unavailable", "manufacturer": "Unavailable", "driver_version": "Unavailable", "dedicated_memory": "Unavailable", "shared_memory": "Unavailable"}


def get_motherboard_info():
    try:
        if wmi:
            c = wmi.WMI()
            board = c.Win32_BaseBoard()[0]
            return {"manufacturer": safe_get(board.Manufacturer), "model": safe_get(board.Product), "bios": safe_get(board.SerialNumber)}
    except Exception:
        pass
    return {"manufacturer": "Unavailable", "model": "Unavailable", "bios": "Unavailable"}


def get_windows_details():
    return {
        "edition": safe_get(platform.win32_edition() if hasattr(platform, 'win32_edition') else "Unavailable"),
        "version": safe_get(platform.version()),
        "build": safe_get(platform.win32_ver()[1]),
        "architecture": safe_get(platform.architecture()[0]),
        "computer_name": safe_get(socket.gethostname()),
    }


def get_storage_devices():
    devices = []
    try:
        import psutil
        for part in psutil.disk_partitions(all=False):
            try:
                usage = psutil.disk_usage(part.mountpoint)
                devices.append({
                    "device": part.device,
                    "mountpoint": part.mountpoint,
                    "fstype": part.fstype or "Unknown",
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent,
                    "drive_type": "Unavailable"
                })
            except Exception:
                continue
    except Exception:
        return devices
    return devices


def get_installed_apps():
    apps = []
    try:
        if wmi:
            c = wmi.WMI()
            for app in c.Win32_Product():
                apps.append({
                    "name": safe_get(app.Name),
                    "publisher": safe_get(app.Vendor),
                    "version": safe_get(app.Version),
                    "location": safe_get(app.InstallLocation),
                    "install_date": safe_get(app.InstallDate),
                })
    except Exception:
        pass
    return apps


def get_startup_apps():
    return []
