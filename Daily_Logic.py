
# coding: utf-8

# In[4]:

import MySQLdb


# In[24]:

# Open database connection
db = MySQLdb.connect("localhost","root","","dbtest1",unix_socket="/opt/lampp/var/mysql/mysql.sock" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()

print ("Database version : %s " % data)

# disconnect from server
#db.close()


# In[13]:




# # Discount Logic (on top of analysis)

# ### Modified slack w/ Wastage, Forecast, Clearance 

# In[1]:

import copy 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Dataset=pd.read_csv("SuperUltraData.csv")


# In[2]:

df=Dataset[['RETAIL_OUTLET_NUMBER','BASE_PRODUCT_NUMBER','CALENDAR_DATE','REDUCED_SALES_SINGLES_QTY','EXPECTED_DAILY_SALES_QTY','ACTUAL_SALES_SINGLES','ADJUSTED_SALES_SINGLES','Delivery_Date','Code_Life_Days','Revised_Order_Qty',]]


# In[3]:

def getInt(s):
    if(s=='?'):
        return 0
    else:
        return int(s)


# In[ ]:

uniProduct = Dataset['BASE_PRODUCT_NUMBER'].unique()


# In[ ]:

def groupSales():
    """exp->list of expectated sales for a unique product....
    expSales->list of exp's for all unique products...
    """
    group_Prod = list(Dataset['BASE_PRODUCT_NUMBER'].groupby(Dataset['RETAIL_OUTLET_NUMBER']))
    uniProduct = Dataset['BASE_PRODUCT_NUMBER'].unique()

    expSales = []
    actSales = []
    calrDate = []
    codeLife = []
    orderQty = []

    for i in range(1,2):
        for r in range(len(uniProduct)):
            exp = []
            act = []
            adj = []
            calr= []
            code = []
            order = []
            
            for k in range(len(group_Prod[i][1])):#this len() here gives number of product in that ith store
                l = str(group_Prod[i][1].iloc[[k]]).split(" ")
                j = int(l[0])#row number of that product in the original table

                if(int(uniProduct[r]) == df['BASE_PRODUCT_NUMBER'][j]):
                    if(df['EXPECTED_DAILY_SALES_QTY'][j]=='NaN'):
                        exp.append(0)
                        calr.append(df['CALENDAR_DATE'][j])
                    else:
                        exp.append(df['EXPECTED_DAILY_SALES_QTY'][j])
                        calr.append(df['CALENDAR_DATE'][j])
                        

                    if(df['ACTUAL_SALES_SINGLES'][j] == 'NaN'):
                        act.append(0)
                    else:
                        act.append(df['ACTUAL_SALES_SINGLES'][j]+df['REDUCED_SALES_SINGLES_QTY'][j])
                        
                    code.append(df['Code_Life_Days'][j])
                    order.append(df['Revised_Order_Qty'][j])
                    
            expSales.append(exp)
            actSales.append(act)
            calrDate.append(calr)
            codeLife.append(code)
            orderQty.append(order)
            
           
    return expSales, actSales,  calrDate, codeLife, orderQty 
#-----------------------------------------------------------

expSales, actSales,  calrDate , codeLife, orderQty = groupSales()


# In[ ]:

def getWeekDay(calrDate):
    from datetime import datetime, timedelta

    mytime=[]
    
    for i in range(len(calrDate)):
        tempTime = []
        for j in range(len(calrDate[i])):
            tempTime.append((datetime.strptime(str(calrDate[i][j]),"%m/%d/%Y")).strftime("%A"))
        mytime.append(tempTime)
    return mytime
#-----------------------------

mytime = getWeekDay(calrDate)


# In[ ]:

def getWastage(actSales,orderQty,codeLife):
    
    wastage = []
    r = len(actSales)
    for i in range(r):
        waste = [0]*len(actSales[i]);
        for j in range(len(actSales[i])):
            c = getInt(codeLife[i][j])
            stock = getInt(orderQty[i][j])
            for k in range(j, c+j):
                if(k < len(actSales[i])):
                    if(stock > actSales[i][k]):
                        stock -= actSales[i][k]
                        actSales[i][k] = 0
                    else:
                        actSales[i][k] -= stock
                        stock = 0
                        break
            if(stock > 0  and j+c-1 < len(actSales[i])):
                waste[j+c-1] = stock
        wastage.append(waste);
    return wastage
#-----------------------------------
 
wastage=getWastage(copy.deepcopy(actSales),orderQty,codeLife)


# In[ ]:

def getSlack(expsales, actSales):
    slack = []
    for i in range(len(expsales)):
        if len(expsales[i]) != 0:
            slack.append([x-y for x,y in zip(expsales[i],actSales[i])])
        else:
            slack.append([])
    return slack
#-------------------------

slack = getSlack(expSales, actSales)


# In[ ]:

def getActualSlack(slack,wastage):
    actSlack = []
    for i in range(len(slack)):
        if len(slack[i]) != 0:
            actSlack.append([x-y for x,y in zip(slack[i],wastage[i])])
        else:
            actSlack.append([])
    return actSlack


# In[ ]:

actSlack=getActualSlack(slack,wastage)


# In[ ]:

def getCumSlack(slack):
    cumSlack = []
    for i in range(len(slack)):
        if len(slack[i]) != 0:
            tempSlack = slack[i]
            for j in range(len(slack[i])-1):
                tempSlack[j+1] += tempSlack[j]
            cumSlack.append(tempSlack)
        else:
            cumSlack.append([])
    return cumSlack
#------------------------------------

cumSlack=getCumSlack(copy.deepcopy(actSlack))


# #### Actual Slack -- taking into account of wastage due to expiry

# In[ ]:

# for i in range(len(actSlack)):
#     if len(actSlack[i])!=0:
#         plt.plot(actSlack[i])
#         plt.ylabel('actSlack')
#         plt.show()


# #### Cumulative Slack -- taking into account of wastage due to expiry

# In[ ]:

# for i in range(len(cumSlack)):
#     if len(cumSlack[i])!=0:
#         plt.plot(cumSlack[i])
#         plt.ylabel('cumSlack')
#         plt.show()


# In[ ]:

def level(a):
    if(a < 0):
        return 0
    else:
        return a


# In[ ]:

def getSlackPercent(cumSlack, orderQty):
    slackPercent = []
    for i in range(len(cumSlack)):
        slackPer = []
        for j in range(len(cumSlack[i])):
            if(level(cumSlack[i][j])==0):
                slackPer.append(0)
            else:
                slackPer.append((level(cumSlack[i][j]) / (level(cumSlack[i][j]) + getInt(orderQty[i][j]))) * 100)
        slackPercent.append(slackPer)
    return slackPercent
#-------------------------------------

slackPercentage = getSlackPercent(cumSlack, orderQty)


# In[ ]:

### Mystery
# for i in range(len(cumSlack)):
#     if len(cumSlack[i]) != len(orderQty[i]):
#         print(str(i)+"----------------"+str(len(cumSlack[i]))+"-------------"+str(len(orderQty[i])))


# #### Slack Percentage Plots

# In[ ]:

for i in range(len(slackPercentage)):
    if len(slackPercentage[i])!=0:
        plt.plot(slackPercentage[i])
        plt.ylabel('slackPercentage')
        plt.show()


# In[ ]:

def getDiscount(slackPercent):
    discount = []
    for i in range(len(slackPercent)):
        disc = []
        for j in range(len(slackPercent[i])):
            if(slackPercent[i][j]<5):
                disc.append(0)
            elif(slackPercent[i][j]<10):
                disc.append(5)
            elif(slackPercent[i][j]<15):
                disc.append(10)
            elif(slackPercent[i][j]<20):
                disc.append(15)
            elif(slackPercent[i][j]<30):
                disc.append(20)
            else:
                disc.append(30)
            
        discount.append(disc)
    return discount
#--------------------------------------

discount=getDiscount(slackPercentage)


# In[ ]:

# for i in range(len(discount)):
#     if len(discount[i])!=0:
#         plt.plot(discount[i])
#         plt.ylabel('discount')
#         plt.show()


# In[ ]:





# In[14]:

uniProduct


# In[15]:

discount


# In[16]:

print(len(discount))


# In[54]:

for i in range(len(discount)):
    if len(discount[i])!=0 :
        # Open database connection
        db = MySQLdb.connect("localhost","root","","dbtest1",unix_socket="/opt/lampp/var/mysql/mysql.sock" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        Product=int(uniProduct[i])
        print (Product)
        prom=int(discount[i][-1])
        print (prom)
        sql = "INSERT INTO Discounts(TPNB,offer) VALUES(%s,%s)"
        #try:
           # Execute the SQL command
        cursor.execute(sql,(Product,prom))
           # Commit your changes in the database
        db.commit()
        #except:
           # Rollback in case there is any error
            #db.rollback()
        db.close()


# In[39]:

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO Discounts(TPNB,Offer) VALUES(652470870,0);"
try:
   # Execute the SQL command
    cursor.execute(sql)
   # Commit your changes in the database
    db.commit()
except:
   # Rollback in case there is any error
    db.rollback()
    db.close()


# In[ ]:



