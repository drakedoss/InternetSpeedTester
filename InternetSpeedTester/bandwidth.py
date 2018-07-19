"""
Internet Speed Tester by Drake Doss

Program gives users the ability to access an automated testing environment for their internet speeds, allowing them to
hold their Internet Service Provider (ISP) responsible for any false, "guaranteed" bandwidth/latency values.

v. 0.3, d. 07/19/2018
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium.common.exceptions
import requests
import time
import datetime
import matplotlib.pyplot as plt
from tkinter import *
"""
This file (bandwidth.py) provides functions to be linked to the front-end which allow the user to begin their automated
testing experience. Selenium, BeautifulSoup, requests, datetime, and Tkinter libraries are used to parse through the
website speedtest.net for data regarding the user's bandwidth and latency. Matplotlib is used to provide the end user
with a graphical representation of speed and latency values.
"""
# Turn on interactive plotting for graph
plt.ion()


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
def write_to_file(titles, data, results, greatest_val):
    i = 0
    file = open('internet_record.txt', 'a+')
    timestamp = str(datetime.datetime.now())

    if titles is None and data is None and results is None:
        file.write('Connection was lost or weak at ' + timestamp + '\n')
        file.write('-' * (30 + len(timestamp)) + '\n')
        return greatest_val, []

    all_float_data = []
    while i < 3:
        data_title = titles[i]
        data_value = data[i]
        curr_data = str(data_title + ': ' + data_value)
        float_value = float(data_value[0:3])
        all_float_data.append(float_value)

        if float_value > greatest_val:
            greatest_val = float_value

        file.write(curr_data + '\n')
        i += 1

    file.write('Link to results: ' + results + '\n')
    file.write(('-' * 15) + timestamp + ('-' * 15) + '\n\n')
    file.close()
    return greatest_val, all_float_data


# Records the download and upload speeds of the user's provided internet service, as well as his or her latency.
def record_speed(exec_path_driver: str, max_value):

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
        write_to_file(None, None, None, max_value)
        alertbox('Program timed out at ' + str(datetime.datetime.now()) + '.', 'Timeout')
        driver.quit()
        return max_value, []
    try:
        start_speed_test = driver.find_element_by_class_name('start-text')
    except selenium.common.exceptions.NoSuchElementException:
        write_to_file(None, None, None, max_value)
        alertbox('Connection lost at ' + str(datetime.datetime.now()) + '.', 'Error')
        driver.quit()
        return max_value, []

    time.sleep(5)

    start_speed_test.click()

    now = datetime.datetime.now()
    # Allow for webdriver to obtain webpage with results once it has been loaded in
    while driver.current_url == 'http://www.speedtest.net/':

        current = datetime.datetime.now()
        time_delta = current - now
        time_delta_sec = abs(time_delta.total_seconds())

        if time_delta_sec >= 180:
            write_to_file(None, None, None, max_value)
            driver.quit()
            return max_value, []

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
    data_tuple = write_to_file(data_titles, data_values, url, max_value)
    max_value = data_tuple[0]
    appendable_data = data_tuple[1]
    driver.quit()

    return max_value, appendable_data


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


# Labels each data point on graph with its value for ease of visual analysis.
def label_plot(download, upload, ping, num_runs):
    i = 0
    for x in download:
        plt.annotate(str(x), (num_runs[i], download[i]))
        i += 1
    i = 0
    for n in upload:
        plt.annotate(str(n), (num_runs[i], upload[i]))
        i += 1
    i = 0
    for k in ping:
        plt.annotate(str(k), (num_runs[i], ping[i]))
        i += 1


# Begins the speedtest using the user-defined minute intervals, stop time, and browser.
def start_testing(minute_delta, stop_time: str, web_driver: str):
    stopping_hour = parse_time(stop_time)

    if stopping_hour == -1:
        alertbox('Please enter a number between 1 and 12 for the ending time.', 'Input error')
        return

    if invalid_delta(minute_delta, stopping_hour):
        return

    minute_delta = int(minute_delta)
    greatest_value = 0
    y_coords = []

    while True:

        speed_tuple = record_speed(web_driver, greatest_value)
        greatest_value = speed_tuple[0]
        data_to_plot = speed_tuple[1]

        y_coords.extend(data_to_plot)
        time.sleep(minute_delta * 60)
        later = datetime.datetime.now()

        if later.hour == stopping_hour:
            dataset_length = int(len(y_coords) / 3)
            total_length = len(y_coords)
            x_axis = [i for i in range(1, dataset_length + 1)]

            download = y_coords[0:total_length:3]
            upload = y_coords[1:total_length:3]
            ping = y_coords[2:total_length:3]

            plt.plot(x_axis, download, 'vr')
            plt.plot(x_axis, upload, '^c')
            plt.plot(x_axis, ping, '.k')

            plt.legend(['Download', 'Upload', 'Ping'])
            plt.ylabel('Down/Upload, Ping (Mbps, ms)')
            plt.xlabel('Test #')

            label_plot(download, upload, ping, x_axis)
            plt.axis([1, dataset_length, 0, (greatest_value + 10)])
            plt.show()
            break

