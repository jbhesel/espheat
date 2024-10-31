# qlib.py library for esp32
# all internal functions (without network and sensors)
import machine
import hashlib
import utime
import time
import binascii

def md(dict_array, headers=0, maxn=9999):
    """
    Konvertiert ein Array von Dictionaries in eine Markdown-Tabelle und gibt diese aus.
    Args:
        dict_array: Liste von Dictionaries mit einheitlichen Schlüsseln
    """
    if not dict_array or not isinstance(dict_array, list) or not dict_array[0]:
        print("Leeres oder ungültiges Array")
        return
    def format_value(value):
        """Hilfsfunktion zum Formatieren von Werten"""
        if isinstance(value, bytes):
            return value.decode()
        return str(value)
    def pad_string(s, width):
        """Fügt Leerzeichen an, bis die gewünschte Breite erreicht ist"""
        s = str(s)
        padding = width - len(s)
        if padding > 0:
            return s + " " * padding
        return s
    
    MIN_WIDTH = 8
    if headers == 0:
        headers = list(dict_array[0].keys())
    
    # Maximale Breite für jede Spalte berechnen
    col_widths = {}
    for header in headers:
        header_str = format_value(header)
        col_widths[header] = max(len(header_str), MIN_WIDTH)
        # Prüfe alle Werte in dieser Spalte
        for d in dict_array:
            value_str = format_value(d.get(header, ''))
            col_widths[header] = max(col_widths[header], len(value_str))
    
    # Kopfzeile erstellen
    header_row = '|'
    for header in headers:
        header_str = format_value(header)
        header_row += ' ' + pad_string(header_str, col_widths[header]) + ' |'
    print(header_row)
    
    # Trennzeile erstellen
    separator = '|'
    for header in headers:
        separator += ' ' + ('-' * col_widths[header]) + ' |'
    print(separator)
    
    # Datenzeilen erstellen
    for d in dict_array:
        row = '|'
        for header in headers:
            value = format_value(d.get(header, ''))
            row += ' ' + pad_string(value, col_widths[header]) + ' |'
        print(row)

def blinkIntern(seconds=0.5, pin=4):  # blink with intern LED
    led = machine.Pin(pin, machine.Pin.OUT)
    led.value(1)
    utime.sleep(seconds)
    led.value(0)

def machineId():
    return binascii.hexlify(machine.unique_id()).decode()

def toHash(data="Hallo Welt", algorithm="sha256"):
    """Berechnet den Hash einer gegebenen Datenmenge.
    Args:
        data (bytes): Die Daten, für die der Hash berechnet werden soll.
        algorithm (str, optional): Der zu verwendende Hash-Algorithmus. Defaults to "sha256".
    Returns:
        str: Der hexadezimale Hash-Wert.
    """
    hash_obj = getattr(hashlib, algorithm)()
    hash_obj.update(data)
    return hash_obj.hexdigest()

def yms(mytime=0):  # -> 20241232235959
    if mytime == 0:
        # Get the current time
        mytime = utime.localtime()
    formatted_time = "{}{:02d}{:02d}{:02d}{:02d}{:02}".format(mytime[0], mytime[1], mytime[2], mytime[3], mytime[4], mytime[5])  
    return formatted_time

def YmdHms(mytime=0):  # -> 2024-12-31 23:59:59
    if mytime == 0:
        # Get the current time
        mytime = utime.localtime()
    formatted_time = "{}-{:02d}-{:02d} {:02d}:{:02d}:{:02}".format(mytime[0], mytime[1], mytime[2], mytime[3], mytime[4], mytime[5])  
    return formatted_time



