import os
import json
import logging
import zipfile

import requests

import file_util


CHROME_DRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com"
CHROME_DRIVER_FOLDER = r"driver"
CHROME_DRIVER_MAPPING_FILE = r"{}\mapping.json".format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_EXE = r"{}\chromedriver.exe"
CHROME_DRIVER_ZIP = r"{}\chromedriver_win32.zip".format(CHROME_DRIVER_FOLDER)


def get_chrome_driver_major_version():
    chrome_browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    chrome_ver = file_util.get_file_version(chrome_browser_path)
    chrome_major_ver = chrome_ver.split(".")[0]
    return chrome_major_ver


def get_latest_driver_version(browser_ver):
    latest_api = "{}/LATEST_RELEASE_{}".format(
        CHROME_DRIVER_BASE_URL, browser_ver)
    resp = requests.get(latest_api)
    lastest_driver_version = resp.text.strip()
    return lastest_driver_version


def download_driver(driver_ver, dest_folder):
    download_api = "{}/{}/chromedriver_win32.zip".format(
        CHROME_DRIVER_BASE_URL, driver_ver)
    dest_path = os.path.join(dest_folder, os.path.basename(download_api))
    resp = requests.get(download_api, stream=True, timeout=300)

    if resp.status_code == 200:
        try:
            with open(dest_path, "wb") as f:
                f.write(resp.content)
            logging.info("Download driver completed")
        except Exception as e:
            print(e)
            print("Auto Make Dir and Retry")
            os.mkdir("driver")
            with open(dest_path, "wb") as f:
                f.write(resp.content)
            logging.info("Download driver completed")
    else:
        raise Exception("Download chrome driver failed")


def unzip_driver_to_target_path(src_file, dest_path):
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    logging.info("Unzip [{}] -> [{}]".format(src_file, dest_path))


def read_driver_mapping_file():
    driver_mapping_dict = {}
    if os.path.exists(CHROME_DRIVER_MAPPING_FILE):
        driver_mapping_dict = file_util.read_json(CHROME_DRIVER_MAPPING_FILE)
        for key in driver_mapping_dict:
            print(driver_mapping_dict[key]['driver_version'])
    return driver_mapping_dict


def check_browser_driver_available():
    print("Install Chrome Driver Automatic")
    chrome_major_ver = get_chrome_driver_major_version()
    print("Ver: "+str(chrome_major_ver))
    mapping_dict = read_driver_mapping_file()
    driver_ver = get_latest_driver_version(chrome_major_ver)

    if chrome_major_ver not in mapping_dict:
        print("Downloading")
        download_driver(driver_ver, CHROME_DRIVER_FOLDER)
        print("Unzip")
        unzip_driver_to_target_path(CHROME_DRIVER_ZIP, CHROME_DRIVER_FOLDER+"/"+driver_ver)

        mapping_dict = {
            chrome_major_ver: {
                "driver_path": CHROME_DRIVER_EXE,
                "driver_version": driver_ver
            }
        }
        mapping_dict.update(mapping_dict)
        file_util.write_json(CHROME_DRIVER_MAPPING_FILE, mapping_dict)
        print("Complete Chrome Driver Setting")


if __name__ == "__main__":
    check_browser_driver_available()
