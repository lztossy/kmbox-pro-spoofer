# KMBox Spoof Automation Tool

This repository contains a Python script (`automate.py`) designed to automate the setup and configuration of devices using uPyCraft and specific hardware interaction for updating device settings like VID and PID. The script also handles dependency management by downloading and executing an installer script.

## Features

- Automatically downloads and installs uPyCraft.
- Automatically downloads and executes an installer script for managing Python dependencies.
- Configures device settings by updating `boot.py` with user-provided VID and PID.
- Sends a reboot command to the device via serial connection to apply new configurations.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Windows 10 or newer.
- Python 3.11 or newer installed on your system.
- Internet connection to download necessary files and dependencies.

## Installation

Clone this repository to your local machine using:

```bash
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
