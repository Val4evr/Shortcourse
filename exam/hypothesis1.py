from Shortcourse import *
from paths import excelPath as excel_path
from paths import outputDirPath as outDir
csub = subdivisionFromExcel(excel_path, ["location"])
exp_GDP = subdivisionFromExcel(excel_path, ["location","life_expectancy", "gdp_per_capita"])
line = "-" * 100


print(line)
print("CLEANING")
removed_indexes = exp_GDP.clean(["life_expectancy", "gdp_per_capita"])
print(f"Number of removed countries:{len(removed_indexes)}")
print("Removed:")                 
for i in removed_indexes:
    print(f"{csub.matrix[i][0]}", end=", ")
print()
print(line)
del csub

print("MEDIAN GDP/CAPITA")
med = exp_GDP.quartileValue(columnName="gdp_per_capita", q=2)
print(f"median GDP/Capita: {med}")
print(line)

print("SUBDIVISION ABOVE / BELOW MEDIAN")
poor = []
rich = []
countries = subsetSubdivision(parent=exp_GDP, columnNames=["location"])
for entry in exp_GDP.matrix:
    if entry[2] < med:
        poor.append(entry)
    else:
        rich.append(entry)
print(f"There are {len(poor)} poor countries")
print(f"There are {len(rich)} rich countries")
print("The poor countries are:")
for i in poor:
    print(i[0], end=", ")
print()
print()
print("The rich countries are:")
for i in rich:
    print(i[0], end=", ")
print()
print(line)

print("BOXPLOTS RICH POOR")
poor_expectancy = [i[1] for i in poor]
rich_expectancy = [i[1] for i in rich]
names= ["poor_exp", "rich_exp"]
new_matrix= matrixFromColumns([poor_expectancy, rich_expectancy])
poor_rich = Subdivision(new_matrix, names)

title='Life Expectancy distribution in "Poor" and "Rich" countries'
one_title = "Country with GDP/Capita < Median"
two_title = "Country with GDP/Capita > Median"
box = plot_dual_box(poor_rich,title=title, one_title=one_title, two_title=two_title)
box.fig.tight_layout()
box.changesize(width=False, smaller=True)
median_poor = poor_rich.quartileValue(columnName="poor_exp", q=2)
q1_poor = poor_rich.quartileValue(columnName="poor_exp", q=1)
q3_poor = poor_rich.quartileValue(columnName="poor_exp", q=3)
median_rich = poor_rich.quartileValue(columnName="rich_exp", q=2)
q1_rich = poor_rich.quartileValue(columnName="rich_exp", q=1)
q3_rich = poor_rich.quartileValue(columnName="rich_exp", q=3)
# outliers = poor_rich.remove_outliers() Rerun to plot outliers on graphs. 
#print(f"self.outliers:{outliers}") #If returns something modify the prints below to include outliers
print()
print(f"Poor Q1: {q1_poor}")
print(f"Poor Q2: {median_poor}")
print(f"Poor Q3: {q3_poor}")
print()
print(f"Rich Q1: {q1_rich}")
print(f"Rich Q2: {median_rich}")
print(f"Rich Q3: {q3_rich}")
print()
print(f"IQR Poor: {q3_poor - q1_poor}")
print(f"IQR Rich: {q3_rich - q1_rich}")
box.save_box(outpath=outDir+"/boxplot_hypothesis1")
print(line)


print("SCATTER RICH POOR")
poor_columnNames = ["location", "life_expectancy", "gdp_per_capita"] 
exp_GDP_poor = Subdivision(poor, poor_columnNames)
exp_GDP_rich = Subdivision(rich, poor_columnNames) #poor_columNames same as rich

columnNameY="life_expectancy"
columnNameX="gdp_per_capita"
title='Relationship between GDP/Capita and life expectancy for "poor" countries'
yTitle="Expected lifespan / years"
xTitle="GDP per capita / $"
poor_scatter = plot_scatter(exp_GDP_poor, columnNameX, columnNameY, title, xTitle, yTitle)
poor_scatter.addRegression()
poor_scatter.saveScatter(outpath=outDir+"/scatter_hypothesis1_poor")

columnNameY="life_expectancy"
columnNameX="gdp_per_capita"
title='Relationship between GDP/Capita and life expectancy for "rich" countries'
yTitle="Expected lifespan / years"
xTitle="GDP per capita / $"
rich_scatter = plot_scatter(exp_GDP_rich, columnNameX, columnNameY, title, xTitle, yTitle)
rich_scatter.addRegression()
rich_scatter.saveScatter(outpath=outDir+"/scatter_hypothesis1_rich")
print(f"Rich PMCC:{rich_scatter.pmcc(columnNameX=columnNameX, columnNameY=columnNameY)}")
print(f"Poor PMCC:{poor_scatter.pmcc(columnNameX=columnNameX, columnNameY=columnNameY)}")
print(line)

print("HYPOTHESIS TESTING poor & rich")
print()

print("Poor test")
exp_GDP_poor.hypothesis_test(columnNameX="gdp_per_capita", columnNameY="life_expectancy", test_type="positive")
print()
print("Rich test")
exp_GDP_rich.hypothesis_test(columnNameX="gdp_per_capita", columnNameY="life_expectancy", test_type="positive")

print(line)