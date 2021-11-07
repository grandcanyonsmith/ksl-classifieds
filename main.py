# from flask import Flask, render_template, request, redirect, url_for, flash
# # from flask_script import Manager, Command, Shell
# from forms import ItemInsertForm
# from forms import ItemRemoveForm
# import requests
# import pandas as pd
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'a really really really really long secret key'


# @app.route('/insert/', methods=['get', 'post'])
# def insert():
#     form = ItemInsertForm()
#     # resp = requests.get("https://ksl-classifieds.herokuapp.com/api/keywords")
#     # keywords = resp.json().get("keywords")
#     if form.validate_on_submit():

#         # df = pd.read_csv('keywords.csv')

#         item_name = form.item_name.data
#         minimum = form.minimum.data
#         maximum = form.maximum.data
#         print(item_name)
#         print(minimum)
#         print(maximum)
#         print("\nData received. Now redirecting ...")
#         endpoint = "https://ksl-classifieds.herokuapp.com/api/add-keyword"
#         data = {"item_name": item_name,
#                 "minimum_price": minimum, "maximum_price": maximum}
#         resp = requests.post(endpoint, json=data)

#         if resp.status_code == 200:
#             flash(f"{item_name} successfully added to the database")
#             print("Data added successfully")
#             return redirect(url_for('insert'))

#         # found = df[df['Item'].str.contains(item_name)]
#         # isFound = found['Item'].count()
#         # print(isFound)

#         # if(isFound==0):
#         #     print ("Unique Item Name")
#         #     new_item = {'Item':item_name, 'Minimum': minimum, 'Maximum': maximum}
#         #     print (new_item)
#         #     new_df = df
#         #     new_df = new_df.append(new_item, ignore_index=True)
#         #     new_df.reset_index(drop=True, inplace=True)
#         #     new_df.to_csv('keywords.csv', index=False)
#         #     print ("Successfully inserted Item - ", item_name)
#         else:
#             print("Something went wrong")
#             return render_template('add-item.html', form=form)

#     return render_template('add-item.html', form=form)


# @app.route('/delete/', methods=['get', 'post'])
# def delete():
#     # form = ItemRemoveForm()
#     resp = requests.get("https://ksl-classifieds.herokuapp.com/api/keywords")
#     keywords = resp.json().get("keywords")

#     return render_template('remove-keyword.html', keywords=keywords)

#     # if form.validate_on_submit():

#     #     df = pd.read_csv('keywords.csv')

#     #     item_name = form.remove_item_name.data

#     #     print(item_name)

#     # print("\nData received. Now Searching for removal ...")

#     # endpoint = f"https://ksl-classifieds.herokuapp.com/api/keywords/delete/{item_name}"
#     # resp = requests.post(endpoint)
#     # if resp.status_code == 200:
#     #     flash(f"{item_name} successfully deleted from the database")
#     #     return redirect(url_for('delete'))
#     # found = df[df['Item'].str.contains(item_name)]
#     # isFound = found['Item'].count()
#     # print(isFound)

#     # if(isFound != 0):
#     #     print("Item found")
#     #     new_df = df
#     #     new_df = new_df[new_df.Item != item_name]
#     #     new_df.reset_index(drop=True, inplace=True)
#     #     new_df.to_csv('keywords.csv', index=False)
#     #     print("Successfully Deleted Item - ", item_name)
#     # else:
#     #     print("Not found")

#     # return render_template('delete.html', form=form)


# @app.route("/remove/")
# def remove_keyword():
#     # endpoint = f"https://ksl-classifieds.herokuapp.com/api/keywords/delete/{item_name}"
#     # resp = requests.post(endpoint)
#     # if resp.status_code == 200:
#     #     flash(f"{item_name} successfully deleted from the database")
#     #     return redirect(url_for('delete'))
#     return render_template("remove-keyword.html")


# @app.route('/', methods=["POST", "GET"])
# def index():
#     resp = requests.get("https://ksl-classifieds.herokuapp.com/api/keywords")
#     keywords = resp.json().get("keywords")
#     return render_template('index.html', keywords=keywords)


# @app.route('/<product_name>')
# def product_page(product_name):

#     resp = requests.get(
#         f"https://ksl-classifieds.herokuapp.com/api/filter/{product_name}")
#     products = resp.json().get("products")
#     return render_template('product_page.html', products=products, product_name=product_name)

#     # return render_template('index.html')


# if __name__ == "__main__":
#     app.run(debug=True)

import json
from account_types import *
import mintapi
import csv
import time
from urllib.parse import quote

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from twilio.rest import Client

import os
import shutil
import requests

def start_driver():
    option = Options()
    # You can comment and uncomment the below 2 lines to get window or windowless mode of the google chrome.
    # option.add_argument('--headless')
    # option.add_argument('--disable-gpu')
    # Chrome driver manager automatically downloads the latest driver required to run google chrome using selenium.
    return webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=option)

start_driver()

mint = mintapi.Mint(
    'canyonfsmith@gmail.com',  # Email used to log in to Mint
    'Sterling7147!',  # Your password used to log in to mint
    # Optional parameters
    mfa_method='email',  # See MFA Methods section
                       # Can be 'sms' (default), 'email', or 'soft-token'.
                       # if mintapi detects an MFA request, it will trigger the requested method
                       # and prompt on the command line.
    mfa_input_callback=None,  # see MFA Methods section
                              # used with mfa_method = 'sms' or 'email'
                              # A callback accepting a single argument (the prompt)
                              # which returns the user-inputted 2FA code. By default
                              # the default Python `input` function is used.
    mfa_token=None,   # see MFA Methods section
                      # used with mfa_method='soft-token'
                      # the token that is used to generate the totp
    intuit_account=None, # account name when multiple accounts are registered with this email.
    headless=False,  # Whether the chromedriver should work without opening a
                     # visible window (useful for server-side deployments)
                         # None will use the default account.
    session_path=None, # Directory that the Chrome persistent session will be written/read from.
                       # To avoid the 2FA code being asked for multiple times, you can either set
                       # this parameter or log in by hand in Chrome under the same user this runs
                       # as.
    imap_account='canyonfsmith@gmail.com', # account name used to log in to your IMAP server
    imap_password='Sterling7147!', # account password used to log in to your IMAP server
    imap_server=None,  # IMAP server host name
    imap_folder='INBOX',  # IMAP folder that receives MFA email
    wait_for_sync=False,  # do not wait for accounts to sync
    wait_for_sync_timeout=300,  # number of seconds to wait for sync
	use_chromedriver_on_path=False,  # True will use a system provided chromedriver binary that
	                                 # is on the PATH (instead of downloading the latest version)
  )



all_accounts = mint.get_accounts()
total_cash = []
total_investment = []
total = []

# def app():
#     print("Running application...")
#     for account in all_accounts:
#         if account['name'] in investment_accounts:
#             total_investment.append(float(account['currentBalance']))
#     total_investment_sum = {"investment": "{:,}".format(sum(total_investment).__round__(2))}
#     total.append(total_investment_sum)
#     print(total_investment_sum)
#     return total_investment_sum

class Finance:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def get_cash():
        start_driver()
        for account in all_accounts:
            if account['name'] in cash_accounts:
                total_cash.append(float(account['value']))
        total_cash_sum = {"cash": "{:,}".format(sum(total_cash).__round__(2))}
        total.append(total_cash_sum)
        return total_cash_sum

    def get_investments():
        for account in all_accounts:
            if account['name'] in investment_accounts:
                total_investment.append(float(account['currentBalance']))
        total_investment_sum = {"investment": "{:,}".format(sum(total_investment).__round__(2))}
        total.append(total_investment_sum)
        return total_investment_sum

if __name__ == '__main__':
    print("Running application...")
    Finance.get_cash()
    Finance.get_investments()
    print(json.dumps(total, indent=4, sort_keys=True))
    mint.close()    