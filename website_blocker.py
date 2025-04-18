import tkinter as tk
from tkinter import messagebox
import os
import platform
import subprocess

# Hosts file and redirect IP
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT = "127.0.0.1"

def clean_domain(site):
    return site.replace("https://", "").replace("http://", "").strip().split("/")[0]

def flush_dns():
    try:
        subprocess.run(["ipconfig", "/flushdns"], check=True, shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to flush DNS: {e}")

def block_websites():
    sites = text_area.get("1.0", tk.END).strip().splitlines()
    try:
        with open(HOSTS_PATH, 'r+') as file:
            content = file.read()
            for site in sites:
                clean_site = clean_domain(site)
                entry = f"{REDIRECT} {clean_site}\n"
                if clean_site and entry not in content:
                    file.write(entry)
        flush_dns()
        messagebox.showinfo("Success", "Websites Blocked Successfully!")
    except PermissionError:
        messagebox.showerror("Error", "Please run this app as administrator.")

def unblock_websites():
    sites = text_area.get("1.0", tk.END).strip().splitlines()
    try:
        with open(HOSTS_PATH, 'r') as file:
            lines = file.readlines()
        with open(HOSTS_PATH, 'w') as file:
            for line in lines:
                if not any(clean_domain(site) in line for site in sites):
                    file.write(line)
        flush_dns()
        messagebox.showinfo("Success", "Websites Unblocked Successfully!")
    except PermissionError:
        messagebox.showerror("Error", "Please run this app as administrator.")

# GUI
app = tk.Tk()
app.title("Website Blocker")
app.geometry("420x300")

label = tk.Label(app, text="Enter websites (one per line):")
label.pack(pady=5)

text_area = tk.Text(app, height=10)
text_area.pack(pady=5)

block_btn = tk.Button(app, text="Block Websites", command=block_websites)
block_btn.pack(pady=5)

unblock_btn = tk.Button(app, text="Unblock Websites", command=unblock_websites)
unblock_btn.pack(pady=5)

app.mainloop()
