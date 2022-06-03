import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
from DictFunction import convertJSONtoDict
import datetime

###### SET SPRINT DAY & DATE EXTRACTED ######
### Increase by one the counter "SprintDate" stored in "/DayCounter.py"
def get_SprintDay_Counter(filename="/<Path>/DayCounter.py"):
    with open(filename, "a+") as f:
        f.seek(12, 0)
        val = int(f.read() or 0) + 1
        if val == 11:
         val = 1
        f.seek(12, 0)
        f.truncate()
        f.write(str(val))
        return val

### Set the Date and Sprint Day that the data was extracted
DateExtracted = datetime.date.today().strftime("%d/%b/%Y")
SprintDay = get_SprintDay_Counter()
# DateExtracted = '25/Apr/2022'


###### EXTRACT SPRINT DATA ######
### Download the Sprint data from the Jira API
startAt = 0
NewSprintDict = dict()

while True:
   url = "https://your-domain.atlassian.net/rest/api/3/jql/autocompletedata&startAt="+str(startAt)+"&maxResults=-1"

   auth = HTTPBasicAuth("email@example.com", "<api_token>")

   headers = {
      "Accept": "application/json"
   }

   response = requests.request(
      "GET",
      url,
      headers=headers,
      auth=auth
   )

   SlicedSprintData = json.loads(response.text)

   if SlicedSprintData["issues"]:
      pass
   else:
      break

   # Convert JSON into a Dictionary
   SlicedSprintDict = convertJSONtoDict(SlicedSprintData, NewSprintDict, DateExtracted, SprintDay)

   startAt += 100

### Transform the Sprint Data Dictionary into a Data Frame
NewSprintData = pd.DataFrame(NewSprintDict)


###### EXTRACT KANBAN DATA ######
### Download the Kanban data from the Jira API
startAt = 0
NewKanbanDict = dict()

while True:
   url = "https://your-domain.atlassian.net/rest/api/3/jql/autocompletedata&startAt="+str(startAt)+"&maxResults=-1"

   auth = HTTPBasicAuth("email@example.com", "<api_token>")

   headers = {
      "Accept": "application/json"
   }

   response = requests.request(
      "GET",
      url,
      headers=headers,
      auth=auth
   )

   SlicedKanbanData = json.loads(response.text)

   if SlicedKanbanData["issues"]:
      pass
   else:
      break

   # Convert JSON into a Dictionary
   SlicedKanbanDict = convertJSONtoDict(SlicedKanbanData, NewKanbanDict, DateExtracted, SprintDay)

   startAt += 100

### Transform Dictionary into a Data Frame
NewKanbanData = pd.DataFrame(NewKanbanDict)


###### INSERT NEW DATA INTO THE DATABASE ######
### Set path and files name of the Data Base
DataBasePath = "/<Path>"
DataBaseSprintDataName = "/<FileName>.csv"
DataBaseKanbanDataName = "/<FileName>.csv"

### Read Box full Jira data set
FullSprintData = pd.read_csv(DataBasePath + DataBaseSprintDataName, sep=";", index_col="Unnamed: 0")
FullKanbanData = pd.read_csv(DataBasePath + DataBaseKanbanDataName, sep=";", index_col="Unnamed: 0")

### Append new data
UpdatedSprintData = pd.concat([FullSprintData, NewSprintData], ignore_index=True, join="outer")
UpdatedKanbanData = pd.concat([FullKanbanData, NewKanbanData], ignore_index=True, join="outer")

### Save new full data sets
UpdatedSprintData.to_csv(DataBasePath + DataBaseSprintDataName, sep=";")
UpdatedKanbanData.to_csv(DataBasePath + DataBaseKanbanDataName, sep=";")