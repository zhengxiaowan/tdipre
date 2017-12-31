from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import requests 
import simplejson as json
import datetime
from bokeh.plotting import figure, output_file, show
from bokeh import embed

app = Flask(__name__)

# Load the dataset
def loaddata(name):
    dictionary = {'api_key':'XyT1FY3chW_8gD_g4ytW', 'date.lt':'2017-11-30', 'date.gt':'2017-11-01', 'ticker':name}
    r = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json', params=dictionary)
    x = r.json()
    df=pd.DataFrame(x['datatable']['data'])
    df.columns = pd.DataFrame(x['datatable']['columns'])['name']
    dfnew=df[['ticker','date','open','high','low','close']]
    return dfnew


@app.route('/',methods=['GET','POST'])
def index():
#  return render_template('index.html')

    if request.method == 'GET':
        return render_template('index.html')
    else:
        name=request.form['name']
        name2=str(name)
        feature=request.form.getlist('feature')
        featurenumber=len(feature)
        if (name2=='' or featurenumber==0):
            return 'Wrong input, please check!'
        else:
            dfnew=loaddata(name)
            x1=dfnew[dfnew['ticker']==name]['date'].values.tolist()
            x=[datetime.datetime.strptime(i, '%Y-%m-%d') for i in x1]
            y=[1,2,3,4]
            for i in range(0, featurenumber):
                y[i]=dfnew[dfnew['ticker']==name][feature[i]].values.tolist()
            p = figure(title=name, x_axis_label='Date', y_axis_label='Price', x_axis_type="datetime")
            color=['blue','green','red','orange']
            for i in range(0,featurenumber):
                p.line(x, y[i], line_width=2, line_color=color[i], legend=feature[i])    
            # Embed plot into HTML via Flask Render
            script, div = embed.components(p)
            #show(p)
            return render_template('graph.html', script=script, div=div)
    

if __name__ == '__main__':
  app.run(port=33507)
