# -*- coding: utf-8 -*-
import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}

for f in data_files:
    d = pd.read_csv("schools/"+f)
    key_name = f.replace(".csv", "")
    data[key_name] = d
        
print(data['sat_results'].head())

for key in data:
    print(data[key].head())

all_survey = pd.read_csv("schools/survey_all.txt", delimiter="\t", encoding="windows-1252")
d75_survey = pd.read_csv("schools/survey_d75.txt", delimiter="\t", encoding="windows-1252")
survey = pd.concat([all_survey, d75_survey], axis=0)
print(survey.head())

survey['DBN'] = survey['dbn']
cols = ["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]
survey = survey.loc[:, cols]
data['survey'] = survey        
        
def doubledigit(x):
    if len(str(x)) == 1:
        return str(x).zfill(2)
    elif len(str(x)) == 2:
        return x

data['hs_directory']['DBN'] = data['hs_directory']['dbn']
data['class_size']['padded_csd'] = data['class_size']['CSD'].apply(doubledigit)
data['class_size']['DBN'] = data['class_size']['padded_csd'].map(str) + data['class_size']['SCHOOL CODE']
print(data['class_size'].head())

print(data['sat_results'].head())
data['sat_results']['SAT Critical Reading Avg. Score'] = pd.to_numeric(data['sat_results']['SAT Critical Reading Avg. Score'], errors = 'coerce')
data['sat_results']['SAT Math Avg. Score'] = pd.to_numeric(data['sat_results']['SAT Math Avg. Score'], errors = 'coerce')
data['sat_results']['SAT Writing Avg. Score'] = pd.to_numeric(data['sat_results']['SAT Writing Avg. Score'], errors = 'coerce')
data['sat_results']['sat_score'] = data['sat_results']['SAT Math Avg. Score'] + data['sat_results']['SAT Critical Reading Avg. Score'] + data['sat_results']['SAT Writing Avg. Score']
print(data['sat_results']['sat_score'].head())

import re
x = "1110 Boston Road\nBronx, NY 10456\n(40.8276026690005, -73.90447525699966)"
lat = re.findall("\(.+, .+\)", x)
sp = str(lat).split(sep=',')
sp1 = re.sub("\[\'\(", "", sp[0])

import re
def lat(x):
    cords = re.findall("\(.+, .+\)", x)
    cords_split = str(cords).split(sep=',')
    lat = re.sub("\[\'\(", "", cords_split[0])
    return lat

data['hs_directory']['lat'] = data['hs_directory']['Location 1'].apply(lat)
print(data['hs_directory'].head())

def long(x):
    cords = re.findall("\(.+, .+\)", x)
    cords_split = str(cords).split(sep=',')
    long = re.sub("\)\'\]", "", cords_split[1])
    return long

data['hs_directory']['lon'] = data['hs_directory']['Location 1'].apply(long)
print(data['hs_directory'].head())

data['hs_directory']['lat'] = pd.to_numeric(data['hs_directory']['lat'], errors = 'coerce')
data['hs_directory']['lon'] = pd.to_numeric(data['hs_directory']['lon'], errors = 'coerce')
print(data['hs_directory'].head())

class_size = data['class_size']
class_bool = class_size['GRADE '] == '09-12'
class_size = class_size[class_bool]
class_boo = class_size['PROGRAM TYPE'] == 'GEN ED'
class_size = class_size[class_boo]
print(class_size.head())

import numpy as np
class_size = class_size.groupby(['DBN']).aggregate(np.mean)
class_size.reset_index(inplace= 'TRUE')
data['class_size'] = class_size
print(data['class_size'].head())

demo_bool = data['demographics']['schoolyear'] == 20112012
data['demographics'] = data['demographics'][demo_bool]
print(data['demographics'].head())

grad_bool = data['graduation']['Cohort'] == '2006'
data['graduation'] = data['graduation'][grad_bool]
grad_boo = data['graduation']['Demographic'] == 'Total Cohort'
data['graduation'] = data['graduation'][grad_boo]
print(data['graduation'].head())

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']
for col in cols:
    data['ap_2010'][col] = pd.to_numeric(data['ap_2010'][col], errors = 'coerce')
print(data['ap_2010'].head())

combined = data["sat_results"].merge(data['ap_2010'], how='left', on='DBN')
combined = combined.merge(data['graduation'], how='left', on='DBN')
print(combined.head())

combined = combined.merge(data['class_size'], how='inner', on='DBN')
combined = combined.merge(data['demographics'], how='inner', on='DBN')
combined = combined.merge(data['survey'], how='inner', on='DBN')
combined = combined.merge(data['hs_directory'], how='inner', on='DBN')
print(combined.head())
combined.shape

means = combined.mean()
combined = combined.fillna(means)
combined = combined.fillna(0)
print(combined.head())

def chara_extract(x):
    y = x[0:2]
    return y
combined['school_dist'] = combined['DBN'].apply(chara_extract)
print(combined['school_dist'].head())

# Data Analysis and Visualisation

correlations = combined.corr()['sat_score']
print(correlations.head())

import matplotlib.pyplot as plt
combined.plot.scatter(x='total_enrollment', y='sat_score')
plt.show()

low_enrollment = combined[combined['total_enrollment'] < 1000]
low_enrollment = combined[combined['sat_score'] < 1000]
print(low_enrollment['School Name'])

import matplotlib.pyplot  as plt
combined.plot.scatter(x='ell_percent', y='sat_score')
plt.show()

from mpl_toolkits.basemap import Basemap 
m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)
m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

longitudes = combined['lon'].tolist()
latitudes = combined['lat'].tolist()

m.scatter(longitudes,latitudes, s=20, zorder=2, latlon=True, c=combined['ell_percent'], cmap='summer')
plt.show()

import numpy as np
districts = combined.groupby(['school_dist']).aggregate(np.mean)
districts.reset_index(inplace=True)
print(districts.head())

from mpl_toolkits.basemap import Basemap 
m = Basemap(
    projection='merc', 
    llcrnrlat=40.496044, 
    urcrnrlat=40.915256, 
    llcrnrlon=-74.255735, 
    urcrnrlon=-73.700272,
    resolution='i'
)
m.drawmapboundary(fill_color='#85A6D9')
m.drawcoastlines(color='#6D5F47', linewidth=.4)
m.drawrivers(color='#6D5F47', linewidth=.4)

longitudes = districts['lon'].tolist()
latitudes = districts['lat'].tolist()

m.scatter(longitudes,latitudes, s=20, zorder=2, latlon=True, c=districts['ell_percent'], cmap='summer')
plt.show()




