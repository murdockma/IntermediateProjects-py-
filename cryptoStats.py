import time
import requests
import pandas as pd
import datetime

class Crypto():
    
    def __init__(self, crypto, historic_date=None, lst_of_cryps=None):
        self.crypto = crypto
        self.historic_date = historic_date
        self.lst_of_cryps = lst_of_cryps
    
    def findCryptoStats(self): 
        # parameters -> pass whatever established crypto you want info on as argument 1, and pass a historic date to see it's historic price as argument 2

        cryp_req = requests.get("https://api.coingecko.com/api/v3/coins/"+str(self.crypto)).json() # request to get info on crypto specified in argument 1

        if('error' in cryp_req):
            print("Crypto not found in coingeck.api")
        else:

            for stat in [cryp_req]: 
                # for each statistic (iteration) in our crypto request
                print(f"Loading {stat['name']} stats......\n")
                # print name of crypto and loading stats
                time.sleep(2)
                try:
                    print(f'''\033[1m{stat['name']}: ${stat["market_data"]["current_price"]["usd"]}\033[0m''') # print cryptos current price
                    print(f'''{self.crypto}'s symbol is -- {stat['symbol']}''') # prints cryptos symbol
                    print(f'''{stat['symbol']} uses a {stat['hashing_algorithm']} hashing algorithm.''') # print cryptos hashing algorithm
                    print(f'''Market cap -- {stat['market_data']['market_cap']['usd']}      Volume -- {stat['market_data']['total_volume']['usd']}''') # prints market cap and total vol
                    print(f'''Market cap rank -- {stat['market_cap_rank']}       Developer score -- {stat['developer_score']}''') # market cap rank and dev score
                    print(stat['name']+"s official subreddit -- "+stat['links']['subreddit_url']) # subreddit url

                except TypeError: # some data on certain cryptos have NoneTypes, cant concatenate a nonetype to str
                    pass

                print(f'''\033[1m\n\nPast Subreddit Details: ({self.historic_date}\033[0m''')

                coin_hist_req = requests.get("https://api.coingecko.com/api/v3/coins/"+ str(stat['id'])+"/history?date="+str(self.historic_date)).json() 
                # request for the historic price on specified day using cryptos id

                for past_detail in [coin_hist_req]: # historic data also has historic subreddit details

                    print(f'''Average posts per 48h -- {past_detail['community_data']['reddit_average_posts_48h']}''') # print average subreddit users
                    print(f'''Average comments per 48h -- {past_detail['community_data']['reddit_average_comments_48h']}''') # average comments per 48h
                    print(f'''Total subs -- {past_detail['community_data']['reddit_subscribers']}''') # total subreddit subscribers

                    print(f'''\n\n\033[1mRepos data:\033[0m\n'+'Total issues -- {past_detail['developer_data']['total_issues']}      Closed Issues -- {past_detail['developer_data']['closed_issues']}''') # repository data

                    print("\n\n\033[1mHistoric:\033[0m")
                    print(f'''{stat['name']}s price on {self.historic_date} -- ${past_detail['market_data']['current_price']['usd']}''') # historic price


                ticker_request = requests.get("https://api.coingecko.com/api/v3/coins/"+stat['id']+"/tickers").json() # requests to get more info on ticker using id
                for ticker in [ticker_request['tickers']]: # iterate through our ticker's details
                    print(f'''\n\033[1mTicker Details:\033[0m \n{stat['name']} trust score: {ticker[0]['trust_score']}''') # print the tickers trust score
                    print(f'''Bid-ask spread: {ticker[0]['bid_ask_spread_percentage']}%''') # print the bid-ask spread
                    print(f'''Last traded at -- {ticker[0]['last_traded_at']}''')
                    print(f'''Trade URL -- {ticker[0]['trade_url']}\n\n''')

                market_chart_req = requests.get("https://api.coingecko.com/api/v3/coins/"+stat['id']+"/market_chart?vs_currency=usd&days=14").json()
                rev_prices = []
                for price in reversed(market_chart_req['prices']): # need to reverse prices in list to show most recent first
                    rev_prices.append(price[1])
                df = pd.DataFrame({'Price (USD)':rev_prices})
                print(f'''\033[1m{stat['name']} market chart: \033[0m\n''')
                display(df.head(24)) # dispalying first 24 rows of dataframe (1Day or so)

                print(f'''\n\n\033[1mDescription\033[0m: \n{stat['description']['en']}''') # description on the crypto

#     findCryptoStats("ethereum", "12-9-2021")



    def evaluate_crypto(self, mon_year, alpha):
        thirty_day = []
        sum_,ovr,int_cnt = 0,0,0
        
        for day in range(1,30):
            try:
                daily_hist_req = requests.get("https://api.coingecko.com/api/v3/coins/"+self.crypto+"/history?date="+str(day)+"-"+str(mon_year)).json() 
            except JSONDecodeError:
                pass
            for k in [daily_hist_req]:
                for hist_price in [daily_hist_req]:
                    try:
                        thirty_day.append((str(round(hist_price['market_data']['current_price']['usd'],2))))
                    except KeyError:
                        thirty_day.append("Market data unavailble for specified day")
                        
        
        cur = 0.00 # set cur val equal to float (since we are adding floats)
        dif_list = []
        tot_sum = sum(int(float(k)) for k in thirty_day) # sum of all values in thirty_day list
        for i in thirty_day:
            dif_list.append(int(float(i)) - cur) # append the difference of our iterations (i.e, [2]-[1], [3]-[2], ....)
            cur = int(float(i)) # update the current with the previous iteration
            ovr+=1 # increase overall counter for every iteration
            if (type(i) == str):
                int_cnt+=1
                sum_+= float(i)
            # if type of i is str (for some reason the floats are stored as strs in this api), add the iteration to our cnt and len(of our iterations) by 1
                
        inc = sum(num for num in dif_list) # sum the vals for our total increase / decrease from the difference list
        perc_inc = round((inc/tot_sum)*100,2)
        self.perc_inc = perc_inc
        print(f'''\033[1mAverage Market Price over previous {int_cnt} days:\033[0m\n ${round(sum_/ovr, 2)}''')
        print(f'''\033[1mAverage price increase over past {int_cnt} days:\033[0m\n {perc_inc}%''') # print percentage increase
        # To find percentage increase we do ((x2-x1)/x1)*100. I summed the differences in each 
        # iteration(x2-x1) and summed all iterations(x1), then divided the summed differences by the total and 
        # multiplied by 100
        
        
        # checks if investment is reasonable based on alpha argument passed thorugh
        if perc_inc > alpha:
            if perc_inc > 0:
                print(f'''\033[1mReasonable investment, average percentage increase({perc_inc}%) is greater than desired alpha({alpha}%)\033[0m''')
        else:
            print(f'''\n\033[1mInvestment % increase is < your desired alpha({alpha}%). Therefore, the investment is not reasonable\033[0m''')
        
        
    def several_crypto_stats(self):
        if self.lst_of_cryps == None:
            pass
        else:
            for coin in self.lst_of_cryps:
                inst = Crypto(coin, self.historic_date)
                inst.findCryptoStats()
                print("\n\n\n\n")
                
                
    def see_price_in_currency(self):
        cur_and_price = []
        currencies = []  
        
        price_req = requests.get("https://api.coingecko.com/api/v3/coins/"+str(self.crypto)).json()
        
        for num in [price_req]:
            cur_and_price.append((num['market_data']['current_price'])) # gets list of all currencies and prices
            
        for i in cur_and_price: 
            for key, val in i.items():
                currencies.append(key) # gets list of just currencies
                
        print(f"list of currencies: {currencies}")
        for num in [price_req]:
            curr = input(f"What currency would you like to see {self.crypto} in?\n")
            print(f'''\nPrice in {curr}: \033[1m{num["market_data"]["current_price"][curr]}\033[0m''')
        # prints price is specified currency
