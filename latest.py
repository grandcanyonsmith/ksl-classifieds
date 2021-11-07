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

# start_driver()

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
	use_chromedriver_on_path=True,  # True will use a system provided chromedriver binary that
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