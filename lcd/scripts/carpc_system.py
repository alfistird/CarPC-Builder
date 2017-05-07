#!/usr/bin/python

import telnetlib;
import time;
import os;
import statvfs;
import subprocess;

host='127.0.0.1';
port='13666';
data = ""


# init
tn = telnetlib.Telnet(host, port)
tn.write("hello\r");

# add screen for date and time
tn.write("screen_add SCREEN\n");
data += tn.read_until("\n");
tn.write("screen_set SCREEN -heartbeat on\n");
data += tn.read_until("\n");
tn.write("widget_add SCREEN 1 title\n");
data += tn.read_until("\n");
tn.write("widget_add SCREEN 2 string\n");
data += tn.read_until("\n");

# generate endless loop
loop = 1
while loop == 1 :

  cmd1 = "hostname -I | cut -d' ' -f1"
  process = subprocess.Popen(cmd1, stdout=subprocess.PIPE , shell=True)
  os.waitpid(process.pid, 0)[1]
  ip = process.stdout.read().strip()

  count = 1
  while count  <= 5 :

    #time date
    time.ctime();
    cur = time.strftime('%H:%M:%S Uhr')
    day = time.strftime('%u')
    if day == "1":
	day = "Mo"
    if day == "2":
	day = "Di"
    if day == "3":
	day = "Mi"
    if day == "4":
	day = "Do"
    if day == "5":
	day = "Fr"
    if day == "6":
	day = "Sa"
    if day == "7":
	day = "So"
    week = time.strftime('KW%W')
    date = time.strftime('%d:%m:%Y')

    tn.write("widget_set SCREEN 1 \"%s\"\n" % (date));
    tn.write("widget_set SCREEN 2 1 2 \"%s %s %s\"\n" % (day,week,cur));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    tn.write("widget_set SCREEN 1 \"IP-Adresse\"\n");
    tn.write("widget_set SCREEN 2 1 2 \"%s\"\n" % (ip));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    cmd1 = "cat /sys/class/thermal/thermal_zone0/temp"
    process = subprocess.Popen(cmd1, stdout=subprocess.PIPE , shell=True)
    os.waitpid(process.pid, 0)[1]
    cpu = process.stdout.read().strip()
    tn.write("widget_set SCREEN 1 \"Temperatur\"\n");
    tn.write("widget_set SCREEN 2 1 2 \"Aktuell: %.2sC  \" \n" % (cpu));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    cmd2 = "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq"
    process2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE , shell=True)
    os.waitpid(process2.pid, 0)[1]
    spd = process2.stdout.read().strip()

    tn.write("widget_set SCREEN 1 \" Taktrate \"\n");
    tn.write("widget_set SCREEN 2 1 2 \"Aktuell: %sMHz\" \n" % (spd[:-3]));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    cmd3 = "uptime | cut -dp -f2 | cut -d, -f1"
    process3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE , shell=True)
    os.waitpid(process3.pid, 0)[1]
    ut = process3.stdout.read().strip()
    tn.write("widget_set SCREEN 1 \" Laufzeit \"\n");
    tn.write("widget_set SCREEN 2 1 2 \"Boot: %s\" \n" % (ut));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    cmd4 = "cat /proc/loadavg | cut -d' ' -f1"
    process4 = subprocess.Popen(cmd4, stdout=subprocess.PIPE , shell=True)
    os.waitpid(process4.pid, 0)[1]
    lo = process4.stdout.read().strip()

    tn.write("widget_set SCREEN 1 \"   Last   \"\n");
    tn.write("widget_set SCREEN 2 1 2 \"Aktuell: %s\" \n" % (lo));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  count = 1
  while count  <= 5 :

    cmd5 = "cat /proc/meminfo | grep MemFree | cut -d':' -f2"
    process5 = subprocess.Popen(cmd5, stdout=subprocess.PIPE , shell=True)
    os.waitpid(process5.pid, 0)[1]
    mem = process5.stdout.read().strip()

    tn.write("widget_set SCREEN 1 \"Freier RAM\"\n");
    tn.write("widget_set SCREEN 2 1 2 \"%s  \" \n" % (mem));
    data += tn.read_until("\n");
    time.sleep(1)
    count = count +1

  #used space
  disk = os.statvfs("/")
  totalUsedSpace = float(disk.f_bsize*(disk.f_blocks-disk.f_bfree))
  used1 = round(totalUsedSpace/1024/1024/1024,1)
  totalAvailSpace = float(disk.f_bsize*disk.f_bfree)
  available1 = round(totalAvailSpace/1024/1024/1024,1)
  tn.write("widget_set SCREEN 1 \"   Root   \"\n");
  tn.write("widget_set SCREEN 2 1 2 \"Belegt: %s GB\" \n" % (available1));
  data += tn.read_until("\n");
  time.sleep(5)

  #Logged in user
  cmd1 = "who -q --count | grep = | cut -d= -f2"
  process = subprocess.Popen(cmd1, stdout=subprocess.PIPE , shell=True)
  os.waitpid(process.pid, 0)[1]
  us = process.stdout.read().strip()

  tn.write("widget_set SCREEN 1 \" Benutzer \"\n");
  tn.write("widget_set SCREEN 2 1 2 \"%s\" \n" % (us));
  data += tn.read_until("\n");
  time.sleep(3)
