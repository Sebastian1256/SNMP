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
print(current_RunningLastChanged)

with open('SNMP.txt','r') as SNMP_Times:
    SysUpTime = int(SNMP_Times.readline().strip('\n'))
    RunningLastChanged=int(SNMP_Times.readline().strip('\n'))


if current_sysUptime < SysUpTime:
    print('device has been rebooted')
    if (current_RunningLastChanged > current_StartupLastChanged) and (current_RunningLastChanged > RunningLastChanged) == True:
        print 'running has changed but not saved to startup'
        

if (current_RunningLastChanged > current_StartupLastChanged) and (current_RunningLastChanged > RunningLastChanged) == True:
    print 'running has changed but not saved to startup'
        

        

SysUpTime = current_sysUptime
RunningLastChanged=current_RunningLastChanged


data = (str(SysUpTime) + '\n' + str(RunningLastChanged) + '\n')
