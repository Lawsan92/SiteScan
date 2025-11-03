from matplotlib import pyplot as plt
import datacommons
from datacommons_client.client import DataCommonsClient

zip_code = '78735'

def API_fetch():

  api_key = "AIzaSyCTI4Xz-UW_G2Q2RfknhcfdAnTHq5X5XuI" # Replace with your API key
  client = DataCommonsClient(api_key=api_key)
  response = client.observation.fetch(
      variable_dcids=[
          "Count_Person"],
      date='',
      entity_dcids=[f'zip/{zip_code}']
  )

  response_body = response.byVariable['Count_Person'].byEntity['zip/78735'].orderedFacets[0].observations
  filtered_response_body = [item for item in response_body if 2013 <= int(item.date)]
  return filtered_response_body

def draw_line_graph(response):
  # X-data points (= years), Y-data points (= population)
  year_list, population_list = [], []
  for index, item in enumerate(response):

    year_list.append(int(item.date))
    population_list.append(float(item.value))

  # draw the line graph
  plt.plot(year_list, population_list)

def draw_table(response):
  # Column labels
  col_labels = ['Year', 'Population']

  # Data for the table
  table_data = []

  for index, item in enumerate(response):
    year = int(item.date)
    population = int(item.value)
    table_data.append([year, population])


  # Create a figure and axes
  fig, ax = plt.subplots(figsize=(6, 3))

  # Hide the axes to display only the table
  ax.axis('off')
  ax.axis('tight') # Adjust limits to fit the table

  # Create the table
  table = ax.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
  # Show the plot
  plt.show()
  return

# main logic
response = API_fetch()
print(response)
draw_line_graph(response)
draw_table(response)
