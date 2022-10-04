
#%%
import pandas as pd
import plotly.graph_objs as go

#%%
def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    #%%
    df_aardgas_csv = pd.read_csv("data/Aardgas.csv", sep=";",decimal=',',parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_aardgas = df_aardgas_csv.resample('D').max()
    df_aardgas.interpolate(inplace=True)
    df_aardgas.reset_index(level=0, inplace=True)
    df_aardgas["Year"]=pd.to_datetime(df_aardgas["Timestamp"]).dt.year 
    df_aardgas_year = df_aardgas.groupby("Year").max()
    df_aardgas_year["Gas Consumption"] = df_aardgas_year["Aardgas"] - df_aardgas_year["Aardgas"].shift()
    df_aardgas_year = df_aardgas_year.reset_index(level=0)

    #%%
    graph_one = []    
    graph_one.append(
      go.Bar(
      x = df_aardgas_year["Year"],
      y = df_aardgas_year["Gas Consumption"],
      )
    )

    layout_one = dict(title = 'Gas Consumption',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = 'Consumption m³'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    df_water_csv = pd.read_csv("data/Drinkwater.csv", sep=";",decimal=',', parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_water = df_water_csv.resample('D').max()
    df_water.interpolate(inplace=True)
    df_water.reset_index(level=0, inplace=True)

    df_water["Year"]=pd.to_datetime(df_aardgas["Timestamp"]).dt.year 
    df_water_year = df_water.groupby("Year").max()
    df_water_year["Water Consumption"] = df_water_year["Drinkwater"] - df_water_year["Drinkwater"].shift()
    df_water_year = df_water_year.reset_index(level=0)

    graph_two = []

    graph_two.append(
      go.Bar(
      x = df_water_year["Year"],
      y = df_water_year["Water Consumption"],
      )
    )

    layout_two = dict(title = 'Water Consumption',
                xaxis = dict(title = 'Year',),
                yaxis = dict(title = 'Water Consumption'),
                )

    #%%
    # third chart plots percent of population that is rural from 1990 to 2015
    df_aardgas_csv = pd.read_csv("data/Aardgas.csv", sep=";",decimal=',',parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_aardgas = df_aardgas_csv.resample('D').max()
    df_aardgas.interpolate(inplace=True)
    df_aardgas.reset_index(level=0, inplace=True)
    # df_aardgas = pd.read_csv("data/Aardgas.csv", sep=";",decimal=',', parse_dates=['Timestamp'],dayfirst=True)
    df_aardgas["M"]=pd.to_datetime(df_aardgas["Timestamp"]).astype('datetime64[M]')
    df_aardgas["Y"]=pd.to_datetime(df_aardgas["Timestamp"]).astype('datetime64[Y]')
    df_aardgas_month = df_aardgas[df_aardgas["Y"]>="2012"].groupby("M").max()
    df_aardgas_month["Gas Consumption"] = df_aardgas_month["Aardgas"] - df_aardgas_month["Aardgas"].shift()
    df_aardgas_month = df_aardgas_month.reset_index(level=0)
    df_aardgas_month["Month"] = df_aardgas_month["M"].dt.month
    df_aardgas_month.head(10)
    #%%

    graph_three = []
    graph_three.append(
      go.Box(
      x = df_aardgas_month["Month"],
      y = df_aardgas_month["Gas Consumption"],
      )
    )

    layout_three = dict(title = 'Gas Consumption',
                xaxis = dict(title = 'Month'),
                yaxis = dict(title = 'Consumption m³'),
                )
    
# fourth chart shows rural population vs arable land
    df_solar_csv = pd.read_csv("data/Solar.csv", sep=";",decimal=',',parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_solar = df_solar_csv.resample('D').max()
    df_solar.interpolate(inplace=True)
    df_solar.reset_index(level=0, inplace=True)
    
    df_solar["M"]=pd.to_datetime(df_solar["Timestamp"]).astype('datetime64[M]')
    df_solar["Y"]=pd.to_datetime(df_solar["Timestamp"]).astype('datetime64[Y]')
    df_solar_month = df_solar[df_solar["Y"]>="2012"].groupby("M").max()
    df_solar_month["Solar Energy"] = df_solar_month["Zonnepanelen"] - df_solar_month["Zonnepanelen"].shift()
    df_solar_month = df_solar_month.reset_index(level=0)
    df_solar_month["Month"] = df_solar_month["M"].dt.month

    graph_four = []
    
    graph_four.append(
      go.Box(
      x = df_solar_month["Month"],
      y = df_solar_month["Solar Energy"],
      )
    )

    layout_four = dict(title = 'Solar Energy',
                xaxis = dict(title = 'Month'),
                yaxis = dict(title = 'Solar Energy'),
                )

# fourth chart shows rural population vs arable land



    df_solar_csv = pd.read_csv("data/Solar.csv", sep=";",decimal=',',parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_solar = df_solar_csv.resample('D').max()
    df_solar.interpolate(inplace=True)
    df_solar.reset_index(level=0, inplace=True)

    df_solar["M"]=pd.to_datetime(df_solar["Timestamp"]).astype('datetime64[M]')
    df_solar["Y"]=pd.to_datetime(df_solar["Timestamp"]).astype('datetime64[Y]')
    df_solar_month = df_solar[df_solar["Y"]>="2012"].groupby("M").max()
    df_solar_month["Solar Energy"] = df_solar_month["Zonnepanelen"] - df_solar_month["Zonnepanelen"].shift()
    df_solar_month = df_solar_month.reset_index(level=0)
    df_solar_month["Month"] = df_solar_month["M"].dt.month

    df_elektriciteit_csv = pd.read_csv("data/Elektriciteit.csv", sep=";",decimal=',',parse_dates=['Timestamp'],dayfirst=True, index_col=0)
    df_elektriciteit = df_elektriciteit_csv.resample('D').max()
    df_elektriciteit.interpolate(inplace=True)
    df_elektriciteit.reset_index(level=0, inplace=True)

    df_elektriciteit["M"]=pd.to_datetime(df_elektriciteit["Timestamp"]).astype('datetime64[M]')
    df_elektriciteit["Y"]=pd.to_datetime(df_elektriciteit["Timestamp"]).astype('datetime64[Y]')
    df_elektriciteit_month = df_elektriciteit[df_elektriciteit["Y"]>="2012"].groupby("M").max()
    df_elektriciteit_month["Electricity Consumption"] = df_elektriciteit_month["Elektriciteit"] - df_elektriciteit_month["Elektriciteit"].shift()
    df_elektriciteit_month = df_elektriciteit_month.merge(df_solar_month, on="M")
    df_elektriciteit_month = df_elektriciteit_month.reset_index(level=0)
    df_elektriciteit_month["Electricity"] = df_elektriciteit_month["Electricity Consumption"] + df_solar_month["Solar Energy"]

    graph_five = []
    
    graph_five.append(
      go.Scatter(
      x = df_elektriciteit_month["M"],
      y = df_elektriciteit_month["Electricity"],
      mode = 'lines',
      name = 'Total'
      )
    )
    graph_five.append(
      go.Scatter(
      x = df_elektriciteit_month["M"],
      y = df_elektriciteit_month["Solar Energy"],
      mode = 'lines',
      name = 'Solar'
      )
    )
    graph_five.append(
      go.Scatter(
      x = df_elektriciteit_month["M"],
      y = df_elektriciteit_month["Electricity Consumption"],
      mode = 'lines',
      name = 'Electricity from GRID'
      )
    )
    graph_five.append(
      go.Bar(
      x = df_elektriciteit_month["M"],
      y = df_elektriciteit_month["Electricity Consumption"],
      name = 'Electricity from GRID'
      )
    )
        
    layout_five = dict(title = 'Electricity Consumption',
                xaxis = dict(title = 'Month'),
                yaxis = dict(title = 'Electricity Consumption'),
                )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    figures.append(dict(data=graph_five, layout=layout_five))

    return figures