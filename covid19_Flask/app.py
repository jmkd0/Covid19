from flask import Flask, render_template, request, jsonify #pip install flask
import datetime
import pandas as pd # pip install pandas
import json 
import numpy as np # pip install numpy
#from sklearn.preprocessing import PolynomialFeatures # pip install scikit-learn
#from sklearn import linear_model# pip install scikit-learn==0.23.2


# Create your views here.
app = Flask(__name__)

@app.route("/")
def target():
	return render_template('index.html')

@app.route("/view_world")
def covidView():
    predict = False
    result = covidWholeWorld(predict,"")
    
    return render_template("covid-19.html", response = result)

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
    #if predict == True:
    #    endDate = datetime.datetime.strptime(predictedDate, '%Y-%m-%d')
    #    day = endDate.strftime("%d")
    #    mounth = endDate.strftime("%B")
    #    year = endDate.strftime("%Y")
    #    predictedDate = day+" "+mounth+" "+year
    #    #Forcaste Confirmed
    #    confirmedForcast = forcasteCases(confirmedCovid, endDate)
    #    #Forcaste Recovered
    #    recoveredForcast = forcasteCases(recoveredCovid, endDate)
    #    #Forcaste Death
    #    deathsForcast = forcasteCases(deathsCovid, endDate)
    #Diagram
    evolutionDatas = calculateDiagramm(confirmedCovid, recoveredCovid, deathsCovid)
    #confirmedDiagramm = countryAndLastConfirmed['values'].values.tolist()
    #Map
    mapDataFormat = mapDataCalculate(evolutionDatas)
    mapDataFormat = mapDataFormat.to_json(orient='records')
    
    #Convert each column to list
    countryNames = evolutionDatas['Country/Region'].values.tolist()
    confirmedDiagramm = evolutionDatas['confirme_values'].values.tolist()
    recoveredDiagramm = evolutionDatas['recovered_values'].values.tolist()
    deathsDiagramm = evolutionDatas['death_values'].values.tolist()

    
    result = {
        'country': " The Whole World",
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
        'confirmedDiagrammLine': None,
        'recoveredDiagrammLine': None,
        'deathsDiagrammLine': None,
        'mapAndProgression': mapDataFormat,
        'abscisse': None,
        'showMap': True,
        'predict': predict,
        'predictedDate':predictedDate,
        'confirmedForcast': confirmedForcast - wholeConfirmedCase,
        'recoveredForcast': recoveredForcast - wholeRecoveredCase,
        'deathsForcast': deathsForcast - wholeDeathsCase
    }
    return result

@app.route("/view_country", methods=['POST', 'GET'])
def viewCountry():
    countryName = request.form['country']
    predictedDate = request.form['date']

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

        #Diagram
        evolutionDatas = calculateDiagramm(confirmedCovid, recoveredCovid, deathsCovid)
        #confirmedDiagramm = countryAndLastConfirmed['values'].values.tolist()

        #Convert each column to list
        countryNames = evolutionDatas['Country/Region'].values.tolist()
        confirmedDiagramm = evolutionDatas['confirme_values'].values.tolist()
        recoveredDiagramm = evolutionDatas['recovered_values'].values.tolist()
        deathsDiagramm = evolutionDatas['death_values'].values.tolist()

        #Diagram line
        abscisse, confirmedDiagrammLine, recoveredDiagrammLine, deathsDiagrammLine = calculateDiagrammLine(countryName, confirmedCovid, recoveredCovid, deathsCovid)
       
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
            'mapAndProgression': None,
            'abscisse': abscisse,
            'showMap': False,
            'predict': predict,
            'predictedDate':predictedDate,
            'confirmedForcast': confirmedForcast - int(countryConfirmedCase),
            'recoveredForcast': recoveredForcast - int(countryRecoveredCase),
            'deathsForcast': deathsForcast - int(countryDeathsCase)
        }
        return render_template("covid-19.html", response = result)
    else:
        result = covidWholeWorld(predict, predictedDate)
        return render_template("covid-19.html", response = result)
    

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
    countryAndLastConfirmed.columns = ['Country/Region', 'confirme_values'] #Rename the second column ex: 8/9/20 to confirm_values

    evolutionDatas = countryAndLastConfirmed.sort_values(by='confirme_values', ascending=False)  #sort datas by confirmed case descending
        
    #Recovered
    countryAndLastRecovered = recoveredCovid[['Country/Region', recoveredCovid.columns[-1]]] #Get the country name and the last columns
    countryAndLastRecovered = countryAndLastRecovered.groupby('Country/Region').sum()  #Group the repeat country and sum thier confirmed case
    countryAndLastRecovered = countryAndLastRecovered.reset_index() #reset index to not have 0 1 4 5 7 after grouping
    countryAndLastRecovered.columns = ['Country/Region', 'recovered_values'] #Rename the second column ex: 8/9/20 to values
    
    evolutionDatas = pd.merge(evolutionDatas, countryAndLastRecovered, on='Country/Region') #perform inner join
    
    
    #Deaths
    countryAndLastDeaths = deathsCovid[['Country/Region', deathsCovid.columns[-1]]] #Get the country name and the last columns
    countryAndLastDeaths = countryAndLastDeaths.groupby('Country/Region').sum()  #Group the repeat country and sum thier confirmed case
    countryAndLastDeaths = countryAndLastDeaths.reset_index() #reset index to not have 0 1 4 5 7 after grouping
    countryAndLastDeaths.columns = ['Country/Region', 'death_values'] #Rename the second column ex: 8/9/20 to values

    evolutionDatas = pd.merge(evolutionDatas, countryAndLastDeaths, on='Country/Region') #perform inner join
 
    return evolutionDatas

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


def mapDataCalculate(evolutionDatas):
    #Receive map data from the json file
    #https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json
    #Get country info at the format: code3 name value code
    mapData = pd.read_json('https://cdn.jsdelivr.net/gh/highcharts/highcharts@v7.0.0/samples/data/world-population-density.json')
    oldName = ["United States","Russian Federation","Iran, Islamic Rep.","Egypt, Arab Rep.","Venezuela, RB","Kyrgyz Republic","Czech Republic","Korea, Dem. People’s Rep.","Macedonia, FYR","Zambia","Congo, Dem. Rep.","Slovak Republic","Estonia","Congo, Rep.","Syrian Arab Republic","Gambia, The","Angola","Bahamas, The","Yemen, Rep.","St. Vincent and the Grenadines","Brunei Darussalam","St. Lucia","St. Kitts and Nevis"]
    newName = ["US","Russia","Iran","Egypt","Venezuela","Kyrgyzstan","Czechia","Korea, South","North Macedonia","Zambia","Congo (Kinshasa)","Slovakia","Eswatini","Congo (Brazzaville)","Syria","Gambia","Angola","Bahamas","Yemen","Saint Vincent and the Grenadines","Brunei","Saint Lucia","Saint Kitts and Nevis"]
    
    for i in range(len(oldName)):
        mapData.loc[(mapData.name == oldName[i]),'name']=newName[i]

    confirmedCase = evolutionDatas[["Country/Region", "confirme_values"]]
    confirmedCase = pd.merge(mapData, confirmedCase, left_on='name', right_on='Country/Region', how='left')
    confirmedCase = confirmedCase[["code3", "name", "confirme_values", "code"]]
    confirmedCase = confirmedCase.rename(columns={"confirme_values":"value"})
    return confirmedCase


if __name__ == '__main__':
   app.run(debug = True, port='4000')


