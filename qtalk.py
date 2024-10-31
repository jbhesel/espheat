# qtalk.py library for ESP32 and measuring with DS18B20
import network
import time
import utime
import ntptime
import urequests
import json

def getYmdHms():  # -> 2024-12-32 23:59:59
  # Get the current time
  mytime = utime.localtime()
  # Format the current time as "dd/mm/yyyy HH:MM"
  formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02}".format(mytime[0], mytime[1], mytime[2], mytime[3], mytime[4], mytime[5])  
  return formatted_time

def getNtpTime():  # retrieve time from internet 
  # otherwise the esp32 points at 1970 from start
  # if needed, overwrite default time server
  ntptime.host = "1.europe.pool.ntp.org"
  try:
    vorher = getYmdHms()
    ntptime.settime()
    nacher = getYmdHms()
    if vorher != nacher:
        print("time changed:" , vorher, nacher)
    else:
        print("time:", nacher)
  except:
    print("Error syncing time")

def connect_wifi(ssid, password, timeout=10):
    """Connect ESP32 to WiFi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print('Already connected to:', wlan.config('ssid'))
        getNtpTime()
        return True
    print('Connecting to:', ssid)
    wlan.connect(ssid, password)
    start_time = time.time()
    while not wlan.isconnected():
        if time.time() - start_time > timeout:
            print('Connection timeout')
            return False
        time.sleep(0.1)
    print('Connected!')
    print('IP address:', wlan.ifconfig()[0])
    getNtpTime()
    return True

def send_https_put(url, data, headers=None, verify=True):
    """Send HTTPS PUT request"""
    if headers is None:
        headers = {
            'Content-Type': 'application/json'
        }
    try:
        if isinstance(data, dict):
            data = json.dumps(data)
        # print('qtalk', data)
        response = urequests.put(
            url,
            data=data,
            headers=headers# ,
            # verify=verify
        )
        status_code = response.status_code
        try:
            response_data = response.json()
        except:
            response_data = response.text
        response.close()
        return True, response_data, status_code
    except Exception as e:
        return False, str(e), None

def put_https(url, sensor_data):
    """ send json data, return only boolean success """
    success, response, status = send_https_put(
        url, 
        sensor_data, 
        headers= None #,
        # verify=False  # Set to True if your API has valid SSL cert
    )
    # Handle the response
    if success:
        print('Successfully sent data')
        # print('Response:', response)
        # print('Status:', status)
        return response
    else:
        print('Failed to send data')
        print('Error:', response)
        return false

# Main program configuration
WIFI_SSID = 'YourWiFiName'
WIFI_PASSWORD = 'YourWiFiPassword'
API_URL = 'https://api.example.com/data'
API_TOKEN = 'your-token-here'

def main():
    # Connect to WiFi
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        print("Failed to connect to WiFi")
        return
    # Prepare your data
    sensor_data = {
        'sensor': 'temperature',
        'value': 25.6
    }
    # Prepare headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    # Send the request
    success, response, status = send_https_put(
        API_URL, 
        sensor_data, 
        headers=headers,
        verify=False  # Set to True if your API has valid SSL cert
    )
    # Handle the response
    if success:
        print('Successfully sent data')
        print('Response:', response)
        print('Status:', status)
    else:
        print('Failed to send data')
        print('Error:', response)

# Run the main program
if __name__ == '__main__':
    main()



