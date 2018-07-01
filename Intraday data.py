
import pandas as pd
from urllib.request import urlopen
from datetime import datetime as dt
pd.options.mode.chained_assignment = None

Ticker = 'MSFT'
Time = 3 # In minutes
Days = 50 # Max 50 days
Url = 'http://finance.google.com/finance/getprices?' +\
     	'q='+str(Ticker)+'&i='+str(Time*60)+'&p='+str(Days)+'d&f=d,o,h,l,c,v' 
Dff = pd.read_csv(Url,skiprows=7, header=None) # Read Web page in csv format
Dff.columns = ['U_Date','Close','High','Low','Open','Volume']
Dff = Dff[['U_Date','Open','High','Low','Close','Volume']]

Data = urlopen(Url).readlines(150)
Exchange = str(Data[0])[13:][:-3]   
Tim_Zone = str(Data[6])[18:][:-3]

# Date-time (Convert Unix format)
Dff['Date'] = 0.0
for i in range(0,len(Dff)):
    if Dff['U_Date'][i][0]=='a':
        x= Dff['U_Date'][i].replace('a','')
        Dff['Date'][i] = dt.fromtimestamp(int(x)+((int(Tim_Zone)+240)*60))
    else:
        Dff['Date'][i]= dt.fromtimestamp(int(x)+((int(Tim_Zone)+240)*60)+ (int(Dff['U_Date'][i])*60*Time))
Dff.set_index('Date',inplace = True); del Dff['U_Date']

