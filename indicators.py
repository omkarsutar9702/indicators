#import libraries
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#import data set
df = pd.read_csv("D:\PYTHON\indi\BTC-USD.csv")

#create the function calculate sma and ema 
def sma(data , period=30, column = "Close"):
  return data[column].rolling(window=period).mean()

#calculate ema 
def ema(data , period=20 , column="Close"):
  return data[column].ewm(span=period,adjust=False).mean()

#add this data to dataframe
df["SMA"] = sma(df)
df["EMA"] = ema(df)

#calculate MACD

def macd(data , long_period=25 , short_period=10 , signal=9,column="Close"):
  short_ema=ema(data,short_period,column=column)
  long_ema=ema(data , long_period , column=column)
  data["MACD"] = short_ema - long_ema
  data["signal_line"]=ema(data, signal,column="MACD")
  
  return data
#add data to dataframe
macd(df)

#create the function get reletive strength index
def rsi(data,period=15,column="Close"):
  delta =data[column].diff(1)
  delta = delta[1:]
  up = delta.copy()
  down = delta.copy()
  up[up<0]=0
  down[down>0]=0
  data["up"] = up
  data["down"] = down
  avg_gain = sma(data , period , column="up")
  avg_loss = abs(sma(data,period , column="down"))
  rs = avg_gain / avg_loss
  rsi = 100.0 - (100.0 /(1.0 + rs))
  data["RSI"] = rsi
  
  return data

#add this data to dataframe
rsi(df)

###plot charts
#close price
fig = px.line(df, x='Date', y='Close', title='Time Series of bitcoin')
fig.update_xaxes(rangeslider_visible=True)
fig.show()

#MACD PLOT
fig_macd = px.line(df , x= "Date", y="MACD" , title="macd line")
fig_macd.add_trace(go.Scatter(x=df["Date"], y=df["signal_line"] , mode="lines" , name="signal line"))
fig_macd.show()

#SMA PLOT
fig_sma = px.line(df , x= "Date", y="Close" , title="sma line")
fig_sma.add_trace(go.Scatter(x=df["Date"], y=df["SMA"] , mode="lines" , name="sma line"))
fig_sma.show()

#EMA PLOT
fig_ema = px.line(df , x= "Date", y="Close" , title="ema line")
fig_ema.add_trace(go.Scatter(x=df["Date"], y=df["EMA"] , mode="lines" , name="ema line"))
fig_ema.show()

#ema and sma plot
fig_ema_sma = px.line(df , x= "Date", y="Close" , title="ema and sma line")
fig_ema_sma.add_trace(go.Scatter(x=df["Date"], y=df["SMA"] , mode="lines" , name="sma line"))
fig_ema_sma.add_trace(go.Scatter(x=df["Date"], y=df["EMA"] , mode="lines" , name="Ema line"))
fig_ema_sma.show()

#rsi plot
fig_rsi = px.line(df, x="Date" , y="RSI" , title="RSI LINE")
fig_rsi.show()









