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
        df = dataFrame.copy()

        df["DeliverableQty_Numeric"] = pd.to_numeric(df["DeliverableQty"].str.replace(",", ""), errors='coerce')
        df["ClosePrice_numeric"] = pd.to_numeric(df["ClosePrice"].str.replace(",", ""), errors='coerce')


        df["DeliverableQty_Numeric"] = df["DeliverableQty_Numeric"].fillna(0).astype(np.int64)
        df["ClosePrice_numeric"] = df["ClosePrice_numeric"].fillna(0).astype(np.float64)

        df["Date_time"] = pd.to_datetime(df["Date"], format="%d-%b-%Y")
        df["weekday"] = df["Date_time"].dt.day_name()

        df = df[["Symbol", "Date_time", "DeliverableQty_Numeric", "weekday","ClosePrice_numeric"]]

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


def get_day_wise_diff_closePrice(dataFrame):
   list_of_diff=[]
   non_saturday_df = dataFrame[(dataFrame['weekday'] != 'Saturday')]
   if non_saturday_df.shape[0]==0 :
      return ([],[])
   for i in range(non_saturday_df.shape[0]-1 ):
      list_of_diff.append(abs(float(non_saturday_df.iloc[i]["ClosePrice_numeric"]-non_saturday_df.iloc[i+1]["ClosePrice_numeric"])))
   return list_of_diff
      
def get_week_wise_diff_closePrice(dataFrame):
    list_of_diff=[]
    
    check=False
    non_saturday_df = dataFrame[(dataFrame['weekday'] != 'Saturday')]
    if non_saturday_df.shape[0]==0 :
      return ([],[])
    current_year,current_week,_=non_saturday_df.iloc[0]["Date_time"].date().isocalendar()
    curr_val=non_saturday_df.iloc[0]["ClosePrice_numeric"]
   

    for i in range(non_saturday_df.shape[0]):
        next_year,next_weak,_=non_saturday_df.iloc[i]["Date_time"].date().isocalendar()
        next_val=non_saturday_df.iloc[i]["ClosePrice_numeric"]


        if current_year==next_year and current_week==next_weak :
           check=False
        else:
            list_of_diff.append(abs(float(next_val-curr_val)))
            current_year=next_year
            current_week=next_weak
            curr_val=next_val
            check=True

           
    if not check:
      list_of_diff.append(abs(float(next_val-curr_val)))
    
    return list_of_diff
    
def get_month_wise_diff_closePrice(dataFrame,chance):
    list_of_diff=[]
    month=0
    check=False
    non_saturday_df = dataFrame[(dataFrame['weekday'] != 'Saturday')]
    if non_saturday_df.shape[0]==0 :
      return ([],[])
    
    current_year,current_month,curr_val=non_saturday_df.iloc[0]["Date_time"].date().year,non_saturday_df.iloc[0]["Date_time"].date().month,non_saturday_df.iloc[0]["ClosePrice_numeric"]

    for i in range(non_saturday_df.shape[0]):


        next_year,next_month=non_saturday_df.iloc[i]["Date_time"].date().year,non_saturday_df.iloc[i]["Date_time"].date().month
        next_val=non_saturday_df.iloc[i]["ClosePrice_numeric"]


        if current_year==next_year and current_month==next_month :
             check=False
        else:
          month+=1
          if month==chance:
             list_of_diff.append(abs(float(next_val-curr_val)))
             curr_val=next_val
             current_year=next_year
             current_month=next_month
        
             month=0
             check=True
          else :
              current_year=next_year
              current_month=next_month
             
          
    if not check:
      list_of_diff.append(abs(float(next_val-curr_val)))
 
    return list_of_diff

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
    ClosePrice_numeric=global_db["ClosePrice_numeric"].tolist()

    average_val=np.average(global_db["DeliverableQty_Numeric"]).item()
    average_val_list=[average_val]*len(y)
    closePriceData=get_day_wise_diff_closePrice(global_db)

    return jsonify({'x': x, 'y': y,'Date_time':Date_time,'DeliverableQty_Numeric':DeliverableQty_Numeric,"weekday":weekday,"ClosePrice_numeric":ClosePrice_numeric,"averageVal":average_val_list,"closePriceData":closePriceData})

@app.route('/api/fetch-data-filter', methods=['GET','POST'])
@cross_origin()
def fetch_data_filter_endpoint():
    data = request.json
    print(data)
    filter_range = data['filter_range']
    val = int(data['val'])
    global_db=pd.DataFrame({'Date_time':data['Date_time'],'weekday':data['weekday'],'DeliverableQty_Numeric':data['DeliverableQty_Numeric'],'ClosePrice_numeric':data['ClosePrice_numeric']})
    Date_time=global_db["Date_time"].tolist()
    DeliverableQty_Numeric=global_db["DeliverableQty_Numeric"].tolist()
    ClosePrice_numeric=global_db["ClosePrice_numeric"].tolist()

    weekday=global_db["weekday"].tolist()
    global_db["Date_time"]=pd.to_datetime(global_db["Date_time"])
    x,y=[],[]
    if filter_range=='week':
      x,y= get_week(global_db)
      y = list(map(int, y))
      closePriceData=get_week_wise_diff_closePrice(global_db)

      
     

    
    elif filter_range=='Daily':
          x=list(map(lambda x:x.strftime("%d-%b-%y"),global_db["Date_time"]))
          y=global_db["DeliverableQty_Numeric"].to_list()
          closePriceData=get_day_wise_diff_closePrice(global_db)

    else :
         x,y= get_month(global_db,val)


         y = list(map(int, y))
         closePriceData=get_month_wise_diff_closePrice(global_db,val)

    average_val=np.average(global_db["DeliverableQty_Numeric"]).item()
    average_val_list=[average_val]*len(y)
    
    return jsonify({'x': x, 'y': y,'Date_time':Date_time,'DeliverableQty_Numeric':DeliverableQty_Numeric,"weekday":weekday,"ClosePrice_numeric":ClosePrice_numeric,"avaerageVal":average_val_list,"closePriceData":closePriceData})

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
    
