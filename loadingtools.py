"""
Maksym Bilyk -- All __modules reserved__
"""
from time import sleep
import sys


FUNNY_MESSAGES = ['Swapping time and space...', 'Tokenizing real life...',\
                     'Filtering morale...', 'Checking the gravitational constant in your location',\
                     'Counting backwards from Infinity', 'Spinning the wheel of fortune...',\
                     'Loading the enchanted bunny...', 'Computing chance of success',\
                     'Looking for exact change', 'Listening for the sound of one hand clapping...',\
                     'Keeping all the 1\'s and removing all the 0\'s...',\
                     'Cleaning off the cobwebs...', 'Connecting Neurotoxin Storage Tank...',\
                     'Granting wishes...', 'Spinning the hamster…',\
                     'Convincing AI not to turn evil..', 'Dividing by zero...',\
                     'Trying to sort in O(n)...', 'Looking for sense of humour, please hold on.',\
                     'Ordering 1s and 0s...', 'Loading funny message...', 'Downloading more RAM..',\
                     'Waiting Daenerys say all her titles...', 'Updating to Windows Vista...',\
                     'Deleting System32 folder', 'Initializing the initializer...',\
                     'Optimizing the optimizer...', 'Pushing pixels...', 'Building a wall...',\
                     'Updating Updater...', 'Downloading Downloader...', 'Debugging Debugger...',\
                     'Reading Terms and Conditions for you.', 'Running with scissors...',\
                     'Discovering new ways of making you wait...', 'Breeding the bits',\
                     'Following the white rabbit', 'Making sure all the i\'s have dots...',\
                     'Mining some bitcoins...', 'Formating disc C:\\ ...']


def loader(const, percent, message):
    """
    Parameters
    ----------
    const = number of bars
    percent = current percent of loading from 1 to 100
    message = list of messages (str)

    Returns
    -------
    None
    """

    image = u'\u2588'
    background = u'\u2593'
    sleep(0.01)
    animation = image*const + background*const
    level = percent//(100//const)
    prefix = "\r" + " " + str(percent) + "% " + " "*(percent < 10) + " "*(percent < 100)
    max_len = max([len(elm) for elm in message])
    message = [elm + " "*(max_len-len(elm)) for elm in message]
    msg_counter = percent//(100//len(message)-1)
    ordinal = msg_counter if msg_counter < len(message) else msg_counter - 1
    ending = message[ordinal] if percent < 100 else " "*max_len
    sys.stdout.write(prefix + animation[const-level: const*2 - level] + "\t" + ending)
    sys.stdout.flush()
