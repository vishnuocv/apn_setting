import subprocess
import tkinter as tk

def send_at_command():
    apn_name = apn_entry.get()
    ip_type = ip_entry.get()
    auth_type = auth_entry.get()
    user_name = user_entry.get()
    password = pass_entry.get()
    command = '--3gpp-set-initial-eps-bearer-settings=apn=' + apn_name + ',ip-type=' + ip_type + ',allowed-auth=' + auth_type + ',user=' + user_name + ',password=' + password
    print (command)
    result = subprocess.run(['mmcli', '-m', '0', command], capture_output=True, text=True)
    output_text.delete('1.0', tk.END)  # Clear previous output
    output_text.insert(tk.END, result.stdout)
    output_text.insert(tk.END, command)
    output_text.insert(tk.END, result.stderr)

# Create the main window
window = tk.Tk()
window.config(bg='#84BF04')
window.minsize(600,400)
window.title("Internet/Attach APN setter")

# Create the AT command entry field
apn_lbl = tk.Label(text='APN')
apn_lbl.place(x=210, y=3)
apn_entry = tk.Entry(window)
apn_entry.pack()

# Create the AT command entry field
ip_lbl = tk.Label(text='IP TYPE')
ip_lbl.place(x=190, y=23)
ip_entry = tk.Entry(window)
ip_entry.pack()

# Create the AT command entry field
auth_lbl = tk.Label(text='Authentication')
auth_lbl.place(x=130, y=48)
auth_entry = tk.Entry(window)
auth_entry.pack()

# Create the AT command entry field
user_lbl = tk.Label(text='User name')
user_lbl.place(x=160, y=69)
user_entry = tk.Entry(window)
user_entry.pack()

# Create the AT command entry field
pass_lbl = tk.Label(text='Password')
pass_lbl.place(x=160, y=90)
pass_entry = tk.Entry(window)
pass_entry.pack()


# Create the "Send" button
send_button = tk.Button(window, text="Set", command=send_at_command)
send_button.pack()

exit_button = tk.Button(window, text = "Exit",
            command = window.destroy)
exit_button.pack()

# Create the output text box
output_text = tk.Text(window)
output_text.config(bg='#A67449')
output_text.pack()

# Run the application
window.mainloop()

