# This is a sample Python script.
import pandas as pd
import re

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Inventory = 'rexjs12p78'
    inventory = re.sub("\D", "", Inventory)
    # if inventory = None
    #     print('bino!')
    if len(inventory) == 0:
        print('空')
    else:print("非空")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
