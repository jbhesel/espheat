# qsens.py lib for esp32 dealing with sensors
import onewire, ds18x20, time, binascii, json, machine
import qlib

ds_pin = machine.Pin(14)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()
datH = {}
arcH = {}
loglevel = 1 # 1=debug 2=info 3=some 4=ohne

def qbug(name, content, level=loglevel):
    if level >= 4: # no debug at all
        return
    
    

def sensor8(rom):
    return binascii.hexlify(rom)[8:].decode()

def buildSensorArray():
  for rom in roms:
    sensorid = sensor8(rom)
    tempC = ds_sensor.read_temp(rom)
    print(sensorid, tempC)
    datH[sensorid] = {
        'TempC': [{'yms':'19991231235959', 'val': -100}]
        }
    #datH['maschine'] = {
    #    'id':[{'yms':'19991231235959', 'val': qlib.machineId()}]
    #    }
    arcH[sensorid] = {
        "TempC": []
        }
    return datH
  print(datH)

def measure():
  ds_sensor.convert_temp()
  smallChangeB = False
  for rom in roms:
    tempC = ds_sensor.read_temp(rom)
    rec = {
            "yms": qlib.yms(),
            "val": round(tempC,1)
          }
    last = datH[sensor8(rom)]["TempC"][0]["val"]
    if abs(rec["val"]- last) > 0.11:
        datH[sensor8(rom)]["TempC"].insert(0,rec)
        smallChangeB = True
  if smallChangeB:
      mdDat()
  return datH
  # {"d4866806": { "tempC": [{"yms": 20241231235959, "val":25.2}] }}

def hasChanges(threshold=1.0):
    changeB=False
    for sid,sensor in datH.items():
        if not 'TempC' in sensor:
            continue
        current = sensor["TempC"][0]["val"]
        last = sensor["TempC"][-1]["val"]
        # print('changetest', current-last)
        if abs(current-last) > threshold:
            changeB=True
    return changeB

def setChanges():
    for sid,sensor in datH.items():
        if not 'TempC' in sensor:
            continue
        # reduce data to current record
        # print('setchanges', sid, sensor)
        currentRec = sensor["TempC"][0]
        sensor["TempC"] = []
        sensor["TempC"].insert(0, currentRec)
        # save the current rec to archive
        arcH[sid]["TempC"].insert(0, currentRec)
    print('mdArc')
    mdArc()

def jsonData():
    return json.dumps(datH)

def mdData(datH, maxn=3):
    qlib.md(flattenA(datH), ['lom','yms','att','val'], maxn)
    
def flattenA(datH, maxn=9999):
    flatA = []
    for lom, data in datH.items():
        for att, recA in data.items():
            for rec in recA[:maxn]:
                flatA.append({'lom':lom, 'att':att, 'yms':rec['yms'], 'val':rec['val']})
    return flatA

def jsonLine(datH=datH, maxn=9999):
    flatA = flattenA(datH,maxn)
    for rec in flatA:
        print(json.dumps(rec))

def mdArc():
    mdData(arcH)

def mdDat():
    mdData(datH)


