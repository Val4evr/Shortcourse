from Shortcourse import *
from paths import excelPath as excel_path
from paths import outputDirPath as outDir
csub = subdivisionFromExcel(excel_path, ["location"])
covid_gdp = subdivisionFromExcel(excel_path, ["total_covid_deaths_per_million 2020", "gdp_per_capita", "continent", "location"])
covid_gdp.editColumnName(oldName="total_covid_deaths_per_million 2020", newName="covid")
line = "-" * 100




print(line)
print("CLEANING")
removed_indexes = covid_gdp.clean(["covid", "gdp_per_capita"])
print(f"Number of removed countries:{len(removed_indexes)}")
print("Removed:")
for i in removed_indexes:
    print(f"{csub.matrix[i][0]}", end=", ")
print(line)
del csub

print(line)
print("FILTER SUBDIVISIONS Asia & Europe")
asia_covid_gdp = covid_gdp.clone()
europe_covid_gdp = covid_gdp.clone()
asia_covid_gdp.filterByEntry(columnName="continent", value="Asia")
europe_covid_gdp.filterByEntry(columnName="continent", value="Europe")
asia_countries = asia_covid_gdp.getColumn("location")
europe_countries = europe_covid_gdp.getColumn("location")

print("Asian:")
print(len(asia_countries))
print("European:")
print(len(europe_countries))


print(line)

print("BOXPLOT COVID DEATHS")
asia_covid = [i[0] for i in asia_covid_gdp.matrix]
europe_covid = [i[0] for i in europe_covid_gdp.matrix]
europe_covid.pop()
europe_covid.pop()
europe_covid.pop()
names = ["europe_covid", "asia_covid"]
newmatrix = matrixFromColumns([europe_covid, asia_covid])
europe_asia = Subdivision(newmatrix, names)
title='Covid deaths per million in Asian and European countries'
one_title = "Europe"
two_title = "Asia"
box = plot_dual_box(subdivision=europe_asia, title=title, one_title=one_title, two_title=two_title)
box.fig.tight_layout()
box.save_box(outDir+"/boxplot_hypothesis2")
median_asia = europe_asia.quartileValue(columnName="europe_covid", q=2)
q1_asia = europe_asia.quartileValue(columnName="asia_covid", q=1)
q3_asia = europe_asia.quartileValue(columnName="asia_covid", q=3)
median_europe = europe_asia.quartileValue(columnName="europe_covid", q=2)
q1_europe = europe_asia.quartileValue(columnName="europe_covid", q=1)
q3_europe = europe_asia.quartileValue(columnName="europe_covid", q=3)
print()
print(f"Asia Q1: {q1_asia}")
print(f"Asia Q2: {median_asia}")
print(f"Asia Q3: {q3_asia}")
print()
print(f"EU Q1: {q1_europe}")
print(f"EU Q2: {median_europe}")
print(f"EU Q3: {q3_europe}")
print()
print(f"IQR Asia: {q3_asia - q1_asia}")
print(f"IQR EU: {q3_europe - q1_europe}")
print(line)


print("SCATTER COVID DEATHS")
columnNameY="covid"
columnNameX="gdp_per_capita"
title='Relationship between GDP/Capita and covid deaths per million for Asian countries'
yTitle="Covid deaths per million"
xTitle="GDP per capita / $"
asia_scatter = plot_scatter(asia_covid_gdp, columnNameX, columnNameY, title, xTitle, yTitle)
asia_scatter.addRegression()
asia_scatter.changesize()
asia_scatter.saveScatter(outpath=outDir+"/scatter_hypothesis2_asia")

columnNameY="covid"
columnNameX="gdp_per_capita"
title='Relationship between GDP/Capita and covid deaths per million for European countries'
yTitle="Covid deaths per million"
xTitle="GDP per capita / $"
europe_scatter = plot_scatter(europe_covid_gdp, columnNameX, columnNameY, title, xTitle, yTitle)
europe_scatter.addRegression()
europe_scatter.changesize()
europe_scatter.saveScatter(outDir+"/scatter_hypothesis2_europe")

print(f"PMCC for Asia: {asia_scatter.pmcc(columnNameX=columnNameX, columnNameY=columnNameY)}")
print(f"PMCC for Europe: {europe_scatter.pmcc(columnNameX=columnNameX, columnNameY=columnNameY)}")
print(line)

print("HYPOTHESIS TESTING")

sig_level = 0.05
print("Asian hypothesis test:")
asia_scatter.hypothesis_test(columnNameX="gdp_per_capita", columnNameY="covid", test_type="negative", value_table=True)
print()
print("Europe test:")
europe_scatter.hypothesis_test(columnNameX="gdp_per_capita", columnNameY="covid", test_type="positive")