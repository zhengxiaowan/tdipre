from flask import Flask, render_template, request, redirect
import pandas as pd
import requests 
import simplejson as json
import datetime
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
#  return render_template('index.html')

    if request.method == 'GET':
        return render_template('index.html')
    else:
        name=request.form['name']        
        selected = request.form['plot']
        #selected = str(selected)
        dictionary = {'api_key':'XyT1FY3chW_8gD_g4ytW', 'date.lt':'2017-11-30', 'date.gt':'2017-11-01'}
        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json', params=dictionary)
        x = r.json()
        df=pd.DataFrame(x['datatable']['data'])
        df.columns = pd.DataFrame(x['datatable']['columns'])['name']
        dfnew=df[['ticker','date','open','high','low','close']]
        x1=dfnew[dfnew['ticker']==name]['date'][0]
        y=dfnew[dfnew['ticker']==name][selected][0]            
        return y

if __name__ == '__main__':
  app.run(port=33507)
