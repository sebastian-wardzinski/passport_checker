from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import smtplib
import sys

ADMIN_EMAIL = 'sprawdzanie.paszportu@gmail.com'
ADMIN_PASSWORD = 'insert-password-here'

def initialize_gmail_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(ADMIN_EMAIL, ADMIN_PASSWORD)
    return server


def get_data_from_csv(filename):
    file = open(filename)
    return list(csv.reader(file))


def check_status_and_send_email(work_id, recipient):
    chrome_driver.find_element(by=By.XPATH, value='//*[@id="numer-wniosku"]').send_keys(work_id)
    chrome_driver.find_element(by=By.XPATH, value='//*[@id="sprawdzWniosekSubmit"]').click()

    message = ''
    # Sometimes the result is not readable immediately
    while (message == ''):
        message = chrome_driver.find_element(by=By.XPATH, value='//*[@id="_101_INSTANCE_1001_80408"]/div/div[2]/article/div[3]/div[1]/div/div/p[2]').text

    # I'm not sure what the message will be when the passport isn't ready, or what types of messages are possible, but the below message states it is still not ready
    # As new messages are discovered it may be useful to expand to this branching block
    if (message == 'Twój wniosek został przyjęty w urzędzie. Nie możesz jeszcze odebrać paszportu.' or message == 'Twój paszport jest w realizacji. Nie możesz go jeszcze odebrać.'):
        print(f'Passport with work_id {work_id} is still not ready for pickup.')
    elif (message == 'Nie znaleziono danych dla wniosku'):
        print(f'Work_id {work_id} is not found.')
    else:
        # Only send email notifcation if passport may be ready for pickup
        gmail_server.sendmail(ADMIN_EMAIL, recipient, msg=f'Your passport with work_id {work_id} may be ready for pickup!')


def main():
    global chrome_driver, gmail_server

    chrome_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    gmail_server = initialize_gmail_server()

    # Good practice to make increase chance that all elements we will interact with will be visible
    chrome_driver.maximize_window()

    chrome_driver.get('https://obywatel.gov.pl/wyjazd-za-granice/sprawdz-czy-twoj-paszport-jest-gotowy')

    # Gets rid of pop-up, required to make rest of webpage accessible
    chrome_driver.find_element(by=By.XPATH, value='//*[@id="modal-rodo"]/div/div/div[3]/button').click()

    data = get_data_from_csv("work_ids_to_check.csv")

    for work_id, recipient in data:
        check_status_and_send_email(work_id, recipient)

    gmail_server.close()
    chrome_driver.close()


if __name__ == "__main__":
    main()
    sys.exit()