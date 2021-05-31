print("Welcome Using CCIT Temperature Automatic Report System")
print("Made By CNTFK")
print("Licence: GNU LGPLv3")
print("Version:v1.0")

import os
import time
import random
from selenium import webdriver
from PIL import ImageGrab
import file_util
import chrome_helper as install
print("Load Modular Succeceful!")

verision = "0"
print("Detecting Chrome Driver...")
CHROME_DRIVER_FOLDER = r"driver"
CHROME_DRIVER_MAPPING_FILE = r"{}\mapping.json".format(CHROME_DRIVER_FOLDER)
driver_mapping_dict = {}
if os.path.exists(CHROME_DRIVER_MAPPING_FILE):
    driver_mapping_dict = file_util.read_json(CHROME_DRIVER_MAPPING_FILE)
    for key in driver_mapping_dict:
        print("Driver Verison: "+driver_mapping_dict[key]['driver_version'])
        version = driver_mapping_dict[key]['driver_version']
else:
    install.check_browser_driver_available()
    driver_mapping_dict = file_util.read_json(CHROME_DRIVER_MAPPING_FILE)
    for key in driver_mapping_dict:
        print("Driver Verison: "+driver_mapping_dict[key]['driver_version'])
        version = driver_mapping_dict[key]['driver_version']

print("Load Driver Succeceful!")

driver = webdriver.Chrome("./driver/"+ version +"/chromedriver.exe")
print("Load Chrome")

print("Open Google Form")
driver.get("https://docs.google.com/forms/d/e/1FAIpQLSc3BI67oRNeRDgcyRd_gWBDn8H8jf9EtqcdWpKAVx_uPI-tkw/viewform")

print("Click Next")
next=driver.find_element_by_class_name("appsMaterialWizButtonPaperbuttonContent.exportButtonContent")
next.click()
print("Click Complete")
time.sleep(1)

print("Find Element")
unit=driver.find_elements_by_xpath("//div[contains(@jsname,'LgbsSe')]//div[contains(@jsname,'d9BH4c')]//div[contains(@role,'option')]")
#print(unit)
print("Click List")
unit[0].click()
print("Click Complete")
time.sleep(1)
unit=driver.find_elements_by_xpath("//div[contains(@data-value,'學生2中隊')]")
#print(unit)
print("Choose Element")
unit[1].click()
print("Choose Complete")
time.sleep(1)

id_name=driver.find_elements_by_xpath("//input[contains(@type,'text')]")
#print(id_name)
id_name[0].send_keys("1100533023")
id_name[1].send_keys("沈0甫")

temp = random.randint(0,10)
print("填入溫度:"+str(temp*0.1+35.5))
radio=driver.find_elements_by_xpath("//div//div[contains(@aria-setsize,'9')]")
if(temp>5):
    radio[temp-6].click()
else:
    radio[0].click()
    id_name[2].send_keys(str(temp*0.1+35.5))

print("Check Healthy")
check=driver.find_element_by_xpath("//div//div[contains(@aria-label,'正常')]")
#print(check)
check.click()
check=driver.find_element_by_xpath("//div//div[contains(@aria-label,'否')]")
#print(check)
check.click()

print("Find Element")
unit=driver.find_elements_by_xpath("//div[contains(@jsname,'LgbsSe')]//div[contains(@jsname,'d9BH4c')]//div[contains(@role,'option')]")
print(unit)
print("Click List")
unit[19].click()
print("Click Complete")
time.sleep(1)
unit=driver.find_elements_by_xpath("//div[contains(@data-value,'是，進口疫苗')]")
#print(unit)
print("Choose Element")
unit[1].click()
print("Choose Complete")
time.sleep(1)

confirm=driver.find_elements_by_class_name("appsMaterialWizButtonPaperbuttonContent.exportButtonContent")
confirm[1].click()
time.sleep(2)

im = ImageGrab.grab()
im.save('./data/'+time.strftime("%Y-%m-%d", time.localtime())+".png")

driver.close()
