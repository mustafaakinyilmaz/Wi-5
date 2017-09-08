import os
import tkinter
import paramiko
import scan_sh as sch
from multiprocessing import Process

master = tkinter.Tk()

default_values = {'AP1_ip':'192.168.6.x','AP2_ip':'192.168.6.x','AP3_ip':'192.168.6.x'}

username = 'root'
password = '1357924680'
port = 22

# PATHS
scan_ap3_sh_local = '/home/akinyilmaz/Desktop/required_files/scan_ap3.sh'
scan_ap3_sh_remote = '/usr/share/click'

wlan_awk_local = '/home/akinyilmaz/Desktop/required_files/wlan_scan_new.awk'
wlan_awk_remote = '/usr/share/click'



# AP1
L1 = tkinter.Label(master, text = "AP1 IP:")
L1.place(relx = 0.05, rely = 0.05)
E1 = tkinter.Entry(master, bd = 5)
E1.insert(0,default_values['AP1_ip'])
E1.place(relx = 0.15, rely = 0.05)

# AP2
L2 = tkinter.Label(master, text = "AP2 IP:")
L2.place(relx = 0.05, rely = 0.20)
E2 = tkinter.Entry(master, bd = 5)
E2.insert(0,default_values['AP2_ip'])
E2.place(relx = 0.15, rely = 0.20)


# TEST DURATION
L4 = tkinter.Label(master, text = "Test Duration:")
L4.place(relx = 0.50, rely = 0.55)
E4 = tkinter.Entry(master, bd = 5)
E4.place(relx = 0.70, rely = 0.55)

# TIME INTERVAL
L5 = tkinter.Label(master, text = "Waiting Time:")
L5.place(relx = 0.50, rely = 0.70)
E5 = tkinter.Entry(master, bd = 5)
E5.place(relx = 0.70, rely = 0.70)

# AP3 SSID
L8 = tkinter.Label(master, text = "AP3 SSID:")
L8.place(relx = 0.50, rely = 0.05)
E8 = tkinter.Entry(master, bd = 5)
E8.place(relx = 0.70, rely = 0.05)




def configure_scan_sh():
    configured_scan_sh_ap3 = sch.scan_sh_template.format("%s","%s","%s","%s","%s") %(E4.get(),"%s","%s",E8.get(),E5.get())
    with open('/home/akinyilmaz/Desktop/required_files/scan_ap3.sh','w') as outsch3:
        outsch3.write(configured_scan_sh_ap3)
        print("scan_ap3.sh configuration successful")


def transfer_configurations():
    os.system('sshpass -p "' + password + '" scp ' + wlan_awk_local + ' root@' + E1.get() + ':' + wlan_awk_remote)
    os.system('sshpass -p "' + password + '" scp ' + wlan_awk_local + ' root@' + E2.get() + ':' + wlan_awk_remote)


    res13 = os.system('sshpass -p "' + password + '" scp ' + scan_ap3_sh_local + ' root@' + E1.get() + ':' + scan_ap3_sh_remote)
    if res13 == 0:
        print('scan_ap3.sh transfer to %s successful'%("AP1"))
    else:
        print('Unsuccessful transfer of scan_ap3.sh')

    res23 = os.system('sshpass -p "' + password + '" scp ' + scan_ap3_sh_local + ' root@' + E2.get() + ':' + scan_ap3_sh_remote)
    if res23 == 0:
        print('scan_ap3.sh transfer to %s successful' % ("AP2"))
    else:
        print('Unsuccessful transfer of scan_ap3.sh')



def chmod_scan():
    remotehost1 = E1.get()
    ssh1 = paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh1.connect(remotehost1, port=port, username=username, password=password)
        channel1 = ssh1.get_transport().open_session()
        channel2 = ssh1.get_transport().open_session()
        try:
            channel2.exec_command('chmod +x /usr/share/click/scan_ap3.sh')
        except:
            print('chmod +x command could not be sent')
    except paramiko.SSHException:
        print("Connection failed")
    ssh1.close()

    remotehost2 = E2.get()
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh2.connect(remotehost2, port=port, username=username, password=password)
        channel1 = ssh2.get_transport().open_session()
        channel2 = ssh2.get_transport().open_session()
        try:
            channel2.exec_command('chmod +x /usr/share/click/scan_ap3.sh')
        except:
            print('chmod +x command could not be sent')
    except paramiko.SSHException:
        print("Connection failed")
    ssh2.close()



def test():


    def ap1_scan_ap3():
        remotehost1 = E1.get()
        ssh1 = paramiko.SSHClient()
        ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh1.connect(remotehost1, port=port, username=username, password=password)

        stdin, stdout, stderr = ssh1.exec_command('cd /usr/share/click;./scan_ap3.sh', get_pty=True)
        outs = stdout.read()
        strout = outs.decode('utf-8')

        with open('/home/akinyilmaz/Desktop/test13.txt', 'w') as out1:
            out1.write(strout)
        ssh1.close()

    def ap2_scan_ap3():
        remotehost2 = E2.get()
        ssh2 = paramiko.SSHClient()
        ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh2.connect(remotehost2, port=port, username=username, password=password)

        stdin, stdout, stderr = ssh2.exec_command('cd /usr/share/click;./scan_ap3.sh', get_pty=True)
        outs = stdout.read()
        strout = outs.decode('utf-8')

        with open('/home/akinyilmaz/Desktop/test23.txt', 'w') as out:
            out.write(strout)
        ssh2.close()

    th13 = Process(target=ap1_scan_ap3)
    th13.start()
    th23 = Process(target=ap2_scan_ap3)
    th23.start()

    exit()

# Configuration BUTTON
ConfButton = tkinter.Button(master,text = "Configure",command = lambda: [configure_scan_sh()])
ConfButton.place(relx= 0.15, rely= 0.55)

# Transfer BUTTON
TransferButton = tkinter.Button(master,text = "Transfer",command = lambda: [transfer_configurations(),chmod_scan()])
TransferButton.place(relx= 0.15, rely= 0.70)

# Test BUTTON
TestButton = tkinter.Button(master,text= "Test",command= lambda: [test()])
TestButton.place(relx= 0.15, rely= 0.85)

master.title("Wi5 Test6.1.1")
master.geometry('550x300')
master.mainloop()