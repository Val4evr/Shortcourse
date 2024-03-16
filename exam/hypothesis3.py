from Shortcourse import *
from paths import excelPath as excel_path
from paths import outputDirPath as outDir
csub = subdivisionFromExcel(excel_path, ["location"])
bed_gdp = subdivisionFromExcel(excel_path, ["hospital_beds_per_thousand", "gdp_per_capita", "location"])
line = "-" * 100

print(line)
print("CLEANING")
removed_indexes = bed_gdp.clean(["hospital_beds_per_thousand", "gdp_per_capita"])
print(f"Number of removed countries:{len(removed_indexes)}")
print("Removed:")
for i in removed_indexes:
    print(f"{csub.matrix[i][0]}", end=", ")
print()
print(line)
del csub

print("SCATTER")
columnNameY="hospital_beds_per_thousand"
columnNameX="gdp_per_capita"
title="Relationship between GDP/Capita and hospital beds per thousand"
yTitle="hospital beds / thousand"
xTitle="GDP per capita / $"
bed_gdp_scatter = plot_scatter(bed_gdp, columnNameX, columnNameY, title, xTitle, yTitle)
bed_gdp_scatter.plotMultiOutliers()
bed_gdp_scatter.print_outliers(columnName="location", parent=bed_gdp)
bed_gdp_scatter.addRegression()
bed_gdp_scatter.changesize()
bed_gdp_scatter.saveScatter(outDir+"/scatter_hypothesis3")
print(line)

print("HYPOTHESIS TEST")

print("Non-extrapolated hypothesis test:")
bed_gdp_scatter.hypothesis_test(columnNameX="gdp_per_capita", columnNameY="hospital_beds_per_thousand", test_type="positive", value_table=False)
print("Extrapolated hypothesis test done manually.")
print(line)

