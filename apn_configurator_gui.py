import tkinter as tk
import subprocess
from tkinter import messagebox

def create_or_modify_mobile_broadband_profile(profile_name, apn, ip_type, username, password, authentication):
    # Check if the profile already exists
    result = subprocess.run(["nmcli", "-t", "-f", "NAME", "c", "show"], capture_output=True, text=True)
    existing_profiles = result.stdout.splitlines()
    if profile_name in existing_profiles:
        # Display alert window for confirmation
        response = messagebox.askyesno("Profile Exists", "The profile already exists. Do you want to modify it?")

        if response:

            # Modify the existing profile
            subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.apn", apn])
            subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.username", username])
            subprocess.run(["nmcli", "c", "modify", profile_name, "gsm.password", password])
            output_text.insert(tk.END, "Mobile broadband profile modified successfully.")

        else:
            output_text.insert(tk.END, "Modification of the existing profile canceled.")
            return

    else:
        # Create a new profile
        subprocess.run(["nmcli", "c", "add", "type", "gsm", "ifname", "none", "con-name", profile_name])
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


    # Bring up the mobile broadband connection
    result = subprocess.run(["nmcli", "con", "up", profile_name], capture_output=True, text=True)
    if result==0:
        print("Mobile broadband connection is up.")
    else: 
        print("Mobile broadband connection is not up. Either modem is not detected or driver is not up")

    output_text.insert(tk.END, result.stdout)
    output_text.insert(tk.END, result.stderr)


def mmcli_port_checker():
    mmcli_port_check = subprocess.check_output(['mmcli', '-L']).decode('utf-8')
    mmcli_port = mmcli_port_check.rfind("/")
    mmcli_port_number = mmcli_port_check[mmcli_port + 1:].strip()
    port = mmcli_port_number.split()
    return port[0]	

def send_at_command():
    #filling variables from textbox
    profile_name = profile_entry.get()
    apn_name = apn_entry.get()
    ip_type = ip_entry.get()
    auth_type = auth_entry.get()
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

    #setting values in Network manager and calling connect
    create_or_modify_mobile_broadband_profile(profile_name, apn_name, ip_type, user_name, password, auth_type)



window = tk.Tk()
window.title("APN Setter GUI")

# Adjusting the window size and position
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 650
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
apn_lbl = tk.Label(text='Access point name', font=('Arial', 12))
apn_lbl.pack()
apn_entry = tk.Entry(window, width=50, font=('Arial', 12))
apn_entry.pack(pady=6)

# Create the IP type entry field
ip_lbl = tk.Label(text='IP TYPE (IPV4, IPV6 or IPV4V6)', font=('Arial', 12))
ip_lbl.pack()
ip_entry = tk.Entry(window, width=50, font=('Arial', 12))
ip_entry.pack(pady=6)

# Create the Authentication entry field
auth_lbl = tk.Label(text='Authentication (CHAP, PAP or CHAP/PAP)', font=('Arial', 12))
auth_lbl.pack()
auth_entry = tk.Entry(window, width=50, font=('Arial', 12))
auth_entry.pack(pady=6)

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


button = tk.Button(window, text="Set APN and Connect", font=('Arial', 12), width=20, bg='#ffffff', activebackground='#00ff00', command=send_at_command)
button.pack(pady=15)

exit_button = tk.Button(window, text = "Quit", font=('Arial', 12), width=20, bg='#ffffff', activebackground='red',
            command = window.destroy)
exit_button.pack(pady=15)

# Create the output text box
output_text = tk.Text(window)
output_text.config(bg='#A67449')
output_text.pack(pady=15)

output_text.insert(tk.END, "Please Enter APN details in the text box")

window.mainloop()
