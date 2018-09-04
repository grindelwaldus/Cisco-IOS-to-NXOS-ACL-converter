#!/usr/bin/env python3
import copy
from sys import argv
file_r, file_w = argv[1:]
file_opened = open(file_r, 'r')
file_write = open(file_w, 'w')
portnames = ['bgp', 'biff', 'bootpc', 'bootps', 'chargen', 'cmd', 'daytime', 'discard', 'dnsix', 'domain', 'drip', 'echo', 'exec', 'finger', 'ftp', 'ftp-data', 'gopher', 'hostname', 'ident', 'irc', 'isakmp', 'klogin', 'kshell', 'login', 'lpd', 'mobile-ip', 'nameserver', 'netbios-dgm', 'netbios-ns', 'netbios-ss', 'nntp', 'non500-isakmp', 'ntp', 'onep-plain', 'onep-tls', 'pim-auto-rp', 'pop2', 'pop3', 'rip', 'smtp', 'snmp', 'snmptrap', 'sunrpc', 'syslog', 'tacacs', 'talk', 'telnet', 'tftp', 'time', 'uucp', 'who', 'whois', 'www', 'xdmcp']
for line in file_opened:
    
	portslist = []
	portslist1 = []
	portslist2 = []
		
	if line.count(' eq ') == 1:
		if 'range' in line:
			line = line.split()
			newline = copy.deepcopy(line)
			index_eq = line.index('eq')
			index_range = line.index('range')
			if index_eq < index_range:
				for i in line[:index_range]:
					if i.isdigit() or i in portnames:
						portslist.append(i)
						newline.remove(i)
			else:
				for i in line[index_eq:]:						
					if i.isdigit() or i in portnames:
						portslist.append(i)
						newline.remove(i)												
												
		else:
			line = line.split()
			newline = copy.deepcopy(line)
			for i in line:
				if i.isdigit() or i in portnames:
					portslist.append(i)
					newline.remove(i)
															
		firstport = line.index(portslist[0])
		for k in portslist:
			newline_copy = copy.deepcopy(newline)
			newline_copy.insert(firstport, k)
			new_command_string = ' ' + ' '.join(newline_copy) + '\n'
			file_write.write(new_command_string)					
								
	elif line.count(' eq ') > 1:
		line = line.split()		
		occ1 = line.index('eq')
		occ2 = line[line.index('eq')+1:].index('eq') + line.index('eq') + 1
		newline1 = copy.deepcopy(line[:occ2])
		newline2 =	copy.deepcopy(line[occ2:])

		for i in line[:occ2]:
			if i.isdigit() or i in portnames:
				portslist1.append(i)
				newline1.remove(i)
		for i in line[occ2:]:
			if i.isdigit() or i in portnames:
				portslist2.append(i)
				newline2.remove(i)	
		firstport1 = line[:occ2].index(portslist1[0])
		firstport2 = line[occ2:].index(portslist2[0])

		for i in portslist1:
			newline1_copy = copy.deepcopy(newline1)
			newline1_copy.insert(firstport1, i)
			for y in portslist2:
				newline2_copy = copy.deepcopy(newline2)
				newline2_copy.insert(firstport2, y)
				new_command_string = ' ' + ' '.join(newline1_copy) +  ' ' + ' '.join(newline2_copy) + '\n'
				file_write.write(new_command_string)
	else:
			file_write.write(line)
		
file_opened.close()