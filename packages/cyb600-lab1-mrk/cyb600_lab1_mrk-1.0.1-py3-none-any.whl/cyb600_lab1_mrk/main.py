from datetime import datetime


def thetime():
    """
    Obtains the time using the datetime function and displays it in the terminal
    """
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    print('Current Time: ', time)