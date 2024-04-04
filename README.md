# Backup Partitions

This Python script allows you to backup specific partitions from your Android device. It currently supports backing up the following partitions:
- Boot
- Recovery
- Super
- Cache

## Requirements
- Rooted Android device
- ADB drivers installed
- USB cable
- Python installed(Version:- 3+)

## Usage
1. Connect your rooted Android device to your computer using a USB cable.
2. Open a terminal and navigate to the directory containing the `backup.py` file.
3. Run the following command:
    ```
    sudo python3 backup.py
    ```
4. Follow the on-screen instructions to choose which partitions you want to backup.
5. All files will backup to /sdcard/ (Internal storage)

**Note:** Make sure your device is connected properly and recognized by ADB.

## License

This project is created by @Sathya-github-del.

