import pandas as pd
pd.set_option("max_rows", 2000)
pd.set_option("max_columns", 500)

# US Refugee Resettlement Data 1975-2018
# https://www.refugeeresettlementdata.com/data.html
# Dreher, A., Langlotz, S., Matzat, J., Parsons, C. and Mayda, A. (2020). Immigration, Political Ideologies and the Polarization of American Politic
data = pd.read_stata("orr_prm_1975_2018_v1.dta")

# Calfornia State Association of Counties Population Estimates for Counties and Cities - 1970 to 2018
# https://www.counties.org/data-and-research
popdata = pd.read_excel("population_by_jurisdiction_and_by_county_-_1970_to_2018_-_09-07-2018.xlsx")

print("Refugee Countries")
print(data.citizenship_stable.unique())
print(len(data.citizenship_stable.unique()))

# Refugee Countries with a Majority/Dominant Muslim Percentage Population (>50%) or State Religion https://www.nationsonline.org/oneworld/muslim-countries.htm
muslim_countries = ["afghanistan", "iran", "iraq", "indonesia", "palestine", "somalia", "sudan", 
                    "albania", "syria", "bangladesh", "egypt", "libya", "nigeria", "jordan",
                    "pakistan", "yemen", "algeria", "lebanon", "saudi arabia", "gambia",
                    "senegal", "tunisia", "oman", "turkey", "kuwait", "malaysia", "maruitania",
                    "djibouti", "united arab emirates", "mali", "niger", "maldives", "bahrain",
                    "brunei"] 
# Middle Eastern Muslim Countries, according to above and https://en.wikipedia.org/wiki/Middle_East also including Afghanistan
# There are many Muslim Countries in Africa and South East Asia, but the more colloquial american perception of Muslim countries is only middle eastern
middle_eastern_muslim_countries = ["afghanistan", "iran", "iraq", "palestine", "syria",
                                   "egypt", "jordan", "yemen", "lebanon", "saudi arabia",
                                   "oman", "turkey", "kuwait", "united arab emirates","bahrain"] 
                                   
# California bound refugees from Muslim countries Data from 1998-2018
cmd = data.loc[(data.citizenship_stable.isin(muslim_countries)) & (data.state_fips == "06") & (data.year >= 1998)]
# California bound refugees from Middle Eastern Muslim countries Data from 1998-2018
cmemd = data.loc[(data.citizenship_stable.isin(middle_eastern_muslim_countries)) & (data.state_fips == "06") & (data.year >= 1998)]

# Population Data of calfornia by Counties and Jurisdiction per year
pdcj = popdata.loc[(popdata.Year >= 1998) & (popdata.County.isin(cmd.county10name.unique()))]
# Population Data of calfornia by Counties per year
pdc = pdcj.groupby(["County", "Year"]).sum()

# California bound refugees from Muslim countries Data from 1998-2018 With Population data of calfornia by counties per year
cmdwp = pd.merge(cmd, pdc, left_on=["county10name", "year"], right_on=["County", "Year"], how="left")
# California bound refugees from Middle Eastern Muslim countries Data from 1998-2018 With Population data of calfornia by counties per year
cmemdwp = pd.merge(cmemd, pdc, left_on=["county10name", "year"], right_on=["County", "Year"], how="left")

print("Total Number of Refugees incoming into the US")
print(data.loc[data.year >= 1998].groupby("year").sum().refugees)

print("Total Number of Refugees from Muslim Countries incoming into the US")
print(cmd.groupby("year").sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby("year").sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by Country, 1998-2018")
print(cmd.groupby("citizenship_stable").sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby("citizenship_stable").sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by Country, Year by Year")
print(cmd.groupby(["year", "citizenship_stable"]).sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby(["year", "citizenship_stable"]).sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by California County they settled in, 1998-2018")
print(cmd.groupby("county10name").sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby("county10name").sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by California County they settled in, Year by Year")
print(cmd.groupby(["year", "county10name"]).sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby(["year", "county10name"]).sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by California County they settled in and Original Country, 1998-2018")
print(cmd.groupby(["county10name", "citizenship_stable"]).sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby(["county10name", "citizenship_stable"]).sum().refugees)

print("Total Number of Refugees from Muslim Countries, sorted by California County they settled in and Original Country, Year by Year")
print(cmd.groupby(["year", "county10name", "citizenship_stable"]).sum().refugees)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemd.groupby(["year", "county10name", "citizenship_stable"]).sum().refugees)

print("Total Refugees from Muslim Countries as a percentage of the population of each California County they settled in, 1998-2018")
print(cmdwp.groupby(["county10name"]).sum().refugees / cmdwp.groupby(["county10name"]).max().Population * 100)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemdwp.groupby(["county10name"]).sum().refugees / cmemdwp.groupby(["county10name"]).max().Population * 100)

print("Total Refugees from Muslim Countries as a percentage of the population of each California County they settled in, Year by Year")
print(cmdwp.groupby(["county10name", "year"]).sum().refugees / cmdwp.groupby(["county10name", "year"]).sum().Population * 100)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemdwp.groupby(["county10name", "year"]).sum().refugees / cmemdwp.groupby(["county10name", "year"]).sum().Population * 100)

print("Total Refugees from Muslim Countries as a percentage of the California population in counties that accepted refugees, Year by Year")
print(cmdwp.groupby(["year"]).sum().refugees / cmdwp.groupby(["year"]).sum().Population * 100)
print("Same, but only Middle Eastern Muslim Countries")
print(cmemdwp.groupby(["year"]).sum().refugees / cmemdwp.groupby(["year"]).sum().Population * 100)