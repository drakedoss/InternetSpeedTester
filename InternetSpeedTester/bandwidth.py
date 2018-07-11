"""
Internet Speed Tester by Drake Doss

Program gives users the ability to access an automated testing environment for their internet speeds, allowing them to
hold their Internet Service Provider (ISP) responsible for any false, "guaranteed" bandwidth/latency values.

v. 0.1, d. 07/07/2018
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions
import requests
import time
import datetime
from tkinter import *
"""
This file (bandwidth.py) provides functions to be linked to the front-end which allow the user to begin their automated
testing experience. Selenium, BeautifulSoup, requests, datetime, and Tkinter libraries are used to parse through the
website speedtest.net for data regarding the user's bandwidth and latency.
"""


# Creates an informational window for the user to receive helpful information regarding when testing is done or if the
# program ran into an error.
def alertbox(message: str, status: str):
    alert = Tk()
    alert.title(status)
    label_txt = Label(alert, text=message)
    label_txt.pack(padx=40, pady=10)
    affirm = Button(alert, text='Okay', command=lambda: alert.destroy(), underline=0)
    affirm.pack(padx=10, pady=2)
    alert.mainloop()


# Writes all internet speed data to a file "internet_record.txt" and handles potential exceptions.
def write_to_file(titles, data, results):
    i = 0
    file = open('internet_record.txt', 'a+')
    timestamp = str(datetime.datetime.now())

    if titles is None and data is None and results is None:
        file.write('Connection was lost or weak at ' + timestamp + '\n')
        file.write('-' * (30 + len(timestamp)) + '\n')
        return

    while i < 3:
        curr_data = str(titles[i] + ': ' + data[i])
        file.write(curr_data + '\n')
        i += 1

    file.write('Link to results: ' + results + '\n')
    file.write(('-' * 15) + timestamp + ('-' * 15) + '\n\n')
    file.close()


# Records the download and upload speeds of the user's provided internet service, as well as his or her latency.
def record_speed(exec_path_driver: str):

    # Set up webdriver for initializing speed test analytics
    if exec_path_driver == 'Firefox':
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()

    driver.set_page_load_timeout(5 * 60)

    # Catch potential exceptions if the webpage times out or connection is lost entirely
    try:
        driver.get('http://www.speedtest.net')
    except selenium.common.exceptions.TimeoutException:
        write_to_file(None, None, None)
        alertbox('Program timed out at ' + str(datetime.datetime.now()) + '.', 'Timeout')
        driver.quit()
        return
    try:
        start_speed_test = driver.find_element_by_class_name('start-text')
    except selenium.common.exceptions.NoSuchElementException:
        write_to_file(None, None, None)
        alertbox('Connection lost at ' + str(datetime.datetime.now()) + '.', 'Error')
        driver.quit()
        return

    time.sleep(5)

    start_speed_test.click()

    now = datetime.datetime.now()
    # Allow for webdriver to obtain webpage with results once it has been loaded in
    while driver.current_url == 'http://www.speedtest.net/':
        current = datetime.datetime.now()
        time_delta = current - now
        time_delta_sec = abs(time_delta.total_seconds())
        if time_delta_sec >= 180:
            write_to_file(None, None, None)
            driver.quit()
            return
        time.sleep(1)

    # Obtain URL with results
    url = driver.current_url

    # Find all elements defined by <h3> and <p> HTML tags
    results = requests.get(url)
    soup = BeautifulSoup(results.text, 'html.parser')
    data_titles = soup.find_all('h3')
    data_values = soup.find_all('p')

    # Iterate through all data titles to replace HTML tags with blank space
    i = 0
    for x in data_titles:
        x = str(x)
        x = x.replace('<h3>', '')
        x = x.replace('</h3>', '')
        data_titles[i] = x
        i += 1

    # Iterate through all data values to replace HTML tags with blank space
    i = 0
    for y in data_values:
        y = str(y)
        y = y.replace('<p>', '')
        y = y.replace('<span>', '')
        y = y.replace('</span>', '')
        y = y.replace('</p>', '')
        data_values[i] = y
        i += 1

    # Write data to internet record file for user, quit driver
    write_to_file(data_titles, data_values, url)
    driver.quit()


# Parses the end time defined by the user such that it can be compared with the datetime package format. Returns
# a datetime-formatted int representing the hour at which speedtesting should end.
def parse_time(end_time: str) -> int:

    end_time = end_time.lower()
    valid_input = [str(c) for c in range(0, 10)]
    valid_input.append('a')
    valid_input.append('m')
    valid_input.append('p')

    for x in end_time:
        if x not in valid_input:
            return -1

    if len(end_time) < 3 or len(end_time) > 6:
        return -1

    if len(end_time) == 3:
        end_time = end_time[0:1] + ' ' + end_time[1:3]

    desired_end_time = int(end_time[0: 2])

    if desired_end_time not in range(1, 13):
        return -1

    if desired_end_time == 12:
        if end_time.__contains__('pm'):
            return 12
        if end_time.__contains__('am'):
            return 0
    if end_time.__contains__('pm'):
        return 12 + desired_end_time
    else:
        return desired_end_time


# Detects if the user has entered a str rather than an int for the minute intervals, or if he/she has defined a number
# which exceeds the number of minutes between the present time and the ending time.
def invalid_delta(minute_delta, stop_hr) -> bool:
    if not minute_delta.isdigit():
        alertbox('Please enter an integer value.', 'Error')
        return True
    else:
        minute_delta = int(minute_delta)

    current_hour = datetime.datetime.now().hour
    hr_delta = abs(stop_hr - current_hour)
    max_min_delta = 60 * hr_delta

    if minute_delta < 1 or (minute_delta > max_min_delta):
        alertbox('Please use a value below the number of minutes between now and the defined end time.', 'Error')
        return True
    else:
        return False


# Begins the speedtest using the user-defined minute intervals, stop time, and browser.
def start_testing(minute_delta, stop_time: str, web_driver: str):
    stopping_hour = parse_time(stop_time)

    if stopping_hour == -1:
        alertbox('Please enter a number between 1 and 12 for the ending time.', 'Input error')
        return

    if invalid_delta(minute_delta, stopping_hour):
        return

    minute_delta = int(minute_delta)

    while True:
        record_speed(web_driver)
        time.sleep(minute_delta * 60)
        later = datetime.datetime.now()
        if later.hour == stopping_hour:
            alertbox('Speedtesting complete.', 'Success')
            break
