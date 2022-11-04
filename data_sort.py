import csv
import pandas as pd
import numpy as np


csv_name = str(input("Please enter the name of your CSV file: ") + '.csv')

csv_file_path = f"/Users/ericxie/Documents/Develop/amazon_web_scraper/CSV_files/{csv_name}"

df = pd.read_csv(csv_file_path)
pd.set_option('display.max_columns', 100)  

# Convert from string to float
df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)
df['ReviewCount'] = df['ReviewCount'].str.replace(',', '').astype(int)

print("Please choose from the following options:")
print(f"1. Price\n2. Ratings\n3. Review Count")
option = input("Which option would you like? ")

## Price
if option.lower() == 'price':
    price_check = input("Would you like to see the highest or lowest priced item? ")
    if price_check.lower() == 'highest':
        highest_price = df[df['Price']==df['Price'].max()]
        print(highest_price)
    elif price_check.lower() == 'lowest':
        lowest_price = df[df['Price']==df['Price'].min()]
        print(lowest_price)
    else:
        exit()
## Ratings
elif option.lower() == 'ratings':
    ratings_check = input("Would you like to see the highest or lowest rated item? ")
    if ratings_check.lower() == 'highest':
        highest_ratings = df.sort_values('Rating', ascending=False)
        print(highest_ratings.head(1))
    elif ratings_check.lower() == 'lowest':
        lowest_ratings = df.sort_values('Rating', ascending=True)
        print(lowest_ratings.head(1))
    else:
        exit()
## Review count
elif option.lower() == 'review count':
    review_count = input("Would you like to see the highest or lowest reviewed item? ")
    if review_count.lower() == 'highest':
        highest_review = df[df['ReviewCount']==df['ReviewCount'].max()]
        print(highest_review)
    elif review_count.lower() == 'lowest':
        lowest_review = df[df['ReviewCount']==df['ReviewCount'].min()]
        print(lowest_review)
    else:
        exit()
'''
elif option.lower() == 'price + ratings' or option.lower() == 'ratings + price':
    # highest_price = df[df['Price']==df['Price'].max()]
    lowest_price = df[df['Price']==df['Price'].min()]
    highest_rating = df.sort_values('Rating', ascending=False).head(1)
    n = df.groupby('Description').agg({'Price':'min', 'ReviewCount':'max'})[['Price','ReviewCount']].reset_index()
'''