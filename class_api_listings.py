# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 23:39:29 2014

@author: Xin
"""
import urllib2
import json
import pandas
import datetime       

# Auxiliary function to format items
def make_api_url(item_list, api_url):
    '''Take a list of items and make them acceptable by the api
    '''
    # Join list together as a comma-separated sequence of items
    url_str_list = [str(x) for x in item_list]
    
    url_str_joined = ','.join(url_str_list) 
    
    # Return full url
    return api_url + url_str_joined

# Class for creating an object containing pricing information for each item
class listing(object):
    
    def __init__(self, dataframe, listing_type):
        self.type = listing_type
        # Keep as powers of 5 for recursive lookup
        self.price = self.rank_price(dataframe, 1)
        self.price_5 = self.rank_price(dataframe, 5)
        self.price_25 = self.rank_price(dataframe, 25)
        self.price_125 = self.rank_price(dataframe, 125)
        self.price_625 = self.rank_price(dataframe, 625)
        self.total_quantity = self.sum_column(dataframe, 'quantity')
        self.total_listings = self.sum_column(dataframe, 'listings')
        
    
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
                return self.rank_price(dataframe, n/5) # Recursive lookup
        
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
       
# test


if __name__ == '__main__':     

    listings_api = "https://api.guildwars2.com/v2/commerce/listings?ids="
    
    
    item_list = [8920,19697,19698,19699,19739,19729]
    
    url = make_api_url(item_list, listings_api)
    
    r = urllib2.urlopen(url)
    
    data = json.load(r)
    
    item_prices = []
    
    for elem in data:
            buy_listing = listing(pandas.DataFrame(elem['buys']), 'buy')
            sell_listing = listing(pandas.DataFrame(elem['sells']), 'sell')
            print buy_listing.__dict__
            print sell_listing.__dict__
            
