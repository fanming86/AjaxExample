#coding:utf-8


import wmi
import json
import sys  
import platform
import urllib, urllib2
import time  
import win32com.client as client  
  
class DataPollster(object):
	#获取cpu利用率
	def get_cpu(self):
        # Initilization  
		c = wmi.WMI()
		data_dict = {}
		for cpu in c.Win32_Processor():
			device = cpu.DeviceID.lower()

		    # Get cpu_usage
		 	data_dict[device] = {'volume':float(cpu.LoadPercentage), 'unit':'%'}
		return data_dict

	#获取内存
	def get_memory(self):
	    c = wmi.WMI ()
	    cs = c.Win32_ComputerSystem()
	    os = c.Win32_OperatingSystem()
	    pfu = c.Win32_PageFileUsage()

	    data_dict = {}
	    data_dict["MemTotal"] = {'volume':float(cs[0].TotalPhysicalMemory) / (1024*1024), 'unit':'MB'}
	    data_dict["MemFree"] = {'volume':float(os[0].FreePhysicalMemory)/1024, 'unit':'MB'}
	    data_dict["SwapTotal"] = {'volume':float(pfu[0].AllocatedBaseSize), 'unit':'MB'}
	    data_dict["SwapFree"] = {'volume':float(pfu[0].AllocatedBaseSize - pfu[0].CurrentUsage), 'unit':'MB'}
	    return {'data':data_dict, 'timestamp':time.asctime(time.localtime())}

	#获取网络状态
	def get_net(self):
		c = wmi.WMI ()
		com = client.Dispatch("WbemScripting.SWbemRefresher")
		obj = client.GetObject("winmgmts:\\root\cimv2")
		items = com.AddEnum(obj, "Win32_PerfRawData_Tcpip_NetworkInterface").objectSet

		data_dict = {}
		interfaces = []
		for interface in c.Win32_NetworkAdapterConfiguration (IPEnabled=1):
			print interface.IPAddress[0]
			interfaces.append(interface.Description)

		net_bytes_in = 0
		net_bytes_out = 0
		net_pkts_in = 0
		net_pkts_out = 0

		com.Refresh()
		for item in items:
			if item.Name in interfaces:
		        #print 'Name:%s -> B_in:%s, B_out:%s, P_in:%s, P_out:%s' %(item.Name, item.BytesReceivedPerSec, item.BytesSentPerSec, item.PacketsReceivedPerSec, item.PacketsSentPerSec)
				net_bytes_in += long(item.BytesReceivedPerSec)
				net_bytes_out += long(item.BytesSentPerSec)
				net_pkts_in += long(item.PacketsReceivedPerSec)
				net_pkts_out += long(item.PacketsSentPerSec)

		time.sleep(1)

		net_bytes_in_cur = 0
		net_bytes_out_cur = 0

		com.Refresh()
		for item in items:
			if item.Name in interfaces:
				net_bytes_in = long(item.BytesReceivedPerSec) - net_bytes_in
				net_bytes_in_cur += long(item.BytesReceivedPerSec)
				net_bytes_out = long(item.BytesSentPerSec) - net_bytes_out
				net_bytes_out_cur += long(item.BytesSentPerSec)
				net_pkts_in = long(item.PacketsReceivedPerSec) - net_pkts_in
				net_pkts_out = long(item.PacketsSentPerSec) - net_pkts_out

		data_dict['net_bytes_in'] = {'volume':net_bytes_in, 'unit':'B/s'}
		data_dict['net_bytes_in_sum'] = {'volume':net_bytes_in_cur, 'unit':'B'}
		data_dict['net_bytes_out'] = {'volume':net_bytes_out, 'unit':'B/s'}
		data_dict['net_bytes_out_sum'] = {'volume':net_bytes_out_cur, 'unit':'B'}
		data_dict['net_pkts_in'] = {'volume':net_pkts_in, 'unit':'p/s'}
		data_dict['net_pkts_out'] = {'volume':net_pkts_out, 'unit':'p/s'}

		return {'data':data_dict, 'timestamp':time.asctime(time.localtime())}

	#写入数据库
	# def save(self):


def main():
	dta = DataPollster()
	while True:
		data = dta.get_memory()
		print json.dumps(data)
		try:
			f = None
			req = urllib2.Request("http://localhost:5000/data", json.dumps(data), {'Content-Type': 'application/json'})
			f = urllib2.urlopen(req)
		except urllib2.URLError as e:
			if hasattr(e, 'code'):
				print 'Error code:', e.code
			elif hasattr(e, 'reason'):
				print 'Reason:', e.reason
		finally:
			if f:
				f.close()
		time.sleep(3)

if __name__ == '__main__':
		main()