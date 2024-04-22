import requests
import csv
import json
import os
from datetime import datetime
import time
import logging

url = "http://api.open-notify.org/astros.json"

def call_astros_api(url):
    try:
        resp = requests.get(url)
        return [resp.status_code, resp.content]
    except Exception as err:
        logging.info(datetime.now().strftime("%Y-%m-%d::%H-%M-%S")+ ": OOps: Something Else", err)
        return [False , str(err)]
    logging.info(datetime.now().strftime("%Y-%m-%d::%H-%M-%S") + ": API Response Status Code {0}".format(resp.status_code))


def data_insert(header,data,path):
    try:
        with open(path+'\\space_craftfile.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter='|')
            csvwriter.writerow(header)
            csvwriter.writerows(data)
        csvfile.close()
        return 'Success'
    except Exception as e:
        return 'Failure'

def process_data(dict1):
    try:
        lst1 = []
        header = ''
        if dict1['message'] == 'success':
            if 'people' in dict1 and len(dict1['people']) > 0:
                header = list(dict1['people'][0].keys())
                for item in dict1['people']:
                    if 'name' in list(item.keys()) and 'craft' in list(item.keys()):
                        lst1.append(list(item.values()))
            else:
                logging.info(f'{datetime.now().strftime("%Y-%m-%d::%H-%M-%S")}: Poeple data is absent')
        else:
            logging.info(f'{datetime.now().strftime("%Y-%m-%d::%H-%M-%S")}: Message response is failure')
        return [header , lst1]
    except Exception as e:
        return str(e)

def main(url):
    st = time.time()
    logging.info(f'{datetime.now().strftime("%Y-%m-%d::%H-%M-%S")}: Program started')
    resp_lst = call_astros_api(url)
    status_code = resp_lst[0]
    content = resp_lst[1]
    if status_code == 200:
        response_process_data = process_data(json.loads(content))
        if type(response_process_data) != str:
            logging.info(datetime.now().strftime("%Y-%m-%d::%H-%M-%S") + ": Inserting records inside a csv file")
            resp_file = data_insert(path=os.getcwd(), header=response_process_data[0], data=response_process_data[1])
            if resp_file == 'Success':
                logging.info(datetime.now().strftime("%Y-%m-%d::%H-%M-%S") + ": Records inserted successfully")
            else:
                logging.info(
                    datetime.now().strftime(
                        "%Y-%m-%d::%H-%M-%S") + ": An error occurred during data insertion: {0}".format(
                        resp_file))
                if os.path.isfile(os.getcwd() + '\\space_craftfile.csv'):
                    os.remove(os.getcwd() + '\\space_craftfile.csv')
                else:
                    pass
        else:
            logging.info(f'{datetime.now().strftime("%Y-%m-%d::%H-%M-%S")}: An error occurred processing the data')
    else:
        logging.info(datetime.now().strftime("%Y-%m-%d::%H-%M-%S") + ":Response Message {0}".format(content))
    et = time.time()
    logging.info(f'{datetime.now().strftime("%Y-%m-%d::%H-%M-%S")}: Execution time: {et - st} seconds')


if __name__ == '__main__':
    main(url)