from flask import Flask, request, jsonify
from nselib import capital_market
import pandas as pd
import numpy as np
import os
from flask_cors import CORS,cross_origin
app = Flask(__name__)
CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'
global_db=None
def give_strctured(dataFrame):
   DeliverableQty_numeric=[]
   
   df=dataFrame.copy()
   for i in (df["DeliverableQty"].str.split(",")):
      DeliverableQty_numeric.append("".join(i))
   df["DeliverableQty_Numeric"]=DeliverableQty_numeric
   df["DeliverableQty_Numeric"]=df["DeliverableQty_Numeric"].astype(np.int64)
   df["Date_time"]=pd.to_datetime(dataFrame["Date"],format="%d-%b-%Y")
   df["weekday"]=list(map(lambda x:x.day_name(),df["Date_time"]))

   df=df[["Symbol","Date_time","DeliverableQty_Numeric","weekday"]]

   return df


def fetch_data(symbol, from_date, to_date):
    # Simulate fetching data
    global global_db
    df = capital_market.price_volume_and_deliverable_position_data(symbol, from_date, to_date)
    
   
    new_df=give_strctured(df)
    global_db=new_df
    x=list(map(lambda x:x.strftime("%d-%b-%y"),new_df["Date_time"]))
    print(x)
    y=new_df["DeliverableQty_Numeric"].to_list()
    return x,y
def get_week(dataFrame):
    week_dict={}
    week=1
    sum=0
    non_saturday_df = dataFrame[(dataFrame['weekday'] != 'Saturday')]
    if non_saturday_df.shape[0]==0 :
      return ([],[])
    date_range=non_saturday_df.iloc[0]["Date_time"].date().strftime("%d-%B-%Y")


    for i in range(non_saturday_df.shape[0]-1):

        weekday=non_saturday_df.iloc[i]["weekday"]

        current_year,current_weak,_=non_saturday_df.iloc[i]["Date_time"].date().isocalendar()
        next_year,next_weak,_=non_saturday_df.iloc[i+1]["Date_time"].date().isocalendar()


        date_range_iter=non_saturday_df.iloc[i]["Date_time"].date().strftime("%d-%B-%Y")
        val=non_saturday_df.iloc[i]["DeliverableQty_Numeric"]


        if current_year==next_year and current_weak==next_weak :
           sum+=val
        else:
          sum+=val
        
          date_range=date_range+" - "+date_range_iter
          week_dict.update({f'{date_range}':sum})
          date_range=non_saturday_df.iloc[i+1]["Date_time"].date().strftime("%d-%B-%Y")
          week+=1
          sum=0
    if sum!=0:
      val=non_saturday_df.iloc[non_saturday_df.shape[0]-1]["DeliverableQty_Numeric"]
      sum+=val
      date_range=date_range+" - "+non_saturday_df.iloc[non_saturday_df.shape[0]-1]["Date_time"].date().strftime("%d-%B-%Y")
      week_dict.update({f'{date_range}':sum})
      week+=1
    return (list(week_dict.keys()),list(week_dict.values()))

def get_month(dataFrame,chance):
    month_dict={}
    month=0
    sum=0
    non_saturday_df = dataFrame[(dataFrame['weekday'] != 'Saturday')]
    if non_saturday_df.shape[0]==0 :
      return ([],[])
    date_range=non_saturday_df.iloc[0]["Date_time"].date().strftime("%d-%B-%Y")


    for i in range(non_saturday_df.shape[0]-1):


        current_year,current_month=non_saturday_df.iloc[i]["Date_time"].date().year,non_saturday_df.iloc[i]["Date_time"].date().month
        next_year,next_month=non_saturday_df.iloc[i+1]["Date_time"].date().year,non_saturday_df.iloc[i+1]["Date_time"].date().month


        date_range_iter=non_saturday_df.iloc[i]["Date_time"].date().strftime("%d-%B-%Y")
        val=non_saturday_df.iloc[i]["DeliverableQty_Numeric"]


        if current_year==next_year and current_month==next_month :

           sum+=val
        else:
          month+=1
          if month==chance:
            sum+=val
            date_range=date_range+" - "+date_range_iter
            month_dict.update({f'{date_range}':sum})
            date_range=non_saturday_df.iloc[i+1]["Date_time"].date().strftime("%d-%B-%Y")
            month=0
            sum=0
          else:
            sum+=val
    if sum!=0:

      val=non_saturday_df.iloc[non_saturday_df.shape[0]-1]["DeliverableQty_Numeric"]
      sum+=val

      date_range=date_range+" - "+non_saturday_df.iloc[non_saturday_df.shape[0]-1]["Date_time"].date().strftime("%d-%B-%Y")
      month_dict.update({f'{date_range}':sum})

    return (list(month_dict.keys()),list(month_dict.values()))
@app.route('/', methods=['GET'])
@cross_origin()
def root():
    return 'Hello world'


@app.route('/api/fetch-data', methods=['GET','POST'])
@cross_origin()
def fetch_data_endpoint():
    data = request.json
    print(data)
    symbol = data['symbol']
    from_date = data['from_date']
    to_date = data['to_date']
    x, y = fetch_data(symbol, from_date, to_date)
    Date_time=global_db["Date_time"].tolist()
    DeliverableQty_Numeric=global_db["DeliverableQty_Numeric"].tolist()
    weekday=global_db["weekday"].tolist()
    return jsonify({'x': x, 'y': y,'Date_time':Date_time,'DeliverableQty_Numeric':DeliverableQty_Numeric,"weekday":weekday})

@app.route('/api/fetch-data-filter', methods=['GET','POST'])
@cross_origin()
def fetch_data_filter_endpoint():
    data = request.json
    print(data)
    filter_range = data['filter_range']
    val = int(data['val'])
    global_db=pd.DataFrame({'Date_time':data['Date_time'],'weekday':data['weekday'],'DeliverableQty_Numeric':data['DeliverableQty_Numeric']})
    Date_time=global_db["Date_time"].tolist()
    DeliverableQty_Numeric=global_db["DeliverableQty_Numeric"].tolist()
    weekday=global_db["weekday"].tolist()
    global_db["Date_time"]=pd.to_datetime(global_db["Date_time"])
    x,y=[],[]
    if filter_range=='week':
      x,y= get_week(global_db)
      y = list(map(int, y))
    
    elif filter_range=='Daily':
          x=list(map(lambda x:x.strftime("%d-%b-%y"),global_db["Date_time"]))
          y=global_db["DeliverableQty_Numeric"].to_list()
    else :
         x,y= get_month(global_db,val)

         y = list(map(int, y))
    return jsonify({'x': x, 'y': y,'Date_time':Date_time,'DeliverableQty_Numeric':DeliverableQty_Numeric,"weekday":weekday})

@app.route('/api/dummy', methods=['GET','POST'])
@cross_origin()
def dummy():
    data = request.json
    print(data)
    x = data['x']
    y = data['y']
    return jsonify({'x': x, 'y': y})
    

if __name__ == "__main__":
    port = int(os.getenv('PORT', 4000))
    app.run(debug=True,port=port,host='0.0.0.0')
    
