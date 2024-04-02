import subprocess

#Developer github
github_username = "Sathya-github-del"

def create_adb_instance():
    return subprocess.Popen(['adb', 'shell'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_connected_device():
    devices_output = subprocess.check_output(['adb', 'devices']).decode().split('\n')
    for device in devices_output[1:]:
        if device.strip():
            return device.split('\t')[0]
    return None

def backup_partition(device_id, partition_name, output_file, partition_number):
    if device_id:
        subprocess.call(['adb', '-s', device_id, 'shell', 'su', '-c', 'dd', 'if=' + partition_name, 'of=' + output_file])
        print(f"{partition_number}. Backup of {partition_name} saved to {output_file}")
    else:
        print("No device connected.")

def backup_cache_partition(device_id):
    cache_partition = get_cache_partition_path(device_id)
    if cache_partition:
        # Backup cache partition
        backup_cache = input("Do you want to backup cache partition? (y/n): ")
        if backup_cache.lower() == 'y':
            backup_partition(device_id, cache_partition, '/sdcard/cache.img', "4")
        print("Cache partition backed up successfully.")
    else:
        print("Cache partition not found.")

def get_cache_partition_path(device_id):
    if device_id:
        # Execute 'ls -al /dev/block/by-name' command to fetch cache partition path
        output = subprocess.check_output(['adb', '-s', device_id, 'shell', 'ls', '-al', '/dev/block/by-name']).decode()
        lines = output.split('\n')
        cache_partition = None
        for line in lines:
            if 'cache' in line:
                cache_partition = line.split()[-1]
        return cache_partition
    else:
        return None

def backup_boot_recovery_img(device_id):
    boot_partition, recovery_partition = get_partition_paths(device_id)
    if boot_partition and recovery_partition:
        # Backup boot.img
        backup_boot = input("Do you want to backup boot partition? (y/n): ")
        if backup_boot.lower() == 'y':
            backup_partition(device_id, boot_partition, '/sdcard/boot.img', "1")
        
        # Backup recovery.img
        backup_recovery = input("Do you want to backup recovery partition? (y/n): ")
        if backup_recovery.lower() == 'y':
            backup_partition(device_id, recovery_partition, '/sdcard/recovery.img', "2")

        # Backup cache.img
        backup_cache_partition(device_id)

        # Find super.img partition
        super_partition_path = find_super_partition(device_id)

        # Backup super.img
        backup_super = input("Do you want to backup super partition? (y/n): ")
        if backup_super.lower() == 'y' and super_partition_path:
            backup_partition(device_id, super_partition_path, '/sdcard/super.img', "3")

        print("Images backed up successfully.")
    else:
        print("Failed to fetch partition paths.")  

def get_partition_paths(device_id):
    if device_id:
        # Execute 'ls -al /dev/block/by-name' command to fetch partition paths
        output = subprocess.check_output(['adb', '-s', device_id, 'shell', 'ls', '-al', '/dev/block/by-name']).decode()
        lines = output.split('\n')
        boot_partition = None
        recovery_partition = None
        for line in lines:
            if 'boot' in line:
                boot_partition = line.split()[-1]
            elif 'recovery' in line:
                recovery_partition = line.split()[-1]
        return boot_partition, recovery_partition
    else:
        return None, None

def find_super_partition(device_id):
    if device_id:
        # Execute 'ls -al /dev/block/by-name' command to find super partition
        output = subprocess.check_output(['adb', '-s', device_id, 'shell', 'ls', '-al', '/dev/block/by-name']).decode()
        lines = output.split('\n')
        super_partition = None
        for line in lines:
            if 'super' in line:
                super_partition = line.split()[-1]
                break
        return super_partition
    else:
        return None


def print_github_username():
    print(f"This project was made by {github_username}")


device_id = get_connected_device()

if device_id:
    backup_boot_recovery_img(device_id)
    print_github_username()  
else:
    print("No device connected.")

