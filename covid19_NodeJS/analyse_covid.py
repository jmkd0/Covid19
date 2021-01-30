import sys, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def data_analyse():
    etats_covid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
    confirmed_covid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    recovered_covid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    deaths_covid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

    lines = sys.stdin.readlines()
    request = np.array(json.loads(lines[0]))
    if request[1] == None or request[1] == '0':
        global_world = etats_covid.filter(['Confirmed', 'Deaths', 'Recovered', 'Active'], axis=1)
        data = global_world.sum()
        conf_world = confirmed_covid.filter([request[2], request[3]], axis=1)
        recovered_world = recovered_covid.filter([request[2], request[3]], axis=1)
        deaths_world = deaths_covid.filter([request[2], request[3]], axis=1)
        result = ["Nean","Nean","Nean","Nean","Nean","World","Nean",data[0],data[3],data[2],data[1]]
        if len(conf_world.columns) == 2:
            summ = conf_world.sum()
            result[2] = str(np.abs(summ[1]-summ[0]))
        if len(recovered_world.columns) == 2:
            summ = recovered_world.sum()
            result[3] = str(np.abs(summ[1]-summ[0]))
        if len(deaths_world.columns) == 2:
            summ = deaths_world.sum()
            result[4] = str(np.abs(summ[1]-summ[0]))
        
        return sendData(result)
    else:
        data = etats_covid[etats_covid["Country_Region"] == request[1]].values
        

        result = ["Nean","Nean","Nean","Nean","Nean",request[1],data[0][1],data[0][4],data[0][7],data[0][6],data[0][5]]
        #Confirmed case
        if request[2] in confirmed_covid.columns and request[3] in confirmed_covid.columns:
            position = np.where(confirmed_covid["Country/Region"] == request[1])
            begin = confirmed_covid[request[2]][position[0][0]]
            end = confirmed_covid[request[3]][position[0][0]]
            result[2] = str(np.abs(end - begin))
        #Recovered case
        if request[2] in recovered_covid.columns and request[3] in recovered_covid.columns:
            position = np.where(confirmed_covid["Country/Region"] == request[1])
            begin = recovered_covid[request[2]][position[0][0]]
            end = recovered_covid[request[3]][position[0][0]]
            result[3] = str(np.abs(end - begin))
        #Deaths case
        if request[2] in deaths_covid.columns and request[3] in deaths_covid.columns:
            position = np.where(confirmed_covid["Country/Region"] == request[1])
            begin = deaths_covid[request[2]][position[0][0]]
            end = deaths_covid[request[3]][position[0][0]]
            result[4] = str(np.abs(end - begin))
        
        return sendData(result)


def sendData(data):
    res = {
            "begin_date":       data[0],
            "end_date":         data[1],
            "search_confirmed": data[2],
            "search_recovered": data[3],
            "search_deaths":    data[4],
            "Country" :         data[5],
            "Last_Update":      data[6],
            "Confirmed":        data[7],
            "Active":           data[8],
            "Recovered":        data[9],
            "Deaths":           data[10]
        }
    response = json.dumps(res)
    return response


    

print("voll")
if __name__ == '__main__':
    #result = data_analyse()
    print("cool")
    #print(result)