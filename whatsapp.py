import pandas as pd
# SELENIUM IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os
from csv import writer


from time import sleep
from urllib.parse import quote

os.system("")
os.environ["WDM_LOG_LEVEL"] = "0"
class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")
# options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
print('Once your driver opens up sign in to web whatsapp')
driver.get('https://web.whatsapp.com')


def open_whatsapp(first_name, email,country, phone_number,company, message):
    if phone_number == "":
        pass
    try:
        url = f'https://web.whatsapp.com/send?phone={phone_number}&text={message}'
        driver.get(url)
        try:
            click_btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='compose-btn-send']")))
        except Exception as e:
            print(style.RED + f"\nFailed to send message to: {phone_number}")
            organise_contacts(first_name, email,country, phone_number,company, 'contacts-failed.csv')
            delete_contacts(email, 'contacts.csv')
            return False
        else:
            sleep(1)
            click_btn.click()
            sent=True
            sleep(3)
            print(style.GREEN + f'Message sent to: {phone_number}' + style.RESET)
            organise_contacts(first_name, email,country, phone_number,company, 'contacts-success.csv')
            delete_contacts(email, 'contacts.csv')
            return True
    except Exception as e:
        print(style.RED + f'Failed to send message to {phone_number}' + str(e) + style.RESET)
        return False

# Delete number that message has been sent
def delete_contacts(email, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv('contacts.csv', header=0)

    # Select the rows where the 'email' column is '12345'
    rows_to_delete = df.loc[df['Email'] == email]

    # Delete the rows
    df = df.drop(rows_to_delete.index)

    # Write the modified DataFrame back to the CSV file
    df.to_csv(output_file, index=False)

# Create a new file and dump failed & sucessful contacts
def organise_contacts(first_name, email,country, phone_number,company, output_file):
    df = pd.read_csv('contacts.csv')

    new_row = [first_name,email,country,phone_number,company]


    with open(output_file, 'a', newline='') as f_object:
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
    
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(new_row)
    
        # Close the file object
        f_object.close()

# Import MESSAGE
def import_message( message_file_path, first_name, email, country, phone_number, company):
    d={'{{First Name}}': first_name, '{{Company}}': company}
    with open('message.txt', 'r+') as file:
        content = file.read()
        for k, v in d.items():
            content = content.replace(k, v)
        return quote(content)

# Read CSV File and extract data
def import_contacts( message_file_path, contact_file_path):

    df = pd.read_csv(contact_file_path,sep=',',chunksize=1,low_memory=True)    

    for chunk in df:
        first_name = list((chunk.to_dict()[chunk.columns[0]]).values())[0]
        email = list((chunk.to_dict()[chunk.columns[1]]).values())[0]
        country = list((chunk.to_dict()[chunk.columns[2]]).values())[0]
        phone_number = list((chunk.to_dict()[chunk.columns[3]]).values())[0]
        company = list((chunk.to_dict()[chunk.columns[4]]).values())[0]

        message = import_message(message_file_path, first_name, email, country, str(phone_number).replace(" ", ""), company)

        # if open_whatsapp(phone_number, message):
        #     continue
        open_whatsapp(first_name, email,country, phone_number,company, message)
            

    driver.close()

import_contacts("message.txt", "contacts.csv")