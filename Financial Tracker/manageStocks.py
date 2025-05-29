from numpy import array, nan_to_num
from pandas import read_csv
from pathlib import Path

Currentfilepath = str(Path(__file__).parent.resolve()) + "\\StockManager.csv"
Historyfilepath = str(Path(__file__).parent.resolve()) + "\\StockHistory.csv"

def get_Index_Man():
    df = read_csv(Currentfilepath)
    maxClm = nan_to_num(df['index'].max())
    return int(maxClm)

def get_Index_His():
    df = read_csv(Historyfilepath)
    maxClm = nan_to_num(df['index'].max())
    return int(maxClm)

def readStockManager():
    with open(Currentfilepath, 'r') as f:
        x = f.read()
        f.close()
    
    return x

def readStockHistory():
    with open(Historyfilepath, 'r') as f:
        x = f.read()
        f.close()
    
    return x

def historyempty():
    if readStockHistory() == "index, SellTime, BuyTime, Revenue, Company, NStocks":
        return True
    else:
        return False
    
def managerempty():
    if readStockManager() == "index, BuyTime, Value, Company, NStocks":
        return True
    else:
        return False

def readSingleRow(HisOrMan, nRow):
    x = []
    if HisOrMan == "His":
        with open(Historyfilepath, 'r') as f:
            for row in f.readlines():
                x.append(row.strip().split(','))
            f.close()
    elif HisOrMan == "Man":
        with open(Currentfilepath, 'r') as f:
            for row in f.readlines():
                x.append(row.strip().split(','))
            f.close()
    
    return x[nRow]

def getBalance():
    balance = 0
    for x in range(get_Index_His()):
        balance += float(readSingleRow("His", x + 1)[3])
    return balance

def updateIndexes():
    df = read_csv(Currentfilepath)
    df['index'] = range(1, len(df) + 1)
    df.to_csv(Currentfilepath, index=False)

class AddStock():
    global Currentfilepath
    def __init__(self):
        self.BuyTime = "dd/mm/yyyy hh:mm"
        self.Value = 0.0
        self.Company = "None"
        self.NStocks = 0.0
        self.Index = 0
    
    def addStock(self):
        with open(Currentfilepath, 'a') as save:
            save.write(f"\n{int(self.Index)}, {self.BuyTime}, {self.Value}, {self.Company}, {self.NStocks}")
            save.close()

class RemoveStock():
    global Currentfilepath
    def __init__(self):
        self.Index = 0
    
    def removeStock(self):
        f = read_csv(Currentfilepath)
        f = f[f['index'] != self.Index]
        f.to_csv(Currentfilepath, index=False)

class addHistory():
    global Historyfilepath
    def __init__(self):
        self.Company = "None"
        self.NStocks = 0.0
        self.Revenue = 0.0
        self.BuyTime = "dd/mm/yyyy hh:mm"
        self.SellTime = "dd/mm/yyyy hh:mm"
        self.Index = 0
    
    def add(self):
        with open(Historyfilepath, 'a') as his:
            his.write(f"\n{self.Index}, {self.SellTime}, {self.BuyTime}, {self.Revenue}, {self.Company}, {self.NStocks}")
            his.close()
    
    def clear(self):
        with open(Historyfilepath, 'r+') as his:
            his.seek(0)
            his.truncate()
            his.write("index, SellTime, BuyTime, Revenue, Company, NStocks")
            his.close()