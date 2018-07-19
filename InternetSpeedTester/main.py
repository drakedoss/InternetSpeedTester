"""
Internet Speed Tester by Drake Doss

Program gives users the ability to access an automated testing environment for their internet speeds, allowing them to
hold their Internet Service Provider (ISP) responsible for any false, "guaranteed" bandwidth/latency values.

v. 0.3, d. 07/19/2018
"""
import bandwidth
from tkinter import *
from tkinter import ttk
import ctypes
"""
This file (main.py) imports the back-end functionality of bandwidth.py to be used by the front-end which is powered by 
the Tkinter library.
"""

# Correction for high DPI displays in Windows
if __name__ == "__main__":
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Set up GUI
root = Tk()
root.config(bg='#efe1d7')
root.wm_iconphoto(True, PhotoImage(file='internetspeedtester.png'))
tk_times = StringVar(root, 'AM')
tk_browsers = StringVar(root, 'Chrome')
root.title('Internet Speed Tester')
root.resizable(width=False, height=False)

# Set up Button styles
butt_style = ttk.Style(root)
butt_style.configure('TButton', background='#c2afff')
butt_style.theme_use('alt')

# Add OptionMenu for user to choose what time of day should be paired with the end time hour
time_list = ['AM', 'PM']
times = ttk.OptionMenu(root, tk_times, time_list[0], *time_list)

# Add OptionMenu for user to choose the browser to use for speedtesting
browser_list = ['Chrome', 'Firefox']
browsers = ttk.OptionMenu(root, tk_browsers, browser_list[0], *browser_list)

# Create Labels to inform user of what input is expected in each Entry
user_min_prompt = Label(root, text='Elapsed minutes per speedtest: ', bg='#efe1d7', font=('Verdana', 8))
user_end_prompt = Label(root, text='Time to end at: ', bg='#efe1d7', font=('Verdana', 8))
user_web_prompt = Label(root, text='Browser to use: ', bg='#efe1d7', font=('Verdana', 8))

# Create Entries to obtain necessary input from user
user_min_delta = ttk.Entry(root)
user_end_time = ttk.Entry(root)

# Create Buttons for exiting the program and for running the speedtesting loop using data from the Entry objects
speed_test = ttk.Button(root, text='Run speed test', underline=0, command=lambda: bandwidth.start_testing(
    user_min_delta.get(), (user_end_time.get() + tk_times.get()), tk_browsers.get()))
exit_program = ttk.Button(root, text='Exit program', command=lambda: exit(0), underline=0)

# Place all Tkinter GUI elements in a grid configuration starting at column 0, row 0
user_min_prompt.grid(row=0, column=0, sticky=E)
user_end_prompt.grid(row=1, column=0, sticky=E)
user_web_prompt.grid(row=2, column=0, sticky=E)
user_min_delta.grid(row=0, column=1, pady=2, padx=2)
user_end_time.grid(row=1, column=1, pady=2, padx=2)
speed_test.grid(row=0, column=2, padx=2, pady=5)
exit_program.grid(row=3, column=2, sticky=W, pady=4, padx=2)
browsers.grid(row=2, column=1, sticky=W, padx=2, pady=2)
times.grid(row=1, column=2, sticky=W, padx=5, pady=2)
root.mainloop()
