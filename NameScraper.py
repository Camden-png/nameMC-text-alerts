import os
import sys
import time
import smtplib
import platform

try:
    import requests
except ImportError:
    print("Error: no Requests library found!")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: no BeautifulSoup library found!")
    sys.exit(1)

wait = 1
old = ""
list = []

def clear():
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")

def main():
    clear()
    global wait
    global list
    try:
        value = int(sys.argv[1])
        if value > 0: wait = value
    except: pass
    try:
        file = open("Names.txt", "r")
    except:
        print("Error: no Names.txt found!")
        return 1
    string = file.read()
    file.close()
    if not string:
        print("Error: Names.txt is empty!")
        return 1
    for line in string.split("\n"):
        line = "".join(line.split())
        if line: list.append(line)
    if len(list) <= 3:
        print("Error: no usernames found!")
        return 1
    print("Running...")
    return 0

def loop():
    global old
    global list
    string = ""
    namemc = "https://namemc.com/search?q="
    for name in list[0:-3]:
        try:
            page = requests.get(namemc + name)
            soup = BeautifulSoup(page.content, "html.parser")
            item = str(soup.find_all("div", class_="col-sm-6 my-1"))
            if "Available" in item: string += name + ", "
        except: return 1
    if string: string = string[0:-2]
    if string != old:
        old = string
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls(); server.login(list[-3], list[-2])
            message = "From: %s\r\n" % list[-3] + "To: %s\r\n" % list[-1] + "Subject: %s\r\n" % "" + "\r\n" + "Names: " + string
            server.sendmail(list[-3], list[-1], message)
        except:
            print("Error: no login information found!")
            return 1
    print("Updated...")
    return 0

if main() == 0:
    while True:
        try:
            delay = 60 * wait
            if loop() == 1: sys.exit(1)
            time.sleep(delay - time.time() % delay)
        except KeyboardInterrupt:
            clear(); sys.exit(0)
