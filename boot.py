# This file is executed on every boot (including wake-boot from deepsleep)
# boot.py for Esp32
import machine
import time
import qlib
import qtalk
import qsens
import qini

starttime = time.time()
qversion = 'OA24-1'

def runTime():
    # returns elapsed time in seconds
    return time.time() - starttime
    
def work(threshold=1.0):
    qsens.measure()
    if qsens.hasChanges(threshold):
        qsens.setChanges()
        url = qini.URL + "?v="+qversion+"&machine="+qlib.machineId()
        response=qtalk.put_https(url,{"data":qsens.jsonData()})
        if response:
            print('response:',response)    

def main():
    qtalk.connect_wifi(qini.WIFI_SSID, qini.WIFI_PASSWORD)
    qsens.buildSensorArray()
    print(qsens.jsonData())
    starttime = time.time()
    timeout = 3600*24
    stepS = 15
    while (time.time() - starttime) < timeout:
        print(runTime(), qlib.YmdHms())
        work(1.0)
        # print('Datenbestand')
        # qsens.jsonLine()
        time.sleep(stepS)
    
if __name__ == '__main__':
    main()
