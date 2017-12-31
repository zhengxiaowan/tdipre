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
        #open_value = request.form['open']
        #close_value = request.form['close']
        #high_value = request.form['high']
        #low_value = request.form['low']
        selected=request.form['plot']
        dictionary = {'api_key':'XyT1FY3chW_8gD_g4ytW', 'date.lt':'2017-11-30', 'date.gt':'2017-11-01'}
        r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json', params=dictionary)
        x = r.json()
        df=pd.DataFrame(x['datatable']['data'])
        df.columns = pd.DataFrame(x['datatable']['columns'])['name']
        dfnew=df[['ticker','date','open','high','low','close']]
        x1=dfnew[dfnew['ticker']==name]['date'].values.tolist()
        y=dfnew[dfnew['ticker']==name][selected].values.tolist()
        x=[datetime.datetime.strptime(i, '%Y-%m-%d') for i in x1]
        output_file('result.htm')
        p = figure(title="Price Graph", x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime")
        p.line(x, y, line_width=2)
        show(p)
        return result.htm

if __name__ == '__main__':
  app.run(port=33507)
