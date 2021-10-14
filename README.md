# Data 608 NYC Tree Health Dash Application

This app is to help an arborist study the health of trees in NYC based upon borough, species, and stewardship.

## Assignment

In this module we’ll be looking at data from the New York City tree census:

https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh

This data is collected by volunteers across the city, and is meant to catalog information about every single tree in the city.

Build a dash app for a arborist studying the health of various tree species (as defined by the variable ‘spc_common’) across each borough (defined by the variable ‘borough’). This arborist would like to answer the following two questions for each species and in each borough:

    What proportion of trees are in good, fair, or poor health according to the ‘health’ variable ?
    Are stewards (steward activity measured by the ‘steward’ variable) having an impact on the health of trees?

Please see the accompanying notebook for an introduction and some notes on the Socrata API.

Deployment: Dash deployment is more complicated than deploying shiny apps, so deployment in this case is optional (and will result in extra credit). You can read instructions on deploying a dash app to heroku here: https://dash.plot.ly/deployment

## Getting Started

I initially worked through the components and styles. Working with `venv` was a hurdle that was overcome. I found Azure easier for deploying coupled with a handy student subscription more robust than working with Heroku. The tutorial below for deploying on Azure was incredibly helpful!

### Dependencies

* Python
* Dash
* Dask
* Plotly
* Datashader
* Venv
* Pip
* Mapbox
* Platform to host: Azure was used as a cloud platform service, but Heroku or others can be used.

### Installing

* [GitHub repository](https://github.com/logicalschema/data608-treehealth-dash-sslee)
* [Mapbox](https://www.mapbox.com/)
    * You will need an API key from Mapbox if you want to use the light map style. You can use the free styles listed at Plotly.

### Executing program

* [https://data608-treehealth-dash-sslee.azurewebsites.net/](https://data608-treehealth-dash-sslee.azurewebsites.net/)


## Authors

Sung Lee 
[@logicalschema](https://twitter.com/logicalschema)

## Version History
* 1.0
    * Edited README
* 0.5 to 0.9
    * Editing css
    * Editing favicon and text
    * Pushed to Azure and connected to Github
* 0.4
    * Connected widgets to update graphs by callback
* 0.3
    * Added Dash widgets 
* 0.2
    * Added bar graphs
    * Added Map and Datashader
* 0.1
    * Initial Release

## License

This project is licensed under the [mit] License - see the LICENSE.md file for details

## Acknowledgments

Code snippets and tutorials:
* [Deploy on Azure](https://resonance-analytics.com/blog/deploying-dash-apps-on-azure)
* [Deploy on Heroku](https://towardsdatascience.com/how-to-deploy-your-dash-app-with-heroku-a4ecd25a6205)
* [Handy for External js files on Dash](https://dash.plotly.com/external-resources)
* [Github for a Dash App with Components](https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-oil-gas-ternary)
* [Taxi Holoviews](https://github.com/plotly/dash-holoviews-taxi) 
* [Datashader](https://plotly.com/python/datashader/)

