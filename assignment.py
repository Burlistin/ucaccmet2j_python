import json

#Initializing Output Dict
results_dict = {}
#Initializing yearly sum over all locations variable
yearly_total = 0

#Loading CVS info
with open('stations.csv', encoding='utf-8') as file:
    file.readline() #popping first line (column names) off the file
    for line in file.readlines():
        line = line.strip()
        variables = line.split(',') #getting a list of all variables per observation
        results_dict[variables[0]] = {
            'station': variables[2],
            'state': variables[1],
        }

#Loading Data
with open('precipitation.json', encoding='utf-8') as file:
    data = json.load(file)

#Applying the same analysis code to each city
for city_key in results_dict:
    #Selecting station through iteration
    station_code = results_dict[city_key]['station']
    filtered_observations = []
    #Filtering observations based on station code (Seattle)
    for observation in data:
        if observation['station'] == station_code:
            filtered_observations.append(observation)


    grouped_observations = {}
    #Grouping the filtered observations per month
    for observation in filtered_observations:
        month = observation['date'].split('-')[1] #Getting the month as a number
        if month not in grouped_observations:
            grouped_observations[month] = [observation]
        else:
            grouped_observations[month].append(observation)


    total_monthly_precipitation = []
    total_yearly_precipitation = 0
    #Summarizing precipitation values per month group
    for key in grouped_observations:
        sum_precipitation = 0
        for observation in grouped_observations[key]:
            sum_precipitation += observation['value']
            #Calculating total yearly precipitation throughout all the months
            total_yearly_precipitation += observation['value']
            #Calculating total yearly precipitation over all locations
            yearly_total += observation['value']
        total_monthly_precipitation.append(sum_precipitation)


    relative_monthly_precipitation = []
    #Calculating relative monthly precipitation (mutate table)
    for value in total_monthly_precipitation:
        relative_monthly_precipitation.append(value/total_yearly_precipitation) #unrounded float values


    #Adding total_monthly, total_yearly, and relative_monthly precipitation to the results dict
    results_dict[city_key]['total_monthly_precipitation'] = total_monthly_precipitation
    results_dict[city_key]['total_yearly_precipitation'] = total_yearly_precipitation
    results_dict[city_key]['relative_monthly_precipitation'] = relative_monthly_precipitation


#Calculating relative yearly participation (mutate)
for city_key in results_dict.copy(): #using .copy() so we don't change the size of the dict during iteration
    relative_yearly_precipitation = results_dict[city_key]['total_yearly_precipitation'] / yearly_total #unrounded
    results_dict[city_key]['relative_yearly_precipitation'] = relative_yearly_precipitation

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(results_dict, file, indent=4)
