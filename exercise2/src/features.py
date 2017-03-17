import numpy as np
import pandas as pd


def customerReturnProbability(df):
	#select needed columns
    sub_df = df.loc[:, ['customerID', 'returnQuantity', 'quantity']]

    #group by customerID, sum up quantity and returnQuantity and convert grouping to dataframe
    customer_group = sub_df.groupby('customerID').sum()
    prob_df = customer_group.reset_index()

    #calculate probability be division of both sums and drop columns that arent needed any more
    prob_df['customerReturnProbability'] = prob_df.returnQuantity/prob_df.quantity
    prob_df.drop('returnQuantity', axis = 1, inplace = True)
    prob_df.drop('quantity', axis = 1, inplace = True)

    #merge (join) with original dataframe for final results
    return df.merge(prob_df, how = 'inner', on = 'customerID')


def minMaxSpanPrice(df):
    sub_df = df.loc[:, ['orderID', 'price', 'quantity']]

    #get price of single article
    sub_df['single_price'] = sub_df.price
    sub_df.loc[sub_df.quantity > 0, 'single_price'] = sub_df.loc[sub_df.quantity > 0, 'price'] / sub_df.loc[sub_df.quantity > 0, 'quantity']

    #group orders and get max and min single item price in dataframe
    price_group = sub_df.groupby(['orderID'])
    max_df = price_group.single_price.max().reset_index()
    min_df = price_group.single_price.min().reset_index()

    #create new dataframe containing needed information and get final result by join with original dataframe
    span_df = pd.DataFrame({'orderID': min_df.orderID, 'minMaxSpanPrice': max_df.single_price - min_df.single_price})
    return df.merge(span_df, how = 'inner', on = 'orderID')


def totalOrderPrice(df):
    sub_df = df.loc[:, ['orderID', 'price']]

    #group by orders, sum up prices, create new column with that infromation and delete columns that arent needed any more
    order_group = sub_df.groupby('orderID').sum()
    total_price_df = order_group.reset_index()
    total_price_df['totalOrderPrice'] = total_price_df.price
    total_price_df.drop('price', axis = 1, inplace = True)

    #get final result by join
    return df.merge(total_price_df, how = 'inner', on = 'orderID')


def totalSaving(df):
    df['totalSaving'] = 0

    #new column with difference between expected price (by quantity and rrp) and real price
    df.loc[df.quantity > 0, 'totalSaving'] = df.loc[df.quantity > 0, 'rrp'] * df.loc[df.quantity > 0,'quantity'] - df.loc[df.quantity > 0, 'price']
    df.loc[df.totalSaving < 0, 'totalSaving'] = 0
    return df


def monthOfYear(df):
	#it is alsways a good idea to have a look at the documentation
    df['monthOfYear'] =  pd.DatetimeIndex(df['orderDate']).month
    return df


def sameArticleInOrder(df):
    sub_df = df.loc[:, ['orderID', 'articleID', 'quantity']]

    #group by orders and articles and sum over quantity for each distict order-article-combination
    oa_group = sub_df.groupby(['orderID', 'articleID']).quantity.sum()
    oa_df = oa_group.reset_index()

    #if that sum is greater than 1 that means there is the same article more than once in one order
    oa_df['sameArticleInOrder'] = (oa_df.quantity > 1) * 1
    oa_df.drop('quantity', axis = 1, inplace = True)
    return df.merge(oa_df, how = 'inner', on = ['orderID', 'articleID'])


def hasVoucher(df):
    df['hasVoucher'] = 0
    df.loc[df['voucherID'] != '0', 'hasVoucher'] = 1
    return df


def modeQuantity(df):
	#better use dataframe.mode()
    quant, count = np.unique(df.quantity, return_counts = True)
    mode = quant[count == count.max()][0]
    df['modeQuantity'] = 0
    df.loc[df.quantity == mode, 'modeQuantity'] = 1
    return df
