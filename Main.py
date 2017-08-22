
# coding: utf-8

# In[1]:




# In[1]:

import copy 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:

import classify
import calender
import wastage
import slackCalculation
import slack_percentage
import discountLogic
import Analysis
import preference


# In[3]:

storeData_=pd.read_csv("SuperUltraData.csv")


# In[4]:

#clubcardData consists of purchasing history of clubcard members.
clubcardData = pd.read_csv('Clubcard.txt', delimiter='\t')


# In[5]:

#storeData consists of sales history of 27 unique TPNBs and two stores.
storeData=storeData_[['RETAIL_OUTLET_NUMBER','BASE_PRODUCT_NUMBER','CALENDAR_DATE','REDUCED_SALES_SINGLES_QTY','EXPECTED_DAILY_SALES_QTY','ACTUAL_SALES_SINGLES','ADJUSTED_SALES_SINGLES','Delivery_Date','Code_Life_Days','Revised_Order_Qty',]]



# In[6]:

#uniProduct is list 27 unique TPNBs
uniProduct = storeData['BASE_PRODUCT_NUMBER'].unique()


# In[7]:

#Function groupSales() classify "storeData" store-wise,
#then it groups sales history TPNB wise
#expSales -> is list of lists of forecasts for different TPNBs for a period .
# similarly, actSales -> is for sales history
#calrDate -> consists of corresponding date entries
#codeLife -> has corresponding code-life(i.e. number of days after which product will expire)
#orderQty -> consists of amount of stock arrived on that day.
expSales, actSales,  calrDate , codeLife, orderQty = classify.groupSales(storeData)


# In[8]:

#fetchs name of the weekday(eg. 'thursday') from dd/mm/yy date format.
mytime = calender.getWeekDay(calrDate)


# In[9]:

#function getWastage() finds the quantity that expires at the end of the day
#the algorithm used assumes that the stock arrived first would be sold first if available.
wastage,stock=wastage.getWastage(copy.deepcopy(actSales),orderQty,codeLife)


# In[10]:

#slack refers to the quantity by which sale is behind the target.
slack = slackCalculation.getSlack(expSales, actSales)
actSlack=slackCalculation.getActualSlack(slack,wastage)
cumSlack=slackCalculation.getCumSlack(copy.deepcopy(actSlack))
slackPercentage = slack_percentage.getSlackPercent(cumSlack, orderQty)


# #### Actual Slack -- taking into account of wastage due to expiry

# In[11]:

# for i in range(len(actSlack)):
#     if len(actSlack[i])!=0:
#         plt.plot(actSlack[i])
#         plt.ylabel('actSlack')
#         plt.show()


# #### Cumulative Slack -- taking into account of wastage due to expiry

# In[12]:

# for i in range(len(cumSlack)):
#     if len(cumSlack[i])!=0:
#         plt.plot(cumSlack[i])
#         plt.ylabel('cumSlack')
#         plt.show()


# In[ ]:




# In[ ]:




# #### Slack Percentage Plots

# In[13]:

# for i in range(len(slackPercentage)):
#     if len(slackPercentage[i])!=0:
#         plt.plot(slackPercentage[i])
#         plt.ylabel('slackPercentage')
#         plt.show()


# In[14]:

#Analysis.plotListOfLists(slackPercentage,'slackPercentage')


# In[15]:

# discount -> list of lists of discounts for different TPNBs.
discount=discountLogic.getDiscount(slackPercentage)


# In[ ]:

#Asks for input like TPNB,todays forecast,todays sale,stock arrived....
# and based on today's and past's data,it outputs discount that should 
# be given on that TPNB the next day.
#discountLogic.calcTomorrowDiscount(uniProduct, copy.deepcopy(stock), codeLife,cumSlack)

################################################################################


# In[16]:

# for i in range(len(discount)):
#     if len(discount[i])!=0:
#         plt.plot(discount[i])
#         plt.ylabel('discount')
#         plt.show()



# In[17]:

# def calcTodayDiscount(uniProduct,slackPerecent):
#     tpnb=input("Enter TPNB:")
#     index=getIndexOfProduct(tpnb,uniProduct)
#     nEntries=len(slackPercent[index])
#     return getDiscount(slackPercent[index][nEntries-1])



# In[18]:

# for i in range(len(calrDate)):
#     if(len(calrDate[i])!=0):
#          print(calrDate[i][0])
# uniProduct
# getIndexOfProduct(52251648,uniProduct)
# len(codeLife[2])
#uniProduct

###################################################################################


# In[23]:

# topProducts -> list of lists of top priorities for each unique clubcard no.(PAN)
# uniquePan   -> list of unique clubcard numbers
topProducts,uniquePan=preference.getTopProducts(clubcardData)







# In[11]:

len(topProducts)
import MySQLdb


# In[15]:

for i in range(len(discount)):
    if len(discount[i])!=0 :
        # Open database connection
        db = MySQLdb.connect("localhost","root","","firstDB",unix_socket="/opt/lampp/var/mysql/mysql.sock" )

        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        Product=int(uniProduct[i])
        print (Product)
        prom=int(discount[i][-1])
        print (prom)
        sql = "INSERT INTO discount_list(tpnb,offer) VALUES(%s,%s)"
        #try:
           # Execute the SQL command
        cursor.execute(sql,(Product,prom))
           # Commit your changes in the database
        db.commit()
        #except:
           # Rollback in case there is any error
            #db.rollback()
        db.close()


# In[ ]:



