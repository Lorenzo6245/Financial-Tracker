from numpy import nan_to_num
from customtkinter import *
import manageStocks

labels = []
Hlabels = []

remover = manageStocks.RemoveStock()
history = manageStocks.addHistory()
manager = manageStocks.AddStock()

balance = manageStocks.getBalance()

def updateBalance():
    balance = manageStocks.getBalance()
    L_Balance.configure(text = f"Balance: {balance}")

def addStock():
    in_BT = CTkInputDialog(text = "Insert when you bought the stocks:\n(dd/mm/yyyy hh:mm)", title = " Time")
    manager.BuyTime = in_BT.get_input()
    in_C = CTkInputDialog(text = "Insert the name of the company/cripto:", title = " Company/Cripto")
    manager.Company = in_C.get_input()
    in_NS = CTkInputDialog(text = "Insert the number of stocks:", title = " Number of Stocks")
    manager.NStocks = in_NS.get_input()
    in_V = CTkInputDialog(text = "Insert the value of a single stock:", title = " Value")
    manager.Value = float(in_V.get_input().replace(",", ".")) * float(manager.NStocks)
    manager.Index = manageStocks.get_Index_Man() + 1

    if manager.BuyTime != None and manager.Value != None and manager.Company != None and manager.NStocks != None:
        manager.addStock()
        updatePending()

def removeStock():
    in_I = CTkInputDialog(text = "Insert the index of the investment", title = " Index")
    remover.Index = int(in_I.get_input())
    in_ST = CTkInputDialog(text = "Insert when you sold the stocks:\n(dd/mm/yyyy hh:mm)", title = " Time")
    history.SellTime = in_ST.get_input()
    in_SP = CTkInputDialog(text = "Insert the price at which you sold a single stock:", title = " Sell Price")
    history.NStocks = manageStocks.readSingleRow("Man", int(remover.Index))[4]
    history.Revenue = float(in_SP.get_input().replace(",", ".")) * float(history.NStocks) - float(manageStocks.readSingleRow("Man", int(remover.Index))[2])
    history.BuyTime = manageStocks.readSingleRow("Man", int(remover.Index))[1]
    history.Company = manageStocks.readSingleRow("Man", int(remover.Index))[3]
    history.Index = manageStocks.get_Index_His() + 1

    if remover.Index != None and history.SellTime != None:
        history.add()
        remover.removeStock()

    manageStocks.updateIndexes()
    updatePending()
    updateHistory()
    updateBalance()


def updatePending():
    for label in labels:
        label.destroy()
    labels.clear()
    label = CTkLabel(SF_Pending, text = "  BuyTime, Value, Company, NStocks", font = ("Calibri_Light", 15), wraplength = 400)
    label.pack(pady = 2, anchor = "n")
    labels.append(label)
    for i in range(int(manageStocks.get_Index_Man())):
        label = CTkLabel(SF_Pending, text = ", ".join(str(item) for item in manageStocks.readSingleRow("Man", i + 1)), font = ("Calibri_Light", 15), wraplength = 400)
        label.pack(pady = 1, anchor = "n")
        labels.append(label)
    if manageStocks.managerempty() == False:
        SF_Pending.place(rely = 0.6, relx = 0.47, anchor = "e")

def updateHistory():
    for label in Hlabels:
        label.destroy()
    Hlabels.clear()
    label = CTkLabel(SF_History, text = "  SellTime, BuyTime, Revenue, Company, NStocks", font = ("Calibri_Light", 15), wraplength = 400)
    label.pack(pady = 2, anchor = "n")
    Hlabels.append(label)
    for i in range(int(manageStocks.get_Index_His())):
        label = CTkLabel(SF_History, text = ", ".join(str(item) for item in manageStocks.readSingleRow("His", i + 1)), font = ("Calibri_Light", 15), wraplength=400)
        label.pack(pady = 1, anchor = "n")
        Hlabels.append(label)
    if manageStocks.historyempty() == False:
        SF_History.place(rely = 0.6, relx = 0.53, anchor = "w")
    if manageStocks.managerempty() == False:
        SF_Pending.place(rely = 0.6, relx = 0.47, anchor = "e")
    
def clearHis():
    history.clear()
    updateHistory()
    updateBalance()

root = CTk(className = " Finacial Tracker - by Lorga - based on Financial Tracker by FireBlaze360308")
root.geometry("900x700")

B_AddNewStock = CTkButton(root, text = "Add New Stock", font = ("Calibri_Light", 20), fg_color = "#3adb00", hover_color = "#2a9c02", text_color = "black", command = addStock)
B_AddNewStock.place(rely = 0.2, relx = 0.35, anchor = "ne")

B_RemoveStock = CTkButton(root, text = "Investment Completed", font = ("Calibri_Light", 20), fg_color = "#3adb00", hover_color = "#2a9c02", text_color = "black", command = removeStock)
B_RemoveStock.place(rely = 0.2, relx = 0.65, anchor = "nw")

B_ClearHis = CTkButton(root, text = "Clear History", font = ("Calibri_Light", 20), text_color = "black", fg_color = "#ff0000", hover_color = "#800000", command = clearHis)
B_ClearHis.place(rely = 0.95, relx = 0.5, anchor = "s")

L_Balance = CTkLabel(root, text = f"Balance: {balance}", font = ("Calibri_Light", 20))
L_Balance.place(rely = 0.1, relx = 0.5, anchor = "n")

SF_Pending = CTkScrollableFrame(root, 400, 350)
if manageStocks.managerempty() == False:
    SF_Pending.place(rely = 0.6, relx = 0.47, anchor = "e")
updatePending()

SF_History = CTkScrollableFrame(root, 400, 350)
if manageStocks.historyempty() == False:
    SF_History.place(rely = 0.6, relx = 0.53, anchor = "w")
updateHistory()

root.mainloop()