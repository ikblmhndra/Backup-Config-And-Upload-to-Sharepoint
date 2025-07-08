
---

## BACKUP-CONFIG-AND-UPLOAD-TO-SHAREPOINT

  

_Secure, Automate, Empower Your Network Resilience_

  

![last-commit](https://img.shields.io/github/last-commit/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?style=flat&logo=git&logoColor=white&color=0080ff)  ![repo-top-language](https://img.shields.io/github/languages/top/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?style=flat&color=0080ff)  ![repo-language-count](https://img.shields.io/github/languages/count/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?style=flat&color=0080ff)

  

_Built with the tools and technologies:_

  

![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)

  

  

___

  

## Table of Contents

  

- [Overview](https://github.com/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?tab=readme-ov-file#overview)

- [Getting Started](https://github.com/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?tab=readme-ov-file#getting-started)

- [Prerequisites](https://github.com/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?tab=readme-ov-file#prerequisites)

- [Installation](https://github.com/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint?tab=readme-ov-file#installation)

  
  

___

  

## Overview

  

Backup-Config-And-Upload-to-Sharepoint is a powerful automation tool that orchestrates the backup, secure storage, and management of firewall configurations across multiple device types, including Fortinet and Palo Alto. It ensures reliable, hands-free operations with integrated authentication, network diagnostics, and real-time notifications.

  

**Why Backup-Config-And-Upload-to-Sharepoint?**

  

This project aims to simplify and automate the complex processes of network configuration management. The core features include:

  

- **🛠️ Automated Backup & Upload:** Seamlessly download firewall configs and upload them securely to SharePoint.

- **🔒 Secure Authentication:** Manage session-based and token-based authentication for Fortinet and Palo Alto devices.

- **🌐 Network Diagnostics:** Verify device connectivity and troubleshoot network issues proactively.

- **📢 Real-time Notifications:** Keep your team informed with Telegram alerts on backup status and errors.

- **🗂️ Centralized Configuration Management:** Handle environment variables and device settings efficiently.

- **🤖 Error Handling & Resilience:** Gracefully manage failures and ensure continuous operation.

  

___

  

## Getting Started

### **1. `config_manager.py`**

  

- Handles environment variables and configuration

- Functions: `load_environment()`, `get_constants()`, `get_device_config()`, `update_env_token()`

  

### **2. `palo_alto_auth.py`**

  

- Manages Palo Alto firewall authentication

- Functions: `check_token_valid_pa()`, `regenerate_token_pa()`, `handle_palo_alto_auth()`

  

### **3. `fortinet_auth.py`**

  

- Handles Fortinet firewall session management

- Functions: `save_session()`, `load_session()`, `is_session_valid_fortinet()`, `regenerate_session_fortinet()`, `handle_fortinet_auth()`

  

### **4. `backup_operations.py`**

  

- Manages configuration downloads and file operations

- Functions: `download_config()`, `create_backup_directory()`, `generate_filename()`, `save_config_to_file()`

  

### **5. `sharepoint_uploader.py`**

  

- Handles SharePoint file uploads

- Functions: `get_sharepoint_credentials()`, `authenticate_sharepoint()`, `upload_file_to_sharepoint()`, `upload_to_sharepoint()`

  

### **6. `notification_service.py`**

  

- Manages Telegram notifications

- Functions: `send_telegram_notification()`, `create_failure_message()`, `create_success_message()`, `send_failure_notification()`, `send_success_notification()`

  

### **7. `network_utils.py`**

  

- Network connectivity utilities

- Functions: `check_device_connectivity()`, `check_multiple_devices()`, `is_device_online()`, `get_device_response_time()`, `validate_ip_address()`

  

### **8. `main.py`**

  

- Main orchestration script

- Functions: `process_single_firewall()`, `run_backup_process()`, `main()`

  

## **Key Benefits of This Structure:**

  

### **Modularity:**

  

- Each module has a single responsibility

- Easy to maintain and test individual components

- Clear separation of concerns

  

### **Reusability:**

  

- Functions can be imported and used in other projects

- Each module can be used independently

  

### **Maintainability:**

  

- Easy to locate and fix issues

- Simple to add new features or device types

- Clear documentation for each module

  

### **Testability:**

  

- Each module can be unit tested separately

- Mock dependencies easily for testing

  

### Prerequisites

  

This project requires the following dependencies:

  

- **Programming Language:** Python

- **Package Manager:** Conda

  

### Installation

  

Build Backup-Config-And-Upload-to-Sharepoint from the source and install dependencies:

  

1. **Clone the repository:**

```sh

❯ git clone https://github.com/ikblmhndra/Backup-Config-And-Upload-to-Sharepoint

```

2. **Navigate to the project directory:**

```sh

❯ cd Backup-Config-And-Upload-to-Sharepoint

```

3. **Install the dependencies:**

```sh

❯ pip3 install -r requirements.txt

```