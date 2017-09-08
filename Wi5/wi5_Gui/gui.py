import tkinter
from tkinter import messagebox
import paramiko
import os
import wireless_template as wlt
import start_sh as st
import network_template as nt
import agent_click as ag

master = tkinter.Tk()
var = tkinter.IntVar()

default_values = {'data_plane_ip':'192.168.5.x','control_plane_ip':'192.168.6.x','data_port':'eth1.x','control_port':'eth1.x','ap_ip':'192.168.x.x'}
username = 'root'
password = '1357924680'
port = 22

#REMOTE and LOCAL PATHS
firewall_local_path = '/home/akinyilmaz/Desktop/required_files/firewall'
firewall_remote_path = '/etc/config/'

wireless_local_path = '/home/akinyilmaz/Desktop/required_files/configured_wireless.txt'
wireless_remote_path = '/etc/config/'

network_local_path = '/home/akinyilmaz/Desktop/required_files/configured_network.txt'
network_remote_path = '/etc/config/'

agent_click_local_path = '/home/akinyilmaz/Desktop/required_files/configured_agent_click.txt'
agent_click_remote_path = '/usr/share/click/'

start_sh_local_path = '/home/akinyilmaz/Desktop/required_files/configured_start.sh'
start_sh_remote_path = '/usr/share/click/'

click_exe_local_path = '/home/akinyilmaz/Desktop/required_files/click_for_AR71xx'
click_exe_remote_path = '/tmp/'



# AP's Current IP Label and Entrry
L1 = tkinter.Label(master, text = "AP CurrentIP:")
L1.place(relx = 0.05, rely = 0.05)
E1 = tkinter.Entry(master, bd = 5)
E1.insert(0,default_values['ap_ip'])
E1.place(relx = 0.25, rely = 0.05)

# Control Plane IP Label and Entry
L2 = tkinter.Label(master, text = "ContPlaneIP:")
L2.place(relx = 0.05, rely = 0.15)
E2 = tkinter.Entry(master, bd = 5)
E2.insert(0,default_values['control_plane_ip'])
E2.place(relx = 0.25, rely = 0.15)

# Control Plane Port Label and Entry
L3 = tkinter.Label(master, text = "ContPanelPort:")
L3.place(relx = 0.55, rely = 0.15)
E3 = tkinter.Entry(master, bd = 5)
E3.insert(0,default_values['control_port'])
E3.place(relx = 0.75, rely = 0.15)

# Data Plane IP Label and Entry
L4 = tkinter.Label(master, text = "DataPlaneIP:")
L4.place(relx = 0.05, rely = 0.25)
E4 = tkinter.Entry(master, bd = 5)
E4.insert(0,default_values['data_plane_ip'])
E4.place(relx = 0.25, rely = 0.25)

# Data Plane Port Label and Entry
L5 = tkinter.Label(master, text = "DatePlanePort:")
L5.place(relx = 0.55, rely = 0.25)
E5 = tkinter.Entry(master, bd = 5)
E5.insert(0,default_values['data_port'])
E5.place(relx = 0.75, rely = 0.25)

# Wireless Channel
L6 = tkinter.Label(master, text = "Wireless Channel:")
L6.place(relx = 0.55, rely = 0.05)
E6 = tkinter.Entry(master, bd = 5)
E6.place(relx = 0.75, rely = 0.05)

# Non-Odin SSID
L7 = tkinter.Label(master, text = "Non-Odin SSID:")
L7.place(relx = 0.05, rely = 0.35)
E7 = tkinter.Entry(master, bd = 5)
E7.place(relx = 0.25, rely = 0.35)

# ODIN LABEL
L8 = tkinter.Label(master, text = "ODIN PART")
L8.place(relx = 0.70, rely = 0.45)

# ODIN SSID
L9 = tkinter.Label(master, text = "ODIN SSID:")
L9.place(relx = 0.55, rely = 0.55)
E9 = tkinter.Entry(master, bd = 5)
E9.place(relx= 0.75, rely = 0.55)

# Debug ODIN
L10  = tkinter.Label(master, text= "Debug ODIN:")
L10.place(relx= 0.55, rely= 0.65)
E10 = tkinter.Entry(master, bd = 5)
E10.place(relx= 0.75, rely = 0.65)

# Multichannel Agents
L11  = tkinter.Label(master, text= "MultiChan Agents:")
L11.place(relx= 0.55, rely= 0.75)
E11 = tkinter.Entry(master, bd = 5)
E11.place(relx= 0.75, rely = 0.75)


# start.sh
var1 = tkinter.IntVar()
C1 = tkinter.Checkbutton(master, variable = var1, text = "start.sh")
C1.place(relx = 0.05, rely = 0.65)

# agent.click
var2 = tkinter.IntVar()
C2 = tkinter.Checkbutton(master, variable = var2, text = "agent.click")
C2.place(relx = 0.25, rely = 0.65)

# wireless
var3 = tkinter.IntVar()
C3 = tkinter.Checkbutton(master, variable = var3, text = "wireless")
C3.place(relx = 0.25, rely = 0.55)

# network
var4 = tkinter.IntVar()
C4 = tkinter.Checkbutton(master, variable = var4, text = "network")
C4.place(relx = 0.05, rely = 0.75)

# firewall
var5 = tkinter.IntVar()
C5 = tkinter.Checkbutton(master, variable = var5, text = "firewall")
C5.place(relx = 0.25, rely = 0.75)

# click exe
var6 = tkinter.IntVar()
C6 = tkinter.Checkbutton(master, variable = var6, text = "click.exe")
C6.place(relx = 0.05, rely = 0.55)


# Wireless Configuration
def configure_wireless():
    if var3.get() == 1:
        configured_wireless = wlt.wireless_template.format("%s","%s")%(E6.get(),E7.get())
        with open('/home/akinyilmaz/Desktop/required_files/configured_wireless.txt','w') as outwireless:
            outwireless.write(configured_wireless)
            print("Wireless configuration successful")

# Start.sh Configuration
def configure_start_sh():
    if var1.get() == 1:
        configured_start_sh = st.start_sh_template.format("%s")%(E5.get())
        with open('/home/akinyilmaz/Desktop/required_files/configured_start.sh','w') as outstart:
            outstart.write(configured_start_sh)
            print("Start.sh configuration successful")


# Network Configuration
def configure_network():
    lan_ifaces = ['1', '2', '3', '4']
    if var4.get() == 1:
        entered_port = [E3.get()[5:], E5.get()[5:]]
        # Control Plane Format
        configured_force2 = nt.force_template2.format("%s", "%s", "%s") % (entered_port[0], entered_port[0], E2.get())
        # Data Plane Format
        configured_force1 = nt.force_template1.format("%s", "%s", "%s") % (entered_port[1], entered_port[1], E4.get())

        not_used_lan_ifaces = [x for x in lan_ifaces if x != entered_port[0]]
        not_used_lan_ifaces = [x for x in not_used_lan_ifaces if x != entered_port[1]]

        # Not used interface1 Format
        configured_lan1 = nt.lan_template1.format("%s", "%s") % (not_used_lan_ifaces[0], not_used_lan_ifaces[0])
        # Not used interface2 Format
        configured_lan2 = nt.lan_template2.format("%s", "%s") % (not_used_lan_ifaces[1], not_used_lan_ifaces[1])

        # Configured Network Template
        configured_network = nt.network_template.format("%s","%s","%s","%s") % (configured_force1,configured_force2,configured_lan1,configured_lan2)

        with open('/home/akinyilmaz/Desktop/required_files/configured_network.txt', 'w') as outnetwork:
            outnetwork.write(configured_network)
            print("Network configuration successful")



def configure_agent_click():
    if var2.get() == 1:
        remotehost = E1.get()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(remotehost, port= port, username= username, password=password)
            (stdin,stdout,stderr) = (ssh.exec_command('ifconfig wlan0 | grep wlan0'))
            out = stdout.read()
            strout = out.decode('utf-8')
            HWaddr = strout[-20:-3]
            print(HWaddr)
            configured_agent_click = ag.agent_click_template.format("%s","%s","%s","%s","%s","%s","%s","%s") % (HWaddr,E6.get(),E2.get(),E9.get(),E10.get(),E11.get(),E2.get(),HWaddr)
            with open('/home/akinyilmaz/Desktop/required_files/configured_agent_click.txt', 'w') as outagent:
                outagent.write(configured_agent_click)
                print("Agent.click configuration successful")
            ssh.close()
        except paramiko.SSHException:
            print("Connection failed")

def config_message():
    messagebox.showinfo("Configuration","All configurations created")


def transfer_configurations():
    if var1.get() == 1:
        res1 = os.system('sshpass -p "' + password + '" scp ' + start_sh_local_path + ' root@' + E1.get() + ':' + start_sh_remote_path + 'start.sh')
        if res1 == 0:
            print('start.sh transfer successful')
        else:
            print('Unsuccessful transfer of start.sh')
    if var2.get() == 1:
        res2 =  os.system('sshpass -p "' + password + '" scp ' + agent_click_local_path + ' root@' + E1.get() + ':' + agent_click_remote_path + 'agent.click')
        if res2 == 0:
            print('agent.click transfer successful')
        else:
            print('Unsuccessful transfer of agent.click')
    if var3.get() == 1:
        res3 = os.system('sshpass -p "' + password + '" scp ' + wireless_local_path + ' root@' + E1.get() + ':' + wireless_remote_path + 'wireless')
        if res3 == 0:
            print('wireless transfer successful')
        else:
            print('Unsuccessful transfer of wireless')
    if var4.get() == 1:
        res4 = os.system('sshpass -p "' + password + '" scp ' + network_local_path + ' root@' + E1.get() + ':' + network_remote_path + 'network')
        if res4 == 0:
            print('network transfer successful')
        else:
            print('Unsuccessful transfer of network')
    if var5.get() == 1:
        res5 = os.system('sshpass -p "' + password + '" scp ' + firewall_local_path + ' root@' + E1.get() + ':' + firewall_remote_path + 'firewall')
        if res5 == 0:
            print('firewall transfer successful')
        else:
            print('Unseccessful transfer of firewall')
    if var6.get() == 1:
        res6 = os.system('sshpass -p "' + password + '" scp ' + click_exe_local_path + ' root@' + E1.get() + ':' + click_exe_remote_path + 'agent_click_forAR71xx')
        if res6 == 0:
            print('click.exe transfer successful')
        else:
            print('Unsuccessful transfer of click.exe')




def ssh_connection_restart_network():

    remotehost = E1.get()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(remotehost, port=port, username= username, password=password)
        channel1 = ssh.get_transport().open_session()
        channel2 = ssh.get_transport().open_session()
        try:
            channel1.exec_command('chmod +x /usr/share/click/start.sh')
            channel2.exec_command('/etc/init.d/network restart')
            print("init.d and chmod +x successful")
            print("Current ip is: %s" % (E2.get()))
            messagebox.showinfo("IP","Please give your PC a static IP with domain 6.")
        except:
            print('init.d and chmod +x commands could not be sent')
    except paramiko.SSHException:
        print("Connection failed")

    ssh.close()
    exit()

# Go Button
GoButton = tkinter.Button(master,text = "GO!", command = lambda: [configure_wireless(),configure_start_sh(),configure_network(),configure_agent_click(),config_message(),transfer_configurations(),ssh_connection_restart_network()])
GoButton.place(relx = 0.05, rely = 0.85)



master.title("Wi5 Configuration")
master.geometry('650x400')
master.mainloop()
