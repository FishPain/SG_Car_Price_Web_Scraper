#import needed libraries
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import oss2
import os


def get_car_info(soup):
  # Get the name
  name = soup.find_all("a", class_="globaltitle")[0].getText()
  # Get the prices
  price_list = []
  prices = soup.find_all("td", class_="font_red")
  for price in prices:
    if price.getText().strip().startswith("$"):
      price_list.append(price.getText().strip())


  print(f"{name}: {price_list}")
  if len(price_list) == 0:
    price_list = ""
  return name, price_list

  # new car from 1000001


# Not all code r valid
def foo(car_code, name_list, price_list, counter):
  link = f"https://www.sgcarmart.com/used_cars/info.php?ID={car_code}"
  #fetch link
  page = requests.get(link)
  for page in page.history:
    print(page.url)

  # Link and status code
  print(link, page)

  # All the html codes
  soup = BeautifulSoup(page.text, 'html.parser')
  try:
    car_info = get_car_info(soup)
  except:
    print("No such car")
    counter += 1
  else:
    name_list.append(car_info[0])
    price_list.append(car_info[1])
    counter = 0
  return counter


# Export to csv
def export_to_csv(data, file_name):
  df = pd.DataFrame(data, columns= ['Car Name', 'Prices'])

  # Show first 20 records
  df.head(20)

  # Export to CSV File
  try:
      df.to_csv(f'{file_name}.csv', index = False, header=True)
  except:
    print("Failed to tave to CSV!")
  else:
    return os.path.abspath(f'{file_name}.csv')



def save_to_oss(path):
  # Security risks may arise if you use the AccessKey pair of an Alibaba Cloud account to log on to OSS because the account has permissions on all API operations. We recommend that you use your RAM user's credentials to call API operations or perform routine operations and maintenance. To create a RAM user, log on to the RAM console. 
  auth = oss2.Auth(os.environ.get('PRIVATE_KEY'), os.environ.get('SECRET_KEY'))

  # Set yourEndpoint to the endpoint of the region in which the bucket is located. For example, if your bucket is located in the China (Hangzhou) region, set yourEndpoint to https://oss-cn-hangzhou.aliyuncs.com. 
  endpoint = 'oss-ap-southeast-1.aliyuncs.com'

  # Specify the bucket name. 
  bucket = oss2.Bucket(auth, endpoint, 'bapdata') 
  bucket.put_object_from_file('data/', path)


def run_this():
  code = 1000001
  counter = 0
  all_name_list = []
  all_price_list = []

  while code <= 1020001 and counter <= 30:
    print(f"[{code}]")
    try:
        print("1")
        a = foo(code, all_name_list, all_price_list, counter)
    except:
        # got blocked by ddos. wait for 1 minute
        print("2")
        time.sleep(60)
    else:
        print("3")
        time.sleep(1.5)
        code += 1
        counter = a
      
    # Add to pandas and csv
    data = {
        "Car Name" : all_name_list,
        "Prices" : all_price_list
        }
    
  path = export_to_csv(data,"sgCarMart_used_car_prices")
  save_to_oss(path)

  return print("Process Completed")

run_this()


