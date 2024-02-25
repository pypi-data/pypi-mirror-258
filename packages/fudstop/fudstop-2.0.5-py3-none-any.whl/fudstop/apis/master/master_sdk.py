import sys
from pathlib import Path
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[2])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import os
from dotenv import load_dotenv
load_dotenv()
import json
import inspect
from .tools import fudstop_tools
import pandas as pd
from apis.polygonio.async_polygon_sdk import Polygon
from apis.polygonio.polygon_options import PolygonOptions
from apis.polygonio.polygon_database import PolygonDatabase
from apis.webull.webull_trading import WebullTrading
from apis.webull.webull_markets import WebullMarkets
from apis.occ.occ_sdk import occSDK
from apis.newyork_fed.newyork_fed_sdk import FedNewyork
from apis.fed_print.fedprint_sdk import FedPrint
from apis.earnings_whisper.ew_sdk import EarningsWhisper
from apis.treasury.treasury_sdk import Treasury
from webull_options.webull_options import WebullOptions
from datetime import datetime, timedelta
from openai import OpenAI
import httpx
import asyncio
from datetime import date, datetime
etf_list = pd.read_csv('etf_list.csv')
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return super().default(obj)

def custom_json_dumps(data):
    return json.dumps(data, cls=CustomJSONEncoder)

def is_etf(symbol):
    """Check if a symbol is an ETF."""
    return symbol in etf_list['Symbol'].values

class MasterSDK:
    def __init__(self):
        self.trading = WebullTrading()
        self.markets = WebullMarkets(host='localhost', database='markets', password='fud', port=5432, user='chuck')
        self.occ = occSDK(host='localhost', database='markets', password='fud', port=5432, user='chuck')
        self.fed = FedNewyork()
        self.fedprint = FedPrint()
        self.client = OpenAI(api_key=os.environ.get('OPENAI_KEY'))
        self.ew = EarningsWhisper() #sync
        self.treas = Treasury(host='localhost', database='fudstop', password='fud', port=5432, user='chuck')
        self.poly = Polygon(host='localhost', database='fudstop', password='fud', port=5432, user='chuck')
        self.poly_opts =PolygonOptions(host='localhost', database='fudstop', password='fud', port=5432, user='chuck')
        self.db= PolygonDatabase(host='localhost', database='fudstop', password='fud', port=5432, user='chuck')
        self.wb_opts = WebullOptions(database='fudstop')
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')    
        self.available_functions = {
            'all_poly_options': self.all_poly_options,
            'all_webull_options': self.all_webull_options,
            'occ_options': self.occ_options,
            'webull_analysts': self.webull_analysts,
            'webull_capital_flow': self.webull_capital_flow,
            'webull_etf_holdings': self.webull_etf_holdings,
            'webull_financials': self.webull_financials,
            'webull_highs_lows': self.webull_highs_lows,
            'webull_institutions': self.webull_institutions,
            'webull_news': self.webull_news,
            'webull_short_interest': self.webull_short_interest,
            'webull_top_active': self.webull_top_active,
            'webull_top_gainers': self.webull_top_gainers,
            'webull_top_losers': self.webull_top_losers,
            'webull_top_options': self.webull_top_options,
            'webull_vol_anal': self.webull_vol_anal
        }




    def serialize_record(self,record):
        # Check if the record is a Pandas DataFrame or Series
        if isinstance(record, pd.DataFrame):
            # Convert DataFrame to a dictionary
            return record.to_dict(orient='records')
        elif isinstance(record, pd.Series):
            # Convert Series to a list
            return record.tolist()
        else:
            # For any other type, return it as is or handle serialization differently
            return record
    async def batch_insert_dataset(self, dataset: pd.DataFrame, table_name, unique_columns) -> None:
        """Auto batch inserts the dataframe into postgres SQL database."""

        await self.db.batch_insert_dataframe(dataset, table_name=table_name, unique_columns=unique_columns)



    async def webull_short_interest(self, ticker, limit:int=20, insert:bool=False):
        """Get short interest data for a ticker."""
        data = await self.trading.get_short_interest(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='short_int', unique_columns='ticker')

        return df.head(limit).to_dict('records')
    

    async def webull_vol_anal(self, ticker, limit:int=50, insert:bool=False):
        "Get volume analysis data for a ticker"""
        data = await self.trading.volume_analysis(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='vol_anal', unique_columns='ticker')
        return df.head(limit).to_dict('records')


    async def webull_institutions(self, ticker, limit:int=50, insert:bool=False):
        """Get institutional ownership data for a ticker."""
        if is_etf(ticker):
            return "Ticker is an ETF. Try again."
        data = await self.trading.institutional_holding(ticker)
        df = data.as_dataframe
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='inst_holding', unique_columns='ticker')
        return df.head(limit).to_dict('records')
    

    async def webull_analysts(self, ticker, limit:int=50, insert:bool=False):
        """Get analyst ratings for a ticker"""
        if is_etf(ticker):
            return "Ticker is an ETF. Try again."
        data = await self.trading.get_analyst_ratings(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='analysts', unique_columns='ticker')
        return df.head(limit).to_dict('records')
    
    async def webull_financials(self, ticker, type:str='balancesheet', limit:int=4, insert:bool=False):
        """Get webull financial data for a ticker.
        
        
        Args:

        >>> ticker
        >>> type = the type of financials (balancesheet, cashflow, incomestatement)
        """
        if is_etf(ticker):
            return "Ticker is an ETF. Try again."
        data = await self.trading.financials(symbol=ticker, financials_type=type)

        df = pd.DataFrame(data)
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='financials', unique_columns='ticker')
        
        return df.head(limit).to_dict('records')
        
    async def webull_etf_holdings(self, ticker, limit:int=25, insert:bool=False):
        """Gets ETF holdings for a non-etf symbol."""
        if is_etf(ticker):
            return "Ticker is an ETF. Try again."
        
        data = await self.trading.etf_holdings(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='etf_holdings', unique_columns='ticker')
        return df.head(limit).to_dict('records')

    async def webull_news(self, ticker, limit:int=5, insert:bool=False):
        """Gets the latest news for a ticker."""
        data = await self.trading.news(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='wb_news', unique_columns='ticker')
        return df.head(limit).to_dict('records')
    async def webull_capital_flow(self, ticker, limit:int=3, insert:bool=False):
        """Gets capital flow data broken down by player size for a ticker."""
        data = await self.trading.capital_flow(ticker)
        df = data.df
        df['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(df, table_name='cap_flow', unique_columns='ticker')
        return df.head(limit).to_dict('records')
    


    async def webull_top_gainers(self, type:str='preMarket', limit:int=20, insert:bool=False):
        """Gets the top 20 gainers on the day by type.
        
        >>> TYPES: 

        preMarket
        afterMarket
        5min
        1d
        5d
        3m
        52w
        """


        data = await self.markets.get_top_gainers(rank_type=type)
        
        data['type'] = type.lower()
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'top_gainers_{type}', unique_columns='symbol, type')
        return data.head(limit).to_dict('records')
    


    async def webull_top_losers(self, type:str='preMarket', limit:int=20, insert:bool=False):
        """Gets the top 20 losers on the day by type.
        
        >>> TYPES: 

        preMarket
        afterMarket
        5min
        1d
        5d
        3m
        52w
        """


        data = await self.markets.get_top_losers(rank_type=type)
        data['type'] = type.lower()
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'top_losers_{type}', unique_columns='symbol, type')
        return data.head(limit).to_dict('records')
    

    async def webull_top_options(self, type:str='volume', limit:int=20, insert:bool=False):
        """Gets the top 20 top options on the day by type.
        
        >>> TYPES: 

        totalVolume
        totalPosition
        volume
        position
        impVol
        turnover
        posIncrease
        posDecrease
        """


        data = await self.markets.get_top_options(rank_type=type)
        data['type'] = type.lower()
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'top_options_{type}', unique_columns='symbol, type')
        return data.head(limit).to_dict('records')
    

    
    async def webull_top_active(self, type:str='rvol10', limit:int=20, insert:bool=False):
        """Gets the top 20 top options on the day by type.
        
        >>> TYPES: 

        rvol10d
        turnover
        range
        """


        data = await self.markets.get_most_active(rank_type=type, as_dataframe=True)
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'top_active', unique_columns='symbol')
        return data.head(limit).to_dict('records')
    



    # async def webull_earnings(self, date:int=None, limit:int='20'):
    #     """Get earnings for a specific date."""


    #     data = await self.markets.earnings(start_date=date)

    #     await self.batch_insert_dataset(data, table_name=f'earnings', unique_columns='releasedate')
    #     return data.head(limit).to_dict('records')



    async def webull_highs_lows(self, type:int='newHigh', limit:int=20, insert:bool=False):
        """Get tickers pushing 52w highs and lows or near them.
        >>> TYPES:

            newHigh
            newLow
            nearHigh
            nearLow

        
        """
        


        data = await self.markets.highs_and_lows(type)

        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'{type}', unique_columns='symbol')
        return data.head(limit).to_dict('records')



    async def all_webull_options(self, ticker:str, limit:int=50, insert:bool=False):
        """Get all options for a ticker."""

        

        base_data, from_, opts = await self.wb_opts.all_options(ticker)
        vol_1y = base_data.vol1y
        opts = opts.as_dataframe
        data = opts
        data['vol1y'] = vol_1y
        data['underlying_price'] = base_data.close
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'wb_opts', unique_columns='option_symbol')
        return data.head(limit).sort_values('vol').to_dict('records')



    async def all_poly_options(self, ticker:str, limit:int=50, contract_type=None, strike_price_gte=None, strike_price_lte=None, expiry_date_gte=None, expiry_date_lte=None, insert:bool=False):
        """Get all options for a ticker."""

        

        data = await self.poly_opts.get_option_chain_all(ticker)
 
        if insert == True:
            await self.batch_insert_dataset(data.df, table_name=f'poly_opts', unique_columns='option_symbol')
        return data.df.head(limit).sort_values('vol').to_dict('records')


    async def occ_options(self, ticker:str, limit:int=50, insert:bool=False):
        """Get occ options data for a ticker."""
        

        data = await self.occ.options_monitor(ticker)

        data['ticker'] = ticker
        if insert == True:
            await self.batch_insert_dataset(data, table_name=f'occ_opts', unique_columns='ticker')
        return data.head(limit).to_dict('records')
    


    async def run_conversation(self, query):
        # Step 1: send the conversation and available functions to the model
        messages = [{"role": "user", "content": f"Call the function and go over the results as the options master: {query}"}]
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            tools=fudstop_tools,
            tool_choice="auto",  # auto is default, but we'll be explicit
        )
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        # Step 2: check if the model wanted to call a function
        if tool_calls:
            available_functions = self.available_functions
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
    
            messages.append(response_message)  # extend conversation with assistant's reply

            # Step 4: send the info for each function call and function response to the model
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print(function_name)
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)

                records = await function_to_call(**function_args)

                # Process each record for serialization
                processed_records = [self.serialize_record(record) for record in records]

                # Serialize the list of processed records
                serialized_response = custom_json_dumps(processed_records)

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": serialized_response,
                })

            second_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
            )  # get a new response from the model where it can see the function response
            return second_response




    async def run_all_ticker_funcs(self, ticker):

        tasks = [ 
            self.all_poly_options(ticker=ticker),
            self.all_webull_options(ticker=ticker),
            self.occ_options(ticker=ticker),
            self.webull_analysts(ticker=ticker),
            self.webull_financials(ticker=ticker),
            #self.webull_earnings(date=self.eight_days_from_now),
            self.webull_capital_flow(ticker=ticker),
            self.webull_etf_holdings(ticker=ticker),
            self.webull_highs_lows(type='newHigh'),
            self.webull_institutions(ticker=ticker),
            self.webull_news(ticker=ticker),
            self.webull_short_interest(ticker=ticker),
            self.webull_top_active('rvol10d'),
            self.webull_top_active('volume'),
            self.webull_top_active('turnover'),
            self.webull_top_gainers('preMarket'),
            self.webull_top_gainers('afterMarket'),
            self.webull_top_gainers('1d'),
            self.webull_top_losers('preMarket'),
            self.webull_top_losers('afterMarket'),
            self.webull_top_losers('1d'),
            self.webull_top_options('volume'),
            self.webull_top_options('position'),
            self.webull_top_options('posIncrease'),
            self.webull_top_options('posDecrease'),
            self.webull_top_options('turnover'),
            self.webull_top_options('volume'),
            self.webull_top_options('totalPosition'),
            self.webull_top_options('impVol'),
            self.webull_vol_anal(ticker=ticker),
            self.webull_highs_lows('newLow'),
            self.webull_highs_lows('nearLow'),
            self.webull_highs_lows('nearHigh'),
            
        ]


        await asyncio.gather(*tasks)




