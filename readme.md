# Introduction: What is Shortcourse?

Shortcourse is an easy to use wrapper over common statistical libraries such as pandas, Matplotlib and SciPy. It was built with the purpose of being used under timed conditions in statistics writeup exams. 

It accepts an Excel file that contains a simple table. Shortcourse provides functionality to analyse that data. By providing sensible defaults and a lot of conditional logic, Shortcourse aims to be faster and more convenient to use than Excel for timed courseworks. 

Check out the example work that can be produced with it under `exam/'Are Wealthy Countries Healthier.pdf'`

# Features: What can it do? :

This is a non-exhaustive list of interesting user facing features.

**Core: Organizational features:**
- Generate CSV representation of table
- "Clean" the table by removing all NaN values in a column
- Filter rows by a certain value in a column
- Sort rows by value in a column
- Create subsets of tables
- Read Excel files 

**Maths: Statistically useful features:**
- Round values in specified columns
- Find mean, quartiles and IQR
- Remove outliers (using 1.5IQR method)
- Find equations of linear regression lines
- Find standard deviation
- Find PMCC (Product Moment Correlation Coefficient)
- Hypothesis testing with:
    - Innacurate interpolation method for easy marking by teachers
    - Accurate p-value method for correctness

**Plots: Features for plotting figures:**
- Plot scatter graphs and box plots with sensible defaults
- Add a regression line with string equation
- Add labeled, color coded  outliers

# Usage:
The intended usecase for the Shortcourse library is to be used by python scripts, each of which is dedicated to a single section in the writeup. Under the `exam` folder you will see all the files specific to my coursework examination. The hypothesis files were used to generate all the graphs, plots, lists and figures in the `Are Wealthy Countries Healthier.pdf` coursework which was produced during the exam. You will find the graphs and plots in `exam/output`.

# Implementation Q&A:

**Printing from functions?**

At first glance, having the functions print their output directly may seem strange. This design choice is deliberate. It allows offloading as much code from the scripts to the library, reducing repetition at the expense of customizability. Because Shortcourse has a narrow use case where all function outputs will be printed anyway, this is fine.

**Why not use pandas Dataframe?**

Because that is no fun! Implementing my own datastructure was interesting and I learned a lot about decorators. 

# Installation: 

Development was done on WSL with Anaconda, but it is not required.


1. **In your terminal, navigate to your directory of choice and clone this repo:**
```
cd Documents/Programming

git clone https://github.com/Val4evr/Shortcourse.git
```

2. **Change directory to Shortcourse, and create and activate a new virtual environment.**
```
cd Shortcourse
python -m venv shortcourse_env
```
On Windows run:
```
shortcourse_env\Scripts\activate 
```
On Linux/Unix/MacOS run:
```
source shortcourse_env/bin/activate
```

3. **Install Shortcourse with dependencies:**
```
pip install .
```

4. **Run an example script to check everything works:**
```
python exam/hypothesis1.py
```

You can now:
- Run more scripts (`hypothesis2.py` & `hypothesis3.py`)
- Check out the generated plots and graphs in `exam/output`

**If something does not work, please post an issue.**
