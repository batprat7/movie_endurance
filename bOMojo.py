from bs4 import BeautifulSoup
import requests as rq
import re
import pandas as pd
import numpy as np

def convdollar(x):
    """
    Just a parsing function converting 2.5k to 2500, 1mil to 1000000
    """
    x = x.replace('$', '')
    x = x.replace(',', '')
    return x

def scrape():
    """
    Gets all box office data from 1989 to 2018 from boxofficemojo.com
    """
    years=[str(a) for a in range(1977,2019)]
    df_list=[]
    for year in years:
        r=rq.get('https://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr=%s&p=.htm' % year)
        print('Box Office data for %s scraped' % year)
        p=BeautifulSoup(r.text,'html.parser')
        
        ### Look for the table ### 
        b=p.find_all('table')
        
        ### Usually the fourth table object on page ### 
        tb=b[0].find_all('td')
        
        ## Each data field is found in a <td> element in the fourth table. Store all data in a list ## 
        data=[]
        for i in tb:
            if i['class'] and 'mojo-field-type-release' in i['class'] and '-' not in i['class']:
                curr = i.find('a').contents[0]
                if curr != '-':
                    data.append(curr)
            elif i['class'] and 'mojo-field-type-money' in i['class'] and '-' not in i['class']:
                curr = i.contents[0]
                if curr != '-':
                    data.append(curr)


                
        ### Still a <b> tag left for <font> tags ## 
        #data=[a.contents[0] if type(a)!=bs4.element.NavigableString else a for a in data]
        
        ### Strip special characters ### 

        data=[re.sub('[^A-Za-z0-9-. ]+', '', a) for a in data]


        
        ### Fill NaNs ### 
        data=[np.nan if a =='na' else a for a in data]
        
        ### Define the feature names ###
        columns=['title', 'gross', 'worldwide-gross']
        
        ### First 6 elements are column headers # 
        to_df=data
        print('Movies found: ', len(to_df)/3)
        
        ### Escape clause in case the layout changes from year to year ### 
        if len(to_df)%len(columns) != 0:
            print('Possible table misalignment in table for year %s' % year)
            break 
        
        ### Convert to pandas dataframe ### 
        
        nrow=int(len(to_df)/len(columns))
        df=pd.DataFrame(np.array(to_df).reshape(nrow,3),columns=columns)
        df[['gross', 'worldwide-gross']]=df[['gross', 'worldwide-gross']].applymap(lambda x:convdollar(x))
        df_list.append(df)

    main=pd.concat(df_list)
    
    # Store data into csv # 
    main.to_csv('./annual_mojo.csv')

    
if __name__ == "__main__": 

    scrape()
