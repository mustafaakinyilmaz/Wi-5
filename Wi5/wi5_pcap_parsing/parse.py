import os
import pandas as pd



path = "/home/akinyilmaz/Desktop/pcap/"
source_ip = "192.168.5.219"
dest_ip = "192.168.5.81"

def remove(s):
    return s[30:]

def format_time(list):
    formatted = [members[13:-7] for members in list ]
    return formatted

def open_pcap():
    pcap_files = os.popen("ls "+path+"*.pcap")
    out = pcap_files.read()
    str = out.split()
    return str

def pcap_to_csv(pcap_index):
    os.system("tshark -T fields -n -r "+open_pcap()[pcap_index]+" -E separator=* -E header=y -e frame.time -e ip.src -e ip.dst -e ip.proto -e tcp.port > %s.csv" %(open_pcap()[pcap_index][:-5]))

def tcp_contains_remove(pcap_index):
    os.system('tshark -T fields -n -r '+open_pcap()[pcap_index]+' -E separator=* -E header=y -Y "tcp contains "remove"" -e frame.time -e ip.src -e ip.dst -e ip.proto -e tcp.port > %s.csv' %(open_pcap()[pcap_index][:-5]+"remove"))

def tcp_contains_add(pcap_index):
    os.system('tshark -T fields -n -r ' + open_pcap()[pcap_index] + ' -E separator=* -E header=y -Y "tcp contains "add"" -e frame.time -e ip.src -e ip.dst -e ip.proto -e tcp.port > %s.csv' % (open_pcap()[pcap_index][:-5] + "add"))


# take index as input
pcap_list = []
for i in open_pcap():
    pcap_list.append(remove(i))

print(pcap_list)
pcap_index = int(input("Please enter index of .pcap file:"))
pcap_to_csv(pcap_index)


#  Ordinary csv file
csv_read = pd.read_csv(open_pcap()[pcap_index][:-5]+".csv", sep="*", low_memory=False)
ip_src = csv_read["ip.src"]
ip_dest = csv_read["ip.dst"]
ip_proto = csv_read["ip.proto"]
frame_time = csv_read["frame.time"]
formatted_frame_time = format_time(frame_time)
frame_datetime = pd.to_datetime(formatted_frame_time, format= "%H:%M:%S.%f")



# tcp contains "remove" file
tcp_contains_remove(pcap_index)

csv_remove_read = pd.read_csv(open_pcap()[pcap_index][:-5]+"remove.csv", sep="*", low_memory=False)
frame_remove_time = csv_remove_read["frame.time"]
frame_remove_vap_OK = frame_remove_time[1::2]
formatted_remove_time = format_time(frame_remove_vap_OK)
remove_datetime = pd.to_datetime(formatted_remove_time, format= "%H:%M:%S.%f")



delay_list = []
for k in range(len(remove_datetime)):
    dataFrame = pd.DataFrame({'date_time':frame_datetime,'source_ip':ip_src,'dest_ip':ip_dest,'protocol':ip_proto})
    dataFrame = dataFrame[dataFrame.source_ip == source_ip]
    dataFrame = dataFrame[dataFrame.dest_ip == dest_ip]
    dataFrame = dataFrame[dataFrame.protocol == "6"]
    dataFrame = dataFrame[dataFrame.date_time > remove_datetime[k]]
    time_i = remove_datetime[k]
    time_f = dataFrame['date_time'].iloc[0]
    delay = time_f - time_i
    delay_list.append(delay)




#total = pd.to_datetime(0)
total = delay_list[0]
count = len(delay_list)

if count > 1:
    for l in range(count-1):
        total = total + delay_list[l+1]

average_delay_str = str(total/count)
average_delay = average_delay_str[17:-3]

print("Average delay for %s is = %s ms." %(pcap_list[pcap_index],average_delay))