# retrieve stock market indices from alpha vantage api

import urllib.request, json, ssl, time, calendar

def retrieve_index(index_name):
  request_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
  request_string += index_name
  request_string += "&outputsize=full&apikey=NYDT3BAZT5URMG8S"

  bypasscontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1) # bypass certificate
  
  req = urllib.request.Request(request_string)
  contents = urllib.request.urlopen(req, context=bypasscontext).read()
  contents_string = contents.decode("utf-8")
  contents_json = json.loads(contents_string)

  return contents_json

# indices
INDICES = [
  ["^SPG1200", "S&P GLOBAL 1200"],
  ["^GDOW", "The Global Dow (USD)"],
  ["^W1DOW", "Dow Jones Global Index"],
  ["^GSPTSE", "S&P/TSX"],
  ["^GSPC",	"S&P"],
  ["^DJI", "Dow"],
  ["^IXIC", "Nasdaq"],
  ["^NYA", "NYSE COMPOSITE (DJ)"],
  ["^XAX", "NYSE AMEX COMPOSITE INDEX"],
  ["^BATSK", "BATS 1000 Index"],
  ["^RUT", "Russell 2000"],
  ["^VIX", "Vix"],
  ["^FTSE", "FTSE 100"],
  ["^GDAXI", "DAX"],
  ["^FCHI", "CAC 40"],
  ["^STOXX50E", "ESTX50 EUR P"],
  ["^N100", "EURONEXT 100"],
  ["^BFX", "BEL 20"],
  ["MICEXINDEXCF.ME", "MICEX IND"],
  ["^N225", "Nikkei 225"],
  ["^HSI", "HANG SENG INDEX"],
  ["000001.SS", "SSE Composite Index"],
  ["^STI", "STI Index"],
  ["^AXJO", "S&P/ASX 200"],
  ["^AORD", "ALL ORDINARIES"],
  ["^BSESN", "S&P BSE SENSEX"],
  ["^JKSE", "Jakarta Composite Index"],
  ["^KLSE", "FTSE Bursa Malaysia KLCI"],
  ["^NZ50", "S&P/NZX 50 INDEX GROSS"],
  ["^KS11", "KOSPI Composite Index"],
  ["^TWII", "TSEC weighted index"],
  ["^GSPTSE", "S&P/TSX Composite index"],
  ["^BVSP", "IBOVESPA"],
  ["^MXX", "IPC MEXICO"],
  ["^IPSA", "IPSA SANTIAGO DE CHILE"],
  ["^MERV", "MERVAL BUENOS AIRES"],
  ["^TA100", "TA-125"],
  ["^CASE30", "EGX 30 INDEX"],
  ["JN0U.FGI", "FTSE/JSE TOP 40 USD"],
  ["^NSEI", "NIFTY 50"]
]

index_data = {}

for i in range(len(INDICES)):
  try:
    data = retrieve_index(INDICES[i][0])
    title = data["Meta Data"]["2. Symbol"]
    description = INDICES[i][1]
    daily_data = data["Time Series (Daily)"]
    parsed_data = {}
    
    for key, value in daily_data.items():
      date_time = key + " 00:00:00"
      pattern = "%Y-%m-%d %H:%M:%S"
      utc_epoch = int(calendar.timegm(time.strptime(date_time, pattern)))
      parsed_data[str(utc_epoch)] = float(value["2. high"])
      
    index_data[INDICES[i][1]] = {
      "id": title,
      "name": description,
      "data": parsed_data
    }

    print("SUCCESS: " + INDICES[i][0])
  except KeyError:
    print("FAILURE: " + INDICES[i][0])
  
with open("aggregate_data/training_output.json", 'w') as outfile:
  json.dump(index_data, outfile)

print("done")
