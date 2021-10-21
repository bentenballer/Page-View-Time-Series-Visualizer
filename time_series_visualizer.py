import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)
# Clean data
df = df[(df["value"]>=df["value"].quantile(0.025)) & (df["value"]<=df["value"].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    g = df.plot(xlabel="Date", ylabel="Page Views", title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019", legend=False)
    fig = g.figure

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.reset_index()
    df_bar["month_year"] = df_bar["date"].dt.to_period("M")
    df_bar = df_bar.drop(columns="date")

    df_bar = df_bar.groupby(by=["month_year"]).mean()
    df_bar = df_bar.reset_index()
    df_bar["year"] = df_bar["month_year"].dt.year
    df_bar["Months"] = df_bar["month_year"].dt.strftime("%B")
    df_bar = df_bar.drop(columns="month_year")

    # Draw bar plot
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    g = df_bar.pivot(index="year", columns="Months", values="value")
    g = g.reindex(months, axis=1)
    g = g.plot(kind="bar", xlabel="Years", ylabel="Average Page Views")
    fig = g.figure

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1,2,figsize=(15,5))
    sns.boxplot(ax=axes[0], x=df_box["year"], y=df_box["value"])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_ylabel("Page Views")
    axes[0].set_xlabel("Year")

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_box.index = pd.CategoricalIndex(df_box["month"], categories=months, ordered=True)
    df_box = df_box.sort_index()
    sns.boxplot(ax=axes[1], x=df_box["month"], y=df_box["value"])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_ylabel("Page Views")
    axes[1].set_xlabel("Month")
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
