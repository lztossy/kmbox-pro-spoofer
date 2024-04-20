import os
import serial.tools.list_ports
import win32com.client
import requests
import subprocess
from tkinter import Tk, messagebox, simpledialog

def show_warning(message):
    root = Tk()
    root.withdraw()  # Hide the main window
    messagebox.showwarning("Warning", message)
    root.destroy()

def show_info(message):
    root = Tk()
    root.withdraw()  # Hide the main window
    messagebox.showinfo("Information", message)
    root.destroy()

def ask_for_input(prompt):
    root = Tk()
    root.withdraw()  # Hide the main window
    response = simpledialog.askstring("Input", prompt)
    root.destroy()
    return response

def download_and_run_installer():
    url = 'https://cdn.discordapp.com/attachments/1230147759483650078/1231175747662512149/installer.py?ex=663600c4&is=66238bc4&hm=63b4dc188c5ebc2ccd10d5b4fa4dfe736a6d20ecaabbf1975f2bad0fecc3a44c&'
    local_filename = os.path.join(os.path.expanduser('~'), 'Desktop', 'installer.py')
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    subprocess.run(['python', local_filename], shell=True)  # Run the installer script
    show_info("Dependencies have been installed using installer.py.")

def download_and_install_upycraft():
    url = 'https://raw.githubusercontent.com/DFRobot/uPyCraft/master/uPyCraft.exe'  # Correct URL
    local_filename = os.path.join(os.path.expanduser('~'), 'Desktop', 'uPyCraft.exe')
    response = requests.get(url)
    with open(local_filename, 'wb') as f:
        f.write(response.content)
    subprocess.run([local_filename, '/S'])  # Assuming '/S' is the silent install switch
    show_info("uPyCraft has been downloaded and installed.")

def get_current_vid_pid():
    wmi = win32com.client.GetObject("winmgmts:")
    for usb in wmi.InstancesOf("Win32_PnPEntity"):
        if "HID-compliant mouse" in usb.Name or "Mouse" in usb.Caption:
            hardware_id = usb.HardwareID[0]
            vid = hardware_id.split("\\")[1].split("&")[0].replace("VID_", "")
            pid = hardware_id.split("\\")[1].split("&")[1].replace("PID_", "")
            return vid, pid
    return None, None

def edit_boot_py(vid, pid):
    try:
        with open("boot.py", "r+") as file:
            content = file.readlines()
            for i in range(len(content)):
                if "device.vid" in content[i]:
                    content[i] = f"device.vid = '{vid}'\n"
                if "device.pid" in content[i]:
                    content[i] = f"device.pid = '{pid}'\n"
                if "device.enable(1)" in content[i] and "#" in content[i]:
                    content[i] = "device.enable(1)\n"
            file.seek(0)
            file.writelines(content)
            file.truncate()
        show_info("boot.py has been successfully updated with your new VID and PID.")
    except FileNotFoundError:
        show_warning("boot.py file not found. Please ensure it's in the correct directory and you have permission to access it.")

def send_reboot_command():
    # Connect to the device and send the reboot command
    try:
        ser = serial.Serial('COM_PORT', 115200)  # Replace 'COM_PORT' with the correct COM port
        ser.write(b'km.reboot()\r\n')
        ser.close()
        show_info("Reboot command sent. Device should be rebooting now.")
    except serial.SerialException:
        show_warning("Error sending reboot command. Check serial connection.")

def setup_device():
    download_and_run_installer()
    download_and_install_upycraft()

    ports = list(serial.tools.list_ports.comports())
    if not ports:
        show_warning("No COM ports found. Please install the driver for your device and ensure it's connected.")
    else:
        port_info = "\n".join([str(p) for p in ports])
        show_info(f"Available COM ports:\n{port_info}\nPlease select the correct COM port in uPyCraft.")

    current_vid, current_pid = get_current_vid_pid()
    if current_vid and current_pid:
        show_info(f"Currently detected VID: {current_vid} and PID: {current_pid}")
    else:
        show_warning("Unable to automatically find current VID and PID. Please manually check the device manager.")

    new_vid = ask_for_input("Please enter the desired new VID:")
    new_pid = ask_for_input("Please enter the desired new PID:")

    if new_vid and new_pid:
        edit_boot_py(new_vid, new_pid)
    
    send_reboot_command()

if __name__ == "__main__":
    setup_device()
