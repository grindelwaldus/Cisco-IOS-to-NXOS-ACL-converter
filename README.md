# Cisco-IOS-to-NXOS-ACL-converter
A very simple script to convert ACL from IOS to NXOS format. Probably implemented not in the most graceful way, but does its job.

If you ever had to migrate a lot of ACLs from Cisco Catalyst switches to Nexus, you probably found out that unlike IOS, NXOS doesn't allow you to define a sequence of ports divided by whitespace. Instead, you'll have to make a separate line for each port. 
For instance, this IOS ACL entry
```
permit tcp host 10.54.60.34 10.54.51.12 0.0.0.3 eq 8080 8082
```
has to be converted to the following for NXOS to accept it:
```
permit tcp host 10.54.60.34 10.54.51.12 0.0.0.3 eq 8080
permit tcp host 10.54.60.34 10.54.51.12 0.0.0.3 eq 8082
```
It can easily turn into a nightmare if you have a lot of ACLs to migrate, especially if some entries contain both source and destination ports. This line would require 16 ACL entries on NXOS:
 ``` 
permit tcp 10.154.1.176 0.0.0.15 eq 50615 50620 50625 50630 10.54.60.32 0.0.0.31 eq 10615 10620 10625 10630
```
This script covers all the scenarios: entries with only source/destination ports, both source and destination ports, source/destination ports and range of ports. It also works with port mnemonics (like 'www', 'telnet', 'ftp' etc). 

Here's few examples of convertings it does:
```
ip access-list ports_and_range
 permit tcp host 10.54.60.84 range 1000 2000 10.54.51.12 0.0.0.3 eq 8080 8081 8082 8083
!
ip access-list johnny
 permit tcp host 10.54.201.145 eq irc 1288 host 10.54.201.241 eq cmd sunrpc telnet
```
to
```
ip access-list ports_and_range
 permit tcp host 10.54.60.84 range 1000 2000 10.54.51.12 0.0.0.3 eq 8080
 permit tcp host 10.54.60.84 range 1000 2000 10.54.51.12 0.0.0.3 eq 8081
 permit tcp host 10.54.60.84 range 1000 2000 10.54.51.12 0.0.0.3 eq 8082
 permit tcp host 10.54.60.84 range 1000 2000 10.54.51.12 0.0.0.3 eq 8083
!
ip access-list johnny
 permit tcp host 10.54.201.145 eq irc host 10.54.201.241 eq cmd
 permit tcp host 10.54.201.145 eq irc host 10.54.201.241 eq sunrpc
 permit tcp host 10.54.201.145 eq irc host 10.54.201.241 eq telnet
 permit tcp host 10.54.201.145 eq 1288 host 10.54.201.241 eq cmd
 permit tcp host 10.54.201.145 eq 1288 host 10.54.201.241 eq sunrpc
 permit tcp host 10.54.201.145 eq 1288 host 10.54.201.241 eq telnet
```

Usage: ```./acl_converter.py x.txt y.txt```, where ```x.txt``` is source file you have all your ACLs in and ```y.txt``` is where the converted ACLs would be written.
