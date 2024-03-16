# Introduction: What is Shortcourse?

Shortcourse is an easy to use wrapper over common statistical libraries such as pandas, Matplotlib and SciPy. It was built with the purpose of being used under timed conditions in statistics writeup exams. Shortcourse accepts an excel file that acts as a simple table. Just named columns, containing values. Shortcourse imports that file into its own datastructure, allowing the data to be analysed. By providing sensible defaults and a lot of conditional logic, Shortcourse aims to be faster and more convenient to use than Excel for timed courseworks. 

Check out the example work that can be produced with it under `"exam/Are Wealthy Countries Healthier.pdf"`

# Features: What can it do? :

This is a non-exhaustive list of interesting user facing features.

## Core: Organizational features:
- Generate CSV representation of table
- "Clean" the table by removing all NaN values in a column
- Filter rows by a certain value in a column
- Sort rows by value in a column
- Create subsets of tables
- Read Excel files 

## Maths: Statistically useful features:
- Round values in specified columns
- Find mean, quartiles and IQR
- Remove outliers (using 1.5IQR method)
- Find equations of linear regression lines
- Find standard deviation
- Find PMCC (Product Moment Correlation Coefficient)
- Hypothesis testing with:
    - Innacurate interpolation method for easy marking by teachers
    - Accurate p-value method for correctness

## Plots: Features for plotting figures:
- Plot scatter graphs and box plots with sensible defaults
- Add a regression line with string equation
- Add labeled, color coded  outliers

# Usage:
The intended usecase for the Shortcourse library is to be used by python scripts, each of which is dedicated to a single section in the writeup. Under the `exam` folder you will see all the files specific to my coursework examination. The hypothesis files were used to generate all the graphs, plots, lists and figures in the `Are Wealthy Countries Healthier.pdf` coursework which was produced during the exam. 

# Implementation Q&A:

- Printing from functions?
At first glance, having the functions print their output directly may seem strange. This design choice is deliberate. It allows offloading as much code from the scripts, reducing repetition at the expense of customizability. Because Shortcourse has a narrow use case where all function outputs will be printed anyway, this is acceptable. 

- Why not use pandas Dataframe?
Because that is no fun! Implementing my own datastructure was interesting and I learned a lot about decorators. 

# Installation: 

Development was done on WSL with Anaconda.

# A bit of background

The Shortcourse statistics library was written and tested by myself over the course of 2 weeks in preparation for my IFP Maths coursework examination in February 2023. The exam consists of a single 2 hour session during which a digital writeup must be produced. The writeup must answer the question of "Are wealthy countries healthier?" by analyzing a dataset provided as an Excel file. Though not assesed, it is expected that students prepare for the session by writing a mock writeup with practice data and then tweak the writeup during the session to work with never before seen exam data. The exam tests the student's ability to use computer tools for statistical analysis tasks. Naturally, students are expected to use Excel for this task, though any program is allowed. 

Since day one I could not overlook the fact that in principle, a student could write a program that would automatically adjust the writeup content to suit any Excel file input, allowing them to complete the exam in mere minutes, and to higher quality than manually using Excel (hence the name: a short coursework -> Shortcourse!). That idea resulted in me sitting the exam 2 weeks later relying purely on Shortcourse. 

My hopes for a completing the exam in mere minutes did not materialize. Hypothesis 2 needed to be modified from American countries to European as the exam data had no American countries. Hypothesis 3 exceeded the maximum n value for pre-recorded PMCC critical values, meaning that I had to manually do one hypothesis test, and as a bonus include a precise hypothesis test that can be automatically done by Shortcourse, but cannot be easilly marked by teachers. Rectifying those two flaws as well as editing the writeup took around 1 hour, which was longer than expected. 1 hour is less than the 2 hours given for the task though, so the name "Shortcourse" is still deserved. 

My coursework produced with Shortcourse got the highest ever score in any IFP programme my school offered.


