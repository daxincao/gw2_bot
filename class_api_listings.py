# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 23:39:29 2014

@author: Xin
"""
import urllib2
import json
import pandas as pd
import datetime     

def make_api_url(item_list, api_url):
    '''Take a list of items and make them acceptable by the api
    '''
    # Join list together as a comma-separated sequence of items
    url_str_list = [str(x) for x in item_list]
    
    url_str_joined = ','.join(url_str_list) 
    
    # Return full url
    return api_url + url_str_joined


'''
Class of objects for storing buy & sell information 
sell.price_'x' : sell price at rank 'x' ; e.g. sell_price_1 is the lowest selling price
total_quantity: total amount of an item being listed
total_listings: total number of distinct listings 
'''
class listing(object):

    def __init__(self, dataframe, listing_type, item_id):
        self.listing_type = listing_type
        self.item_id = item_id
        # Keep as powers of 5 for recursive lookup
        self.price = self.rank_price(dataframe, 1)
        self.price_5 = self.rank_price(dataframe, 5)
        self.price_25 = self.rank_price(dataframe, 25)
        self.price_125 = self.rank_price(dataframe, 125)
        self.price_625 = self.rank_price(dataframe, 625)
        self.total_quantity = self.sum_column(dataframe, 'quantity')
        self.total_listings = self.sum_column(dataframe, 'listings')
        self.datetime = datetime.datetime.now()
        
    
    def rank_price(self, dataframe, n):
        '''
        Returns price at rank n within listing
        '''
        # Try to return price at rank n 
        try:
            cumdf = dataframe['quantity'].cumsum()
            index_min = min(cumdf.index[cumdf >= n])
            return int(dataframe['unit_price'][index_min])
                  
        # If no price exists, look at a previous rank and take that price
        except ValueError:
            if n == 1:
                return int(0)
            else:
                return self.rank_price(dataframe, n/5) # recursive lookup
        
        # If there are no listings, then return 0 as price
        except KeyError:
            return int(0)
        else:
            return None
    
    def sum_column(self, dataframe, colname):
        try:
            return int(sum(dataframe[colname]))
        except KeyError:
            return int(0)
           
        
        

def get_listing_dataframe(item_list, api_url="https://api.guildwars2.com/v2/commerce/listings?ids="):
    '''
    Returns a dataframe with each row representing a single listing type for an item
    '''
    # Access URL
    url = make_api_url(item_list, api_url)
    r = urllib2.urlopen(url)
    
    # Convert json
    data = json.load(r)
    
    # Initialize empty list to hold dicts
    element_list = []
    
    # Apply 'listing' class
    for elem in data:
        buy_listing = listing(pd.DataFrame(elem['buys']), 'buy', elem['id'])
        sell_listing = listing(pd.DataFrame(elem['sells']), 'sell', elem['id'])
        element_list.append(buy_listing.__dict__)
        element_list.append(sell_listing.__dict__)
    
    # Return dataframe ; ordered for clarity
    column_order = ['item_id', 'listing_type', 'price', 'price_5', 
                    'price_25', 'price_125', 'price_625', 'total_listings', 
                    'total_quantity', 'datetime']
                    
    return pd.DataFrame.from_dict(element_list)[column_order]

        

if __name__ == '__main__':     
                    
    listings_api = "https://api.guildwars2.com/v2/commerce/listings?ids="
    
    item_list = [8920,19697,19698,19699,19739,19729]
    
    print get_listing_dataframe(item_list, listings_api)
    

            
            
