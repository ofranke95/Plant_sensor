from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend
import gspread
import pandas as pd
from datetime import datetime, timedelta
import time

#MAC-Adress from MiFlora
poller = MiFloraPoller("5C:85:7E:B0:1E:C4",GatttoolBackend)
gc = gspread.service_account()
sheet = gc.open_by_key('1SIVicNq5FcrDpr73jNOlQ6vsvpBnSpLvm0LcGY-FGzQ')
worksheet = sheet.get_worksheet(0)

def check():
        
    moisture = str(poller.parameter_value("moisture"))
    light = str(poller.parameter_value("light"))
    temperature = str(poller.parameter_value("temperature"))
    temperature = temperature.replace(".",",")
    conductivity = str(poller.parameter_value("conductivity"))   
    battery = str(poller.parameter_value("battery"))
    date = datetime.now()
    date = date.strftime("%c")

    data = {"Datum":[date],
            "Temperatur":[temperature],
            "Feuchtigkeit":[moisture],
            "Licht":[light],
            "Leitfähigkeit":[conductivity],
            "Batterie":[battery]
            }

    df = pd.DataFrame(data)
    params = {'valueInputOption': 'USER_ENTERED'}
    body = {'values': df.values.tolist()}
    sheet.values_append(f"Data!A2",params,body)
    
while True:
    check()
    time.sleep(3600)