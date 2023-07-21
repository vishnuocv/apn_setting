import os
import stat
import tkinter as tk
import subprocess
from tkinter import messagebox

# Global variables for authentication and IP type
authentication = ""
ip_type = ""

def switch_on_mobile_broadband():
    subprocess.run(["nmcli", "radio", "wwan", "on"])

def refresh_network_manager_settings():
    subprocess.run(["nmcli", "connection", "reload"])

def restart_network_manager():
    subprocess.run(["sudo", "systemctl", "restart", "NetworkManager"])

# Function to create or modify the mobile broadband profile
def create_or_modify_mobile_broadband_profile_nm(profile_name, apn, ip_type, username, password, authentication):

    # Create a new connection profile file
    connection_file_path = f"/etc/NetworkManager/system-connections/{profile_name}"
    with open(connection_file_path, 'w') as connection_file:
        connection_file.write("[connection]\n")
        connection_file.write("id=" + profile_name + "\n")
        connection_file.write("type=gsm\n")
        connection_file.write("autoconnect=true\n")
        connection_file.write("\n")
        connection_file.write("[gsm]\n")
        connection_file.write("apn=" + apn + "\n")
        connection_file.write("username=" + username + "\n")
        connection_file.write("password=" + password + "\n")
        connection_file.write("ip-type=" + ip_type + "\n")
        connection_file.write("allowed-auth=" + authentication + "\n")

    # Set the correct permissions on the connection file
    os.chmod(connection_file_path, stat.S_IRUSR | stat.S_IWUSR)

    # Refresh Network Manager settings
    refresh_network_manager_settings()
    print("Network Manager settings refreshed.")

    restart_network_manager()
    print("Network Manager restarted.")

    # Switch on the mobile broadband connection
    switch_on_mobile_broadband()
    print("Mobile broadband is switched on.")

def on_checkbox_change():
    global authentication, ip_type

    ip_type = ""
    if ipv4_var.get() and ipv6_var.get():
        ip_type = "IPV4V6"
    elif ipv4_var.get():
        ip_type = "IPV4"
    elif ipv6_var.get():
        ip_type = "IPV6"

    authentication = ""
    if pap_var.get() and chap_var.get():
        authentication = "PAP/CHAP"
    else:
        if pap_var.get():
            authentication = "PAP"
        if chap_var.get():
            if authentication:
                authentication += "/"
            authentication += "CHAP"
            
def modify_mobile_broadband_profile(profile_name, apn, ip_type, username, password, authentication):

    subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.apn", apn])
    subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.username", username])
    subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.password", password])
    output_text.insert(tk.END, "Mobile broadband profile created successfully.")

    # Configure authentication options based on the selected method

    if authentication.lower() in ["pap"]:
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-eap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-chap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschapv2", "yes"])
    elif authentication.lower() in ["chap"]:
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-eap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-pap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschapv2", "yes"])
    elif authentication.lower() in ["pap/chap", "chap/pap"]:
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-eap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-chap", "no"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-pap", "no"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschap", "yes"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ppp.refuse-mschapv2", "yes"])

    # Configure IP type options
    if ip_type.lower() == "ipv4":
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv4.method", "auto"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv6.method", "disabled"])
    elif ip_type.lower() == "ipv6":
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv4.method", "disabled"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv6.method", "auto"])
    elif ip_type.lower() == "ipv4v6":
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv4.method", "auto"])
        subprocess.run(["nmcli", "c", "modify", profile_name, "ipv6.method", "auto"])

def mmcli_port_checker():
    mmcli_port_check = subprocess.check_output(['mmcli', '-L']).decode('utf-8')
    mmcli_port = mmcli_port_check.rfind("/")
    mmcli_port_number = mmcli_port_check[mmcli_port + 1:].strip()
    port = mmcli_port_number.split()
    return port[0]	

def send_at_command():
    global authentication, ip_type
    #filling variables from textbox
    profile_name = profile_entry.get()
    apn_name = apn_entry.get()
    auth_type = authentication
    user_name = user_entry.get()
    password = pass_entry.get()

    #fixing the commands
    command = '--3gpp-set-initial-eps-bearer-settings=apn=' + apn_name + ',ip-type=' + ip_type + ',allowed-auth=' + auth_type + ',user=' + user_name + ',password=' + password

    #calling port checker function
    port_number = mmcli_port_checker()
    output_text.delete('1.0', tk.END)  # Clear previous output
    output_text.insert(tk.END, "Port detected is " + port_number + '\n')
    result = subprocess.run(['mmcli', '-m', port_number, command], capture_output=True, text=True)
    output_text.insert(tk.END, result.stdout)
    output_text.insert(tk.END, result.stderr)

    #setting values for Network manager GUI
    create_or_modify_mobile_broadband_profile_nm(profile_name, apn_name, ip_type, user_name, password, auth_type)

    #setting values in Network manager nmcli method
    modify_mobile_broadband_profile(profile_name, apn_name, ip_type, user_name, password, auth_type)


window = tk.Tk()
window.title("APN Configurator GUI")

# Adjusting the window size and position
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 700
window_height = 700
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Create the APN entry field
profile_lbl = tk.Label(text='Profile Name', font=('Arial', 12))
profile_lbl.pack()
profile_entry = tk.Entry(window, width=50, font=('Arial', 12))
profile_entry.pack(pady=6)

# Create the APN entry field
apn_lbl = tk.Label(text='Access point name (APN)', font=('Arial', 12))
apn_lbl.pack()
apn_entry = tk.Entry(window, width=50, font=('Arial', 12))
apn_entry.pack(pady=6)

# Create the IP type checkboxes
ipv4_var = tk.BooleanVar()
ipv4_checkbox = tk.Checkbutton(window, text="IPv4", variable=ipv4_var, font=('Arial', 12))
ipv4_checkbox.pack()

ipv6_var = tk.BooleanVar()
ipv6_checkbox = tk.Checkbutton(window, text="IPv6", variable=ipv6_var, font=('Arial', 12))
ipv6_checkbox.pack()

# Create the authentication checkboxes
pap_var = tk.BooleanVar()
pap_checkbox = tk.Checkbutton(window, text="PAP", variable=pap_var, font=('Arial', 12))
pap_checkbox.pack()

chap_var = tk.BooleanVar()
chap_checkbox = tk.Checkbutton(window, text="CHAP", variable=chap_var, font=('Arial', 12))
chap_checkbox.pack()

# Create the User name entry field
user_lbl = tk.Label(text='User name  (if any)', font=('Arial', 12))
user_lbl.pack()
user_entry = tk.Entry(window, width=50, font=('Arial', 12))
user_entry.pack(pady=6)

# Create the Password entry field
pass_lbl = tk.Label(text='Password (if any)', font=('Arial', 12))
pass_lbl.pack()
pass_entry = tk.Entry(window, width=50, font=('Arial', 12))
pass_entry.pack(pady=6)

ipv4_var.trace("w", lambda *args: on_checkbox_change())
ipv6_var.trace("w", lambda *args: on_checkbox_change())
pap_var.trace("w", lambda *args: on_checkbox_change())
chap_var.trace("w", lambda *args: on_checkbox_change())

button = tk.Button(window, text="Set APN / Connect", font=('Arial', 12), width=20, bg='#ffffff', activebackground='#00ff00', command=send_at_command)
button.pack(pady=15)

exit_button = tk.Button(window, text = "Exit", font=('Arial', 12), width=20, bg='#ffffff', activebackground='red',
            command = window.destroy)
exit_button.pack(pady=15)

# Create the output text box
output_text = tk.Text(window)
output_text.config(bg='#A67449')
output_text.pack(pady=15)

output_text.insert(tk.END, "Please Enter your APN details in the text box")

window.mainloop()
