from .lib import *
from .headers import *
##########
def set_backtest_filepath(path = r'D:\Python\vnsdata\Data\data_price.pkl'):
    return path

def list_cp(exchange = 1) -> pd.DataFrame:
    '''
    In ra list cổ phiếu của tất cả các sàn
    Eg:
    '''
    url = 'https://s.cafef.vn/ajax/pagenew/databusiness/congtyniemyet.ashx?centerid={}&skip=0&take=10000&major=0'.format(exchange)
    df_raw = rq.get(url,headers=cafef_header).json()['Data']
    df = pd.DataFrame(df_raw)
    df = df[df['Symbol'].apply(lambda x: len(x) == 3)]
    df['TradeCenterId'].replace({1: 'HOSE', 2: 'HNX', 9: 'UpCOM',8: 'OTC'}, inplace=True)
    df = df[['Symbol','TradeCenterId','CompanyName','CategoryName']]
    df.dropna(axis=0,inplace=True)
    df.reset_index(drop=True,inplace=True)
    return df

def bctc(cp,type = 1,year = 2023,quarter = 0) -> pd.DataFrame:
    '''
    In ra báo cáo tài chính của doanh nghiệp
    '''
    url_raw = 'https://restv2.fireant.vn/symbols/{}/full-financial-reports?type={}&year={}&quarter={}&limit=999999'.format(cp,type,year,quarter)
    df_raw = rq.get(url_raw,headers=fireant_header).json()
    indexs = [x['name'] for x in df_raw]
    year = [x['year'] for x in df_raw[0]['values']]
    quarter = [x['quarter'] for x in df_raw[0]['values']]
    if quarter != 0:
        col = [str(x) + '-' + str(y) for x, y in zip(year, quarter)]
    ###
    else:
        col = year
    ###
    df = [[z['value']for z in y] for y in [x['values'] for x in df_raw]]
    df = pd.DataFrame(df,index = indexs, columns=col)
    df.loc['Symbol'] = cp
    df = df.fillna(value=0)
    df = df.transpose()
    return df

def price(cp,start_date = '2000-01-01',end_date = '2024-09-20') -> pd.DataFrame:
    url = 'https://restv2.fireant.vn/symbols/{}/historical-quotes?startDate={}&endDate={}&offset=0&limit=999999'.format(cp,start_date,end_date)
    df_raw = rq.get(url,headers=fireant_header).json()
    date_raw = pd.to_datetime([x['date'].replace('T00:00:00','') for x in df_raw],format=('%Y-%m-%d')).strftime(date_format='%Y-%m-%d')
    date = pd.Series(date_raw,name='Date')
    df = pd.DataFrame(df_raw)
    df['date'] = date
    df = df.fillna(0).sort_values('date',ascending=True)
    df.index = df['date'].values
    df['priceOpen'] = df.priceOpen / df.adjRatio
    df['priceClose'] = df.priceClose / df.adjRatio
    df['priceHigh'] = df.priceHigh / df.adjRatio
    df['priceLow'] = df.priceLow / df.adjRatio
    df['priceAverage'] = df.priceAverage / df.adjRatio
    return df

def infor(cp) -> dict:
    url = 'https://restv2.fireant.vn/symbols/{}/fundamental'.format(cp)
    df_raw = rq.get(url,headers=fireant_header).json()
    return df_raw
