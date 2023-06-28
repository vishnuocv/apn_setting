import tkinter as tk
import subprocess

def mmcli_port_checker():
    mmcli_port_check = subprocess.check_output(['mmcli', '-L']).decode('utf-8')
    mmcli_port = mmcli_port_check.rfind("/")
    mmcli_port_number = mmcli_port_check[mmcli_port + 1:].strip()
    port = mmcli_port_number.split()
    return port[0]	

def send_at_command():
    apn_name = apn_entry.get()
    ip_type = ip_entry.get()
    auth_type = auth_entry.get()
    user_name = user_entry.get()
    password = pass_entry.get()
    command = '--3gpp-set-initial-eps-bearer-settings=apn=' + apn_name + ',ip-type=' + ip_type + ',allowed-auth=' + auth_type + ',user=' + user_name + ',password=' + password
    port_number = mmcli_port_checker()
    output_text.delete('1.0', tk.END)  # Clear previous output
    output_text.insert(tk.END, "Port detected is " + port_number + '\n')
    result = subprocess.run(['mmcli', '-m', port_number, command], capture_output=True, text=True)
    output_text.insert(tk.END, result.stdout)
    output_text.insert(tk.END, result.stderr)

window = tk.Tk()
window.title("APN Setter GUI")

# Adjusting the window size and position
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 650
window_height = 600
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

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

button = tk.Button(window, text="Set APN", font=('Arial', 12), width=20, bg='#ffffff', activebackground='#00ff00', command=send_at_command)
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
