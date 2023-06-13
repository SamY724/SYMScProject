import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import random

plt.style.use('fivethirtyeight')

#Setting seed for reproducibility of code
random.seed(42)


#Loading initial stock data from yahoofinance
#The intervals selected for this project was 1 week
#Other works in the field have opted for a 10-15 year time period, as such given the scope of this work, 10 years was selected

#S&P 500 stocks

amp = yf.download("AMP", start="2010-01-01", end="2021-01-01", interval='1wk')
ivz = yf.download("IVZ", start="2010-01-01", end="2021-01-01", interval='1wk')
trow = yf.download("TROW", start="2010-01-01", end="2021-01-01", interval='1wk')
amg = yf.download("AMG", start="2010-01-01", end="2021-01-01", interval='1wk')
ben = yf.download("BEN", start="2010-01-01", end="2021-01-01", interval='1wk')
blk = yf.download("BLK", start="2010-01-01", end="2021-01-01", interval='1wk')

#FTSE100 Stocks

adm = yf.download("ADM",start="2010-01-01", end="2021-01-01", interval='1wk')
azn = yf.download("AZN",start="2010-01-01", end="2021-01-01", interval='1wk')
tsco = yf.download("TSCO",start="2010-01-01", end="2021-01-01", interval='1wk')
shel = yf.download("SHEL",start="2010-01-01", end="2021-01-01", interval='1wk')
bp = yf.download("BP",start="2010-01-01", end="2021-01-01", interval='1wk')
ba = yf.download("BA",start="2010-01-01", end="2021-01-01", interval='1wk')


#Russell2000 Stocks
bset = yf.download("BSET",start="2010-01-01", end="2021-01-01", interval='1wk')
kmt = yf.download("KMT",start="2010-01-01", end="2021-01-01", interval='1wk')
abm = yf.download("ABM",start="2010-01-01", end="2021-01-01", interval='1wk')
lnn = yf.download("LNN",start="2010-01-01", end="2021-01-01", interval='1wk')
anik = yf.download("ANIK",start="2010-01-01", end="2021-01-01", interval='1wk')
sasr = yf.download("SASR",start="2010-01-01", end="2021-01-01", interval='1wk')


#As we are only interested in the price as our data to calculate averages, dataframes comprising of only the closing price are created
#Inappropriate values are dropped using dropna function, which removes any weeks that do not have adequate numerical values (Not a number)

#S&P 500 Stocks

amp = amp.dropna(axis=0)
ivz = ivz.dropna(axis=0)
trow = trow.dropna(axis=0)
amg = amg.dropna(axis=0)
ben = ben.dropna(axis=0)
blk = blk.dropna(axis=0)

#FTSE100 Stocks

adm = adm.dropna(axis=0)
azn = azn.dropna(axis=0)
tsco = tsco.dropna(axis=0)
shel = shel.dropna(axis=0)
bp = bp.dropna(axis=0)
ba = ba.dropna(axis=0)


#Russell2000 stocks

bset = bset.dropna(axis=0)
kmt = kmt.dropna(axis=0)
abm = abm.dropna(axis=0)
lnn = lnn.dropna(axis=0)
anik = anik.dropna(axis=0)
sasr = sasr.dropna(axis=0)


epsilon = 0.1
target = 0.25


#Now that we have the desired data, and can manipulate it, the algorithm can be constructed

def durationPercentageCalculation(stock,data,origin,totalRewards,dollarReturns):
    
    #Creating a safeguard against a potential full investment cycle
    if origin >= len(data):

        print("Investment has reached final duration, successful cycle completed")
        print(f"The rewards for this complete cycle in USD: $", totalRewards)

    else:
        #Creating lists to store price and pct changes
        x=[]
        y=[]

        #Creating percentage changes and value changes
        z = data["Close"].pct_change()
        v = data["Close"].diff()

        for percentage in z[origin+1:]:
            percentage -= target
            x.append(percentage)
        
        for reward in v[origin+1:]:
            y.append(reward)

        x = np.array(x)
        y = np.array(y)

        #summing the percentage and value changes
        x = x.sum()
        y = y.sum()

        investSelect(stock,data,origin,x,y,totalRewards,dollarReturns)



def investSelect(stock,data,origin,x,y,totalRewards,dollarReturns):

    s = x
    rewards = y

    # Probability function and selecting mechanism

    f = min([epsilon**3*(1-epsilon)**(s/2),1])

    #if F falls below 1, and as such is the minimum selected:

    choices = ['Do','Do not']#there is no try
    weights = [f,1-f]
    selecting = random.choices(choices,weights=weights,k=1)

    

    if selecting == ['Do']:
        if dollarReturns == True:
            totalRewards += (rewards-data["Close"][origin]/data["Close"][origin])
        else:
            totalRewards += rewards-data["Close"][origin]
        origin += 1
        durationPercentageCalculation(stock,data,origin,totalRewards,dollarReturns)

    elif selecting == ['Do not']:
        print(f"Stock:",stock,"Investment Count:",[origin],"total rewards:",round(totalRewards,2),"\n")
        print(f'Probability to invest in next period was: ',f,"\n")
        if dollarReturns == True:
            if origin != 0:
                print(f'Project strategy investment rewards per $1 invested:',round((totalRewards/origin)/origin,2))
        else:
            print(totalRewards)
        
        plotStock(data,origin)
      



# Function used for hyperparameter tuning, by finding the avg change in stock
def stockAvgCalc(stockData,stockName):
    ticker = stockData["Close"].pct_change()
    avg = ticker.mean()
    print(f"The avg change of stock",stockName, "is: ",round(avg,4))



# Simple plotting function to visualise stock performance
def plotStock(data,origin):
    plt.figure(figsize=(14,7))
    plt.title("Performance from after final investment made")
    plt.plot(data["Close"][origin:])
    plt.xlabel("Time")
    plt.ylabel("Value in $")
    plt.show()



if __name__ == "__main__":

    durationPercentageCalculation("AMP",amp,0,0,True)
    durationPercentageCalculation("IVZ",ivz,0,0,True)
    durationPercentageCalculation("TROW",trow,0,0,True)
    durationPercentageCalculation("AMG",amg,0,0,True)
    durationPercentageCalculation("BEN",ben,0,0,True)
    durationPercentageCalculation("BLK",blk,0,0,True)

    durationPercentageCalculation("ADM",adm,0,0,True)
    durationPercentageCalculation("AZN",azn,0,0,True)
    durationPercentageCalculation("TSCO",tsco,0,0,True)
    durationPercentageCalculation("SHEL",shel,0,0,True)
    durationPercentageCalculation("BP",bp,0,0,True)
    durationPercentageCalculation("BA",ba,0,0,True)

    durationPercentageCalculation("BSET",bset,0,0,True)
    durationPercentageCalculation("KMT",kmt,0,0,True)
    durationPercentageCalculation("ABM",abm,0,0,True)
    durationPercentageCalculation("LNN",lnn,0,0,True)
    durationPercentageCalculation("ANIK",anik,0,0,True)
    durationPercentageCalculation("SASR",sasr,0,0,True)
    
    
