# SNMP
from snmp_helper import snmp_extract, snmp_get_oid



Community= 'galileo'
SNMP_Ports=[7961,8061]
IP = '50.242.94.227'

router1=(IP,Community,SNMP_Ports[0])
router2=(IP,Community,SNMP_Ports[1])
router =[router1 , router2]

#Uptime of the device
sysUptime = '1.3.6.1.2.1.1.3.0'
# Uptime when running config last changed    
ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
# Uptime when running config last saved (note any 'write' constitutes a save)
ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
# Uptime when startup config last saved   
ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'


current_sysUptime=int(snmp_extract(snmp_get_oid(router2, sysUptime)))
current_RunningLastChanged=int(snmp_extract(snmp_get_oid(router2,
                                                     ccmHistoryRunningLastChanged)))
current_RunningLastSaved=int(snmp_extract(snmp_get_oid(router2,
                                                   ccmHistoryRunningLastSaved)))
current_StartupLastChanged=int(snmp_extract(snmp_get_oid(router2,
                                                     ccmHistoryStartupLastChanged)))
with open('SNMP.txt','r') as SNMP_Times:
    SysUpTime = int(SNMP_Times.readline().strip('\n'))
    RunningLastChanged=int(SNMP_Times.readline().strip('\n'))
    RunningLastSaved=int(SNMP_Times.readline().strip('\n'))
    StartupLastChanged =int(SNMP_Times.readline().strip('\n'))

    
if current_sysUptime < SysUpTime:
    print('device has been rebooted')
    if current_RunningLastChanged < RunningLastChanged:
        print ('running has changed but not saved to startup')
        RunningLastChnaged=current_RunningLastChanged
        RunningLastSaved=current_RunningLastSaved
        StartupLastChanged=current_StartupLastChanged
        
if (current_RunningLastChanged > RunningLastChanged and
    current_RunningLastSaved == 0 or current_RunningLastSaved  and
    current_StartupLastChanged == 0):
    print('you running config has changed but no saved to startup')
    RunningLastChanged =current_RunningLastChanged
    RunningLastSaved =0
    StartupLastChanged = 0


if (current_RunningLastChanged > RunningLastChanged and
    current_RunningLastSaved == RunningLastSaved and
    current_StartupLastChanged == StartupLastChanged):
    print('you running config has changed but no saved to startup')
    RunningLastChanged =current_RunningLastChanged
    

if (current_RunningLastChanged == RunningLastChanged and
    current_RunningLastSaved > RunningLastSaved and
    current_StartupLastChanged > StartupLastChanged):
    
    RunningLastSaved = current_RunningLastSaved
    StartupLastChanged = current_StartupLastChanged

if (current_RunningLastChanged == RunningLastChanged and
    current_RunningLastSaved > RunningLastSaved and
    current_StartupLastChanged == StartupLastChanged):
    RunningLastSaved = current_RunningLastSaved
    
if (current_RunningLastChanged == RunningLastChanged and
    current_RunningLastSaved > RunningLastSaved and
    current_StartupLastChanged == 0):
    RunningLastSaved = current_RunningLastSaved
    StartupLastChanged =0
    print('Startup Config has not been save since last reboot')
        
SysUpTime = current_sysUptime

data = (str(SysUpTime) + '\n' + str(RunningLastChanged) + '\n'
        + str(RunningLastSaved) + '\n'  + str(StartupLastChanged) + '\n')
        

with open('SNMP.txt','w') as SNMP_Times:
          SNMP_Times.write(data)

