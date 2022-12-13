from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import time
import glob
import os

# commands to get the current directory (which is usually the directory to the Git Repository)
parent_directory = os.path.dirname(os.path.realpath(__file__))
print(parent_directory)

# function from Stackoverflow Article User Austin Mackillop @ https://stackoverflow.com/a/51949811
def download_wait(directory, timeout, nfiles=None):
    """
    Wait for downloads to finish with a specified timeout.

    Args
    ----
    directory : str
        The path to the folder where the files will be downloaded.
    timeout : int
        How many seconds to wait until timing out.
    nfiles : int, defaults to None
        If provided, also wait for the expected number of files.

    """
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout:
        time.sleep(1)
        dl_wait = False
        files = os.listdir(directory)
        if nfiles and len(files) != nfiles:
            dl_wait = True

        for fname in files:
            if fname.endswith('.crdownload'):
                dl_wait = True

        seconds += 1
    return seconds

def remove_csvs(parent_directory):
    remove_csvs = glob.glob(f'{parent_directory}/*.csv')
    for filePath in remove_csvs:
        try:
            os.remove(filePath)
            print(f'File at {filePath} removed successfully.')
        except:
            print('Error while deleting file: ', filePath)
remove_csvs(parent_directory)

opts = Options()
opts.add_argument("--headless")
opts.set_preference("browser.download.folderList", 2)
opts.set_preference("browser.download.manager.showWhenStarting", False)
opts.set_preference("browser.download.dir", parent_directory)
opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")

browser = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options = opts)

url = 'https://gis.cdc.gov/grasp/fluview/main.html'
browser.get(url)
time.sleep(10)

download_btn_xpath = '//button[@ng-click="mainCtrl.showDownloadPopup()"]'
browser.find_element('xpath', download_btn_xpath).click()
time.sleep(3)

custom_radio_btn_xpath = '//*[@id="downloadDataBody"]/ul[1]/li[2]/div/ul/li/a'
browser.find_element('xpath', custom_radio_btn_xpath).click()
time.sleep(3)

all_seasons_xpath = '//*[@id="customDownloadPanel"]/li[1]/div/div[3]/li/a'
browser.find_element('xpath', all_seasons_xpath).click()
time.sleep(3)

download_csv_btn_xpath = '//button[@ng-click="mainCtrl.getCsvFile()"]'
browser.find_element('xpath', download_csv_btn_xpath).click()
download_wait(parent_directory, 300)



try:
    filename = glob.glob('./*.csv')[0]
except:
    print('Unable to find CSV file. Waiting 30 seconds.')
    time.sleep(30)
    filename = glob.glob('./*.csv')[0]
print(filename)
os.rename(filename, 'ilinet_state_activity_indicator_map_data.csv')
filename2 = glob.glob('./*.csv')[0]
print(filename2)

browser.close()
print('Exiting program.')
