# Configuration Guide for Cisco Devices Using Python
In this practice, we will demonstrate how to configure Cisco devices (switches and routers) using Python. We will use the telnetlib library (available here: https://docs.python.org/es/3.8/library/telnetlib.html) to automate the configuration of 4 Cisco switches (3 Layer 2 switches and 1 Layer 3 switch). The goal is to make the network scalable by configuring the following protocols:

    DTP (Dynamic Trunking Protocol)

    SVI (Switch Virtual Interface)

    EtherChannel

    Telnet

At the end of the configuration, you should be able to perform end-to-end ping tests.
## 1. Basic Configuration
### a) Configure each device in the network according to the topology name.
```bash
# Set hostname
hostname <hostname>

# Set enable password
enable password <password>
```
### b) VLAN Configuration
```bash
# Create VLANs
vlan <vlan_id>
 name <vlan_name>
 ```
## 2. Switch Link Configuration
### a) Assign VLANs to switch ports and configure Access Mode on switches S0 and S1.
```bash
# Configure Access Mode
interface <interface_id>
 switchport mode access
 switchport access vlan <vlan_id>
```
Configure the ports where the host is connected in Access Mode.
 ![imagen](https://github.com/user-attachments/assets/b8a33266-4818-460c-8ae2-6b30b1d4c2bb)
```bash
```
### b) Configure DTP on [device names].
Configure the ports that connect to each other in the desired dynamic mode.
 ![imagen](https://github.com/user-attachments/assets/2d182579-2e81-416e-997d-9d4222ff92a8)
```bash
# Configure DTP
interface <interface_id>
 switchport mode dynamic desirable
```
## 3. SVI Configuration
### a) Configure FastEthernet 0/1 interfaces as routed ports and assign IPs according to the routing table.
```bash
# Configure routed port
interface FastEthernet0/1
 no switchport
 ip address <ip_address> <subnet_mask>
```
### b) Configure gateways for each VLAN.

 ![imagen](https://github.com/user-attachments/assets/caaab837-eafd-4efe-8772-aefe2a94004c)
```bash
# Configure VLAN gateway
interface Vlan<vlan_id>
 ip address <ip_address> <subnet_mask>
```
## 4. Telnet Configuration
Enable Telnet access on the devices.
```bash
# Enable Telnet
line vty 0 4
 password <telnet_password>
 login
 transport input telnet
```

## 5. DHCP Configuration
Configure DHCP for VLANs.
```bash
# Configure DHCP
ip dhcp pool <pool_name>
 network <network_address> <subnet_mask>
 default-router <gateway_ip>
 dns-server <dns_server_ip>
```

## 6. Python Script for Automation
Below is an example Python script using the telnetlib library to automate the configuration of a Cisco switch.
Advanced version in the file named **"Automatization.py"**
```bash
import telnetlib

# Define device connection details
host = "192.168.1.1"
user = "admin"
password = "cisco"
enable_password = "enablepass"

# Connect to the device
tn = telnetlib.Telnet(host)

# Login to the device
tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")

# Enter enable mode
tn.write(b"enable\n")
tn.read_until(b"Password: ")
tn.write(enable_password.encode('ascii') + b"\n")

# Send configuration commands
commands = [
    "hostname Switch1",
    "vlan 10",
    "name Sales",
    "interface FastEthernet0/1",
    "switchport mode access",
    "switchport access vlan 10",
    "interface Vlan10",
    "ip address 192.168.10.1 255.255.255.0",
    "line vty 0 4",
    "password telnetpass",
    "login",
    "transport input telnet",
    "exit"
]

for cmd in commands:
    tn.write(cmd.encode('ascii') + b"\n")

# Save configuration
tn.write(b"write memory\n")

# Close the connection
tn.write(b"exit\n")
print(tn.read_all().decode('ascii'))
```
