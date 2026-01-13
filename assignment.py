import json

from dateutil.relativedelta import relativedelta

#Loading Data
with open('precipitation.json', encoding='utf-8') as file:
    data = json.load(file)

#Manually selecting for Seattle
seattle_code = 'GHCND:US1WAKG0038'
filtered_observations = []
#Filtering observations based on station code (Seattle)
for observation in data:
    if observation['station'] == seattle_code:
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
    total_monthly_precipitation.append(sum_precipitation)

relative_monthly_precipitation = []
#Calculating relative monthly precipitation (mutate table)
for value in total_monthly_precipitation:
    relative_monthly_precipitation.append(value/total_yearly_precipitation) #unrounded float values

#Finalizing data in the format specified
results = {
    'Seattle':
        {
            'station': 'GHCND:US1WAKG0038',
            'state': 'WA',
            'total_monthly_precipitation': total_monthly_precipitation,
            'total_yearly_precipitation': total_yearly_precipitation,
            'relative_monthly_precipitation': relative_monthly_precipitation,
        }
}

with open('results.json', 'w', encoding='utf-8') as file:
    json.dump(results, file, indent=4)
