import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

def get_mean_median_mode(df, column_name, print_values=False, exclude_stats=[]):
    """ This function takes in a dataframe and a column name and prints the mean, median, and mode of the column. """
    mean = df[column_name].mean() if "mean" not in exclude_stats else None
    median = df[column_name].median() if "median" not in exclude_stats else None
    mode = df[column_name].mode()[0] if "mode" not in exclude_stats else None
    if print_values:
        print(f"Mean: {mean}")
        print(f"Median: {median}")
        print(f"Mode: {mode}")
    return {"mean": mean, "median": median, "mode": mode}

def get_variance_std(df, column_name, print_values=False):
    """ This function takes in a dataframe and a column name and prints the variance and standard deviation of the column. """
    variance = df[column_name].var()
    std = df[column_name].std()
    if print_values:
        print(f"Variance: {variance}")
        print(f"Standard Deviation: {std}")
    return {"variance": variance, "std": std}

def get_correlation(df, column_name_1, column_name_2, print_values=False):
    """ This function takes in a dataframe and two column names and prints the Pearson ’s Correlation (for numerical columns) between the two columns. """
    correlation = df[column_name_1].corr(df[column_name_2])
    if print_values:
        print(f"Correlation: {correlation}")
    return correlation

def get_chi_square(df, column_name_1, column_name_2, print_values=False):
    """ This function takes in a dataframe and two column names and prints the Chi-Square Test (for categorical columns) between the two columns. """
    observed = pd.crosstab(df[column_name_1], df[column_name_2])
    chi2, p, dof, expected = chi2_contingency(observed)
    if print_values:
        print(f"Chi-Square: {chi2}")
        print(f"p-value: {p}")
        print(f"Degrees of Freedom: {dof}")
        print(f"Expected: {expected}")
    return {"chi2": chi2, "p": p, "dof": dof, "expected": expected}

# Graph functions

def plot_histogram(df, column_name, bins=10):
    """ This function takes in a dataframe and a column name and plots a histogram of the column. """
    plt.hist(df[column_name], bins=bins)
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.title(f"Histogram of {column_name}")
    plt.show()


def plot_seaborn_histogram(df, column_name):
    """ This function takes in a dataframe and a column name and plots a histogram of the column using seaborn. """
    sns.histplot(df[column_name], kde=True)
    plt.xlabel(column_name)
    plt.ylabel("Frequency")
    plt.title(f"Histogram of {column_name}")
    plt.show()

def plot_boxplot(df, column_name):
    """ This function takes in a dataframe and a column name and plots a boxplot of the column. """
    sns.boxplot(x=df[column_name])
    plt.xlabel(column_name)
    plt.title(f"Boxplot of {column_name}")
    plt.show()

def plot_scatterplot(df, column_name_1, column_name_2):
    """ This function takes in a dataframe and two column names and plots a scatterplot of the two columns. """
    plt.scatter(df[column_name_1], df[column_name_2])
    plt.xlabel(column_name_1)
    plt.ylabel(column_name_2)
    plt.title(f"Scatterplot of {column_name_1} vs {column_name_2}")
    plt.show()

def plot_heatmap(df):
    """ This function takes in a dataframe and plots a heatmap of the correlation matrix. """
    fmt = '.2f'
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=fmt, center=0)
    plt.title("Heatmap of Correlation Matrix")
    plt.show()