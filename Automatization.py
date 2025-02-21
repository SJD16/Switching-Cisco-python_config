import getpass
import telnetlib

# List of IPs for each switch
HOST = ["10.4.10.2", "10.10.10.5", "172.1.0.1"]

# List of usernames for each switch
USER = ["switch1", "switch2", "switch3"]

# Passwords for Telnet and Enable mode
TELNET_PASSWORD = b"1234"
ENABLE_PASSWORD = b"1234"

# Port ranges for EtherChannel configuration
# Each switch has a specific range of ports for EtherChannel
RANGE_INTERFACE = [
    [b"23-24"],  # Switch 1
    [b"20-21", b"22-23"],  # Switch 2
    [b"23-24"]  # Switch 3
]

# Function to configure EtherChannel for a given port range
def INTCONFIG(i, j):
    tn.write(b"interface range fa0/" + RANGE_INTERFACE[i][j - 1] + b"\n")
    tn.write(b"switchport mode dynamic desirable\n")
    tn.write(b"channel-group " + bytes(str(j), 'ascii') + b" mode desirable\n")  # PAGP desirable
    tn.write(b"do show etherchannel summary\n")
    tn.write(b"interface port-channel " + bytes(str(j), 'ascii') + b"\n")
    tn.write(b"switchport mode dynamic desirable\n")
    tn.write(b"exit\n")
    tn.write(b"do show etherchannel summary\n")

# Main loop to configure each switch
for i in range(len(HOST)):
    print(":+++++++:\n CONNECTING TO " + HOST[i] + "\n:+++++++:")

    # Connect to the device via Telnet
    tn = telnetlib.Telnet(HOST[i])

    # Login to the device
    tn.read_until(b"Username: ")
    tn.write(USER[i].encode('ascii') + b"\n")
    tn.read_until(b"Password: ")
    tn.write(TELNET_PASSWORD + b"\n")

    # Enter privileged EXEC mode
    tn.write(b"enable\n")
    tn.read_until(b"Password: ")
    tn.write(ENABLE_PASSWORD + b"\n")

    # Enter global configuration mode
    tn.write(b"configure terminal\n")

    # Configure EtherChannel based on the switch
    if len(RANGE_INTERFACE[i]) == 2:  # Switch 2 has two EtherChannels
        INTCONFIG(i, 1)
        INTCONFIG(i, 2)
    else:  # Other switches have one EtherChannel
        INTCONFIG(i, 1)

    # Exit to privileged EXEC mode
    tn.write(b"end\n")

    # Save the configuration
    tn.write(b"write memory\n")

    # Close the Telnet session
    tn.write(b"exit\n")
    print(tn.read_all().decode('ascii'))