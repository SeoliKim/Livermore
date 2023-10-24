# main branch empty file holder
# region imports
from AlgorithmImports import *
# endregion

class MeanReversionAlgorithm(QCAlgorithm):
    
    def Initialize(self) -> None:
        # Basic Setup
        self.SetStartDate(2021, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(1000000)

        # Parameter
        self.period = 50 # hr
        self.resolution= Resolution.Hour
        self.lookback_period = 10
        self.buy_threshold = -2  # Z-score threshold to buy
        self.sell_threshold = 2  # Z-score threshold to sell

        # dictionaries
        self.smas={}
        self.stds= {}

        # stocks
        self.tickers= [
            "PG",
            "JNJ",
            "KO",
            "PEP",
            "MCD",            
            "V",
            "MA"
        ]

        for t in self.tickers:
            self.AddEquity(t, self.resolution)
            self.smas[t] = self.SMA(t, self.period, self.resolution) 
            self.stds[t]= self.STD(t,self.period)
            
        
        self.Debug(self.smas)
        
    def OnData(self, slice):
        if not slice.HasData:
            return
        
        for ticker in self.tickers:
            bar = slice.Bars.get(ticker)
            if bar:
                self.smas[ticker].Update(bar.EndTime, bar.Close)
                self.stds[ticker].Update(bar.EndTime, bar.Close)

                if self.smas[ticker].IsReady and self.stds[ticker].IsReady:
                    # Calculate the mean and standard deviation
                    close_price = bar.Close
                    mean = self.smas[ticker].Current.Value
                    std= self.stds[ticker].Current.Value

                    # Calculate the Z-score
                    z_score = (close_price - mean) / std

                    if z_score < self.buy_threshold:
                        # Buy signal: Z-score is below the buy threshold
                        self.SetHoldings(ticker, 1.0)
                    elif z_score > self.sell_threshold:
                        # Sell signal: Z-score is above the sell threshold
                        if self.Portfolio[ticker].Invested:
                            # If ticker is in the portfolio, sell it
                            self.SetHoldings(ticker, 0)
                    
