from django.shortcuts import render
import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model



# Create your views here.
def covidView(request):
    predict = False
    result = covidWholeWorld(predict,"")
    return render(request, 'covid.html', result)

def covidWholeWorld(predict, predictedDate):
    statesCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
    confirmedCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    recoveredCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
    deathsCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    #Whole cases
    wholeConfirmedCase = confirmedCovid[confirmedCovid.columns[-1]].sum() 
    wholeRecoveredCase = recoveredCovid[recoveredCovid.columns[-1]].sum() 
    wholeDeathsCase = deathsCovid[deathsCovid.columns[-1]].sum() 

    confirmedForcast, recoveredForcast, deathsForcast = [0,0,0]
    if predict == True:
        endDate = datetime.datetime.strptime(predictedDate, '%Y-%m-%d')
        day = endDate.strftime("%d")
        mounth = endDate.strftime("%B")
        year = endDate.strftime("%Y")
        predictedDate = day+" "+mounth+" "+year
        #Forcaste Confirmed
        confirmedForcast = forcasteCases(confirmedCovid, endDate)
        #Forcaste Recovered
        recoveredForcast = forcasteCases(recoveredCovid, endDate)
        #Forcaste Death
        deathsForcast = forcasteCases(deathsCovid, endDate)
    #Diagram
    countryNames, countryAndLastConfirmed, recoveredDiagramm, deathsDiagramm = calculateDiagramm(confirmedCovid, recoveredCovid, deathsCovid)
    confirmedDiagramm = countryAndLastConfirmed['values'].values.tolist()
    #Map
    mapDataFormat = mapDataCalculate(countryAndLastConfirmed, countryNames)

    
    result = {
        'country': " the Whole World",
        'lastUpdate': "Currently",
        'wholeConfirmed': wholeConfirmedCase,
        'wholeRecovered': wholeRecoveredCase,
        'wholeDeaths': wholeDeathsCase,
        'wholeActive': wholeConfirmedCase - wholeRecoveredCase - wholeDeathsCase,
        'rateRecovered': round((wholeRecoveredCase/wholeConfirmedCase)*100, 2),
        'rateDeaths': round((wholeDeathsCase/wholeConfirmedCase)*100, 2),
        'countryNames': countryNames,
        'confirmedDiagramm': confirmedDiagramm,
        'recoveredDiagramm': recoveredDiagramm,
        'deathsDiagramm': deathsDiagramm,
        'mapAndProgression': mapDataFormat,
        'showMap': True,
        'predict': predict,
        'predictedDate':predictedDate,
        'confirmedForcast': confirmedForcast - wholeConfirmedCase,
        'recoveredForcast': recoveredForcast - wholeRecoveredCase,
        'deathsForcast': deathsForcast - wholeDeathsCase
    }
    return result

def viewCountry(request):
    countryName = request.POST['country']
    predictedDate = request.POST['date']

    predict = False
    if predictedDate is not None and predictedDate != '':
        predict = True
    
    if countryName is not None and countryName != '':
        statesCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')
        confirmedCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
        recoveredCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
        deathsCovid = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
        #Whole cases
        wholeConfirmedCase = confirmedCovid[confirmedCovid.columns[-1]].sum() 
        wholeRecoveredCase = recoveredCovid[recoveredCovid.columns[-1]].sum() 
        wholeDeathsCase = deathsCovid[deathsCovid.columns[-1]].sum() 

        confirmedForcast, recoveredForcast, deathsForcast= [0,0,0]
        if predict == True:
            endDate = datetime.datetime.strptime(predictedDate, '%Y-%m-%d')
            day = endDate.strftime("%d")
            mounth = endDate.strftime("%B")
            year = endDate.strftime("%Y")
            predictedDate = day+" "+mounth+" "+year
            #Forcaste Confirmed
            dailyConfirmed = confirmedCovid[confirmedCovid['Country/Region']==countryName]
            confirmedForcast = forcasteCases(dailyConfirmed, endDate)
            #Forcaste Recovered
            dailyRecovered = recoveredCovid[recoveredCovid['Country/Region']==countryName]
            recoveredForcast = forcasteCases(dailyRecovered, endDate)
            #Forcaste Death
            dailyDeaths = deathsCovid[deathsCovid['Country/Region']==countryName]
            deathsForcast = forcasteCases(dailyDeaths, endDate)

        #Diagram barre
        countryNames, countryAndLastConfirmed, recoveredDiagramm, deathsDiagramm = calculateDiagramm(confirmedCovid, recoveredCovid, deathsCovid)
        #Diagram line
        abscisse, confirmedDiagrammLine, recoveredDiagrammLine, deathsDiagrammLine = calculateDiagrammLine(countryName, confirmedCovid, recoveredCovid, deathsCovid)


        confirmedDiagramm = countryAndLastConfirmed['values'].values.tolist()
        #Country case
        statesCases = statesCovid.filter(['Country_Region','Last_Update','Confirmed', 'Deaths', 'Recovered', 'Active'], axis=1)
        statesCases = statesCases[statesCases['Country_Region']==countryName]
        #Date managing
        lastUpdate = statesCases.loc[statesCases.Country_Region == countryName, 'Last_Update'].values[0]
        date = datetime.datetime.strptime(lastUpdate, '%Y-%m-%d %H:%M:%S')
        dayName = date.strftime("%A")
        day = date.strftime("%d")
        mounth = date.strftime("%B")
        year = date.strftime("%Y")
        hour = date.strftime("%H")
        minute = date.strftime("%M")
        second = date.strftime("%S")
        lastUpdate = dayName+", "+day+" "+mounth+" "+year+" at "+hour+":"+minute+":"+second

        countryConfirmedCase = statesCases.loc[statesCases.Country_Region == countryName, 'Confirmed'].values[0]
        countryRecoveredCase = statesCases.loc[statesCases.Country_Region == countryName, 'Recovered'].values[0]
        countryDeathsCase = statesCases.loc[statesCases.Country_Region == countryName, 'Deaths'].values[0]
        countryActiveCase = statesCases.loc[statesCases.Country_Region == countryName, 'Active'].values[0]

        result = {
            'country': countryName,
            'lastUpdate': lastUpdate,
            'wholeConfirmed': int(countryConfirmedCase),
            'wholeRecovered': int(countryRecoveredCase),
            'wholeDeaths': int(countryDeathsCase),
            'wholeActive': int(countryActiveCase),
            'rateRecovered': round((countryRecoveredCase/countryConfirmedCase)*100, 2),
            'rateDeaths': round((countryDeathsCase/countryConfirmedCase)*100, 2),
            'countryNames': countryNames,
            'confirmedDiagramm': confirmedDiagramm,
            'recoveredDiagramm': recoveredDiagramm,
            'deathsDiagramm': deathsDiagramm,
            'confirmedDiagrammLine': confirmedDiagrammLine,
            'recoveredDiagrammLine': recoveredDiagrammLine,
            'deathsDiagrammLine': deathsDiagrammLine,
            'abscisse': abscisse,
            'showMap': False,
            'predict': predict,
            'predictedDate':predictedDate,
            'confirmedForcast': confirmedForcast - int(countryConfirmedCase),
            'recoveredForcast': recoveredForcast - int(countryRecoveredCase),
            'deathsForcast': deathsForcast - int(countryDeathsCase)
        }
        return render(request, 'covid.html', result)
    else:
        result = covidWholeWorld(predict, predictedDate)
        return render(request, 'covid.html', result)
    

def forcasteCases(dailyCases, endDate):
    dailyCases = dailyCases[dailyCases.columns[4:]]
    dailyCases = dailyCases.sum()
    dailyCases = pd.DataFrame(dailyCases).reset_index()
    dailyCases.columns = ['dates', 'Cases']
    currentDate = dailyCases['dates'].values.tolist()[-1]
    currentCase = dailyCases['Cases'].values.tolist()[-1]
    currentDate = datetime.datetime.strptime(currentDate, '%m/%d/%y')
    numberDays = (endDate - currentDate).days

    x = dailyCases.index.values
    x = np.array(x).reshape(-1,1)
    y = dailyCases['Cases'].values.tolist()

    #Trainning 
    polyFeat = PolynomialFeatures(degree=4)
    x = polyFeat.fit_transform(x)
    model = linear_model.LinearRegression()
    model.fit(x,y)
    accuracy = model.score(x,y)
    y0 = model.predict(x)
    #Prediction
    transf = polyFeat.fit_transform([[len(x)-1+numberDays]])
    prediction = model.predict(transf)
    prediction = int(prediction)
    return prediction

def calculateDiagramm(confirmedCovid, recoveredCovid, deathsCovid):
    #Confirmed
    countryAndLastConfirmed = confirmedCovid[['Country/Region', confirmedCovid.columns[-1]]] #Get the country name and the last columns
    countryAndLastConfirmed = countryAndLastConfirmed.groupby('Country/Region').sum()  #Group the repeat country and sum thier confirmed case
    countryAndLastConfirmed = countryAndLastConfirmed.reset_index() #reset index to not have 0 1 4 5 7 after grouping
    countryAndLastConfirmed.columns = ['Country/Region', 'values'] #Rename the second column ex: 8/9/20 to values
    countryAndLastConfirmed = countryAndLastConfirmed.sort_values(by='values', ascending=False)  #sort datas by confirmed case descending
    #Convert each column to list
    countryNames = countryAndLastConfirmed['Country/Region'].values.tolist()
    
    #Recovered
    countryAndLastRecovered = recoveredCovid[['Country/Region', recoveredCovid.columns[-1]]] #Get the country name and the last columns
    countryAndLastRecovered = countryAndLastRecovered.groupby('Country/Region').sum()  #Group the repeat country and sum thier confirmed case
    countryAndLastRecovered = countryAndLastRecovered.reset_index() #reset index to not have 0 1 4 5 7 after grouping
    countryAndLastRecovered.columns = ['Country/Region', 'values'] #Rename the second column ex: 8/9/20 to values
    recoveredDiagramm = []
    for country in countryNames:
        countryInfo = countryAndLastRecovered[countryAndLastRecovered['Country/Region']==country]
        recoveredDiagramm.append(list(countryInfo['values'].values)[0])

    #Deaths
    countryAndLastDeaths = deathsCovid[['Country/Region', deathsCovid.columns[-1]]] #Get the country name and the last columns
    countryAndLastDeaths = countryAndLastDeaths.groupby('Country/Region').sum()  #Group the repeat country and sum thier confirmed case
    countryAndLastDeaths = countryAndLastDeaths.reset_index() #reset index to not have 0 1 4 5 7 after grouping
    countryAndLastDeaths.columns = ['Country/Region', 'values'] #Rename the second column ex: 8/9/20 to values
    deathsDiagramm = []
    for country in countryNames:
        countryInfo = countryAndLastDeaths[countryAndLastDeaths['Country/Region']==country]
        deathsDiagramm.append(list(countryInfo['values'].values)[0])
    
    return countryNames, countryAndLastConfirmed, recoveredDiagramm, deathsDiagramm

def calculateDiagrammLine(countryName, confirmedCovid, recoveredCovid, deathsCovid):
    #Confirmed
    dailyConfirmed = confirmedCovid[confirmedCovid['Country/Region']==countryName]
    dailyConfirmed = dailyConfirmed[dailyConfirmed.columns[4:]]
    dailyConfirmed = dailyConfirmed.sum()#if one country have more than one raw sum it
    dailyConfirmed = pd.DataFrame(dailyConfirmed).reset_index()
    dailyConfirmed.columns = ['dates', 'values']#rename colums
    dailyConfirmed['yesterday'] = dailyConfirmed['values'].shift(1).fillna(0)#add new column inside shift all values to the next column and fill the NaN with 0
    dailyConfirmed['day'] = dailyConfirmed['values'] - dailyConfirmed['yesterday']
    confirmedDiagrammLine = dailyConfirmed['day'].values.tolist()
    abscisse = dailyConfirmed['dates'].values.tolist()
    #recovered
    dailyRecovered = recoveredCovid[recoveredCovid['Country/Region']==countryName]
    dailyRecovered = dailyRecovered[dailyRecovered.columns[4:]]
    dailyRecovered = dailyRecovered.sum()#if one country have more than one raw sum it
    dailyRecovered = pd.DataFrame(dailyRecovered).reset_index()
    dailyRecovered.columns = ['dates', 'values']#rename colums
    dailyRecovered['yesterday'] = dailyRecovered['values'].shift(1).fillna(0)#add new column inside shift all values to the next column and fill the NaN with 0
    dailyRecovered['day'] = dailyRecovered['values'] - dailyRecovered['yesterday']
    recoveredDiagrammLine = dailyRecovered['day'].values.tolist()
    #Deaths
    dailyDeaths = deathsCovid[deathsCovid['Country/Region']==countryName]
    dailyDeaths = dailyDeaths[dailyDeaths.columns[4:]]
    dailyDeaths = dailyDeaths.sum()#if one country have more than one raw sum it
    dailyDeaths = pd.DataFrame(dailyDeaths).reset_index()
    dailyDeaths.columns = ['dates', 'values']#rename colums
    dailyDeaths['yesterday'] = dailyDeaths['values'].shift(1).fillna(0)#add new column inside shift all values to the next column and fill the NaN with 0
    dailyDeaths['day'] = dailyDeaths['values'] - dailyDeaths['yesterday']
    deathsDiagrammLine = dailyDeaths['day'].values.tolist()

    return abscisse, confirmedDiagrammLine, recoveredDiagrammLine, deathsDiagrammLine


def mapDataCalculate(countryAndLastConfirmed, countryNames):
    #Receive map data from the json file
    #https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json
    #Get country info at the format: code3 name value code
    mapData = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
    oldName = ["United States","Russian Federation","Iran, Islamic Rep.","Egypt, Arab Rep.","Venezuela, RB","Kyrgyz Republic","Czech Republic","Korea, Dem. People’s Rep.","Macedonia, FYR","Zambia","Congo, Dem. Rep.","Slovak Republic","Estonia","Congo, Rep.","Syrian Arab Republic","Gambia, The","Angola","Bahamas, The","Yemen, Rep.","St. Vincent and the Grenadines","Brunei Darussalam","St. Lucia","St. Kitts and Nevis"]
    newName = ["US","Russia","Iran","Egypt","Venezuela","Kyrgyzstan","Czechia","Korea, South","North Macedonia","Zambia","Congo (Kinshasa)","Slovakia","Eswatini","Congo (Brazzaville)","Syria","Gambia","Angola","Bahamas","Yemen","Saint Vincent and the Grenadines","Brunei","Saint Lucia","Saint Kitts and Nevis"]
  
    for i in range(len(oldName)):
        mapData.loc[(mapData.name == oldName[i]),'name']=newName[i]

    mapDataFormat = []
    for country in countryNames:
        try:
            
            countryInfo = mapData[mapData['name']==country]
            data = {}
            data["code3"] = list(countryInfo['code3'].values)[0]
            data["name"] = country
            data["value"] = countryAndLastConfirmed[countryAndLastConfirmed['Country/Region']==country]['values'].sum()
            data["code"] = list(countryInfo['code'].values)[0]
            mapDataFormat.append(data)
        except:
            pass
    return mapDataFormat


