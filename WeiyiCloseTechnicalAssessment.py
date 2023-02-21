import requests
import csv
from closeio_api import Client
import statistics
from requests.auth import HTTPBasicAuth

# Set the base URL so that we can re-use it for all REST API requests for the Close API
BASE_URL = 'https://api.close.com/api/v1'

# Read the API key from the file so that it doesn't need to be written in the code
# More secure
# Can easily change the key in the file if necessary
f = open('/Users/weiyiwang/Desktop/personal/Close/APIKey.txt','r')
APIKey = f.read()

auth= HTTPBasicAuth(APIKey,"")
headers = {'Accept': 'application/json'}

API = Client(APIKey)



# Create a list of leads, where we can store lead dictionary objects
leads=[]

with open('/Users/weiyiwang/Desktop/personal/Close/CloseAssessmentData.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

# The line will skip the first row of the csv file (Header row)
    next(csv_reader)

# Each csv row needs to be one lead, so I want to break down the file into rows. I can do that with a for loop, since csv_reader is an iterable object
# These are the columns for each row: Company,Contact Name,Contact Emails,Contact Phones,custom.Company Founded,custom.Company Revenue,Company US State
    
    for row in csv_reader:

        # Ignore blank values when the lead name doesn't exist
        # Add validation to ignore rows where the name field is blank

        if row[0] != "":

            # For each lead, there can be many contacts
            # For each row in the csv, generate a list of booleans to keep track of index of the pre-existing lead
            list_of_bool = [True for lead in leads if ('name',row[0]) in lead.items()]

            # Build the contact
            newContact = {}
            if row[1] != "":
                newContact["name"] = row[1]
            if row[2] != "":
                newContact["emails"] = [{"email":row[2]}]
            if row[3] != "":
                newContact["phones"] = [{"phone":row[3]}]
            
            if any(list_of_bool):

                # Then get the index of the lead with the same name, and append the contact information to the contact list for that entry in the leads list
                matchingIndex=0
                for index in range(len(leads)):
                    if leads[index]['name']==row[0]:
                        matchingIndex = index

                # Append the new contact to the existing list of contacts
                leads[matchingIndex]["contacts"] += [
                    newContact
                ]
            # Else create a new lead entirely, and append it to the list
            else:

                # Build the lead
                newLead = {}
                newLead["name"] = row[0]
                newLead["contacts"] = [newContact]
                if row[4] != "":
                    newLead["custom.Company Founded"] = row[4]
                if row[5] != "":
                    # Replace the commas to make converting to float easier
                    newLead["custom.Company Revenue"] = row[5].replace(",", "")
                if row[6] != "":
                    newLead["addresses"] = [{"state":row[6]}]

                
                leads.append(newLead)


# This attempts to use the pre-built wrapper

##for lead in leads:
##    API.post('lead', data=lead)

# This one uses requests.post instead. Uncomment when you actually need to run post requests

##for lead in leads:
##    print(lead)
##    requests.post(BASE_URL+"/lead/",json=lead, headers=headers, auth=auth)

# Prompt for a start date
startDate = input("Start Date (yyyy-mm-dd): ")


# Prompt for an end date
endDate = input("End Date (yyyy-mm-dd): ")

# Below is the json to filter by date
# Copied from the visual editor in Close UI
filterJson = {
    # Set pagination limit so all results returned on first page
    "_limit":100,
    "query": {
        "negate": False,
        "queries": [
            {
                "negate": False,
                "object_type": "lead",
                "type": "object_type"
            },
            {
                "negate": False,
                "queries": [
                    {
                        "negate": False,
                        "queries": [
                            {
                                "condition": {
                                    "before": {
                                        "type": "fixed_local_date",
                                        "value": endDate,
                                        "which": "end"
                                    },
                                    "on_or_after": {
                                        "type": "fixed_local_date",
                                        "value": startDate,
                                        "which": "start"
                                    },
                                    "type": "moment_range"
                                },
                                "field": {
                                    "custom_field_id": "cf_LenGlsxFHqFTuxJiE4Mjalqhj1dWdtg55PklLjkeRcN",
                                    "type": "custom_field"
                                },
                                "negate": False,
                                "type": "field_condition"
                            }
                        ],
                        "type": "and"
                    }
                ],
                "type": "and"
            }
        ],
        "type": "and"
    },
    "_fields":{
        "lead": ["id", "name","custom","addresses"]
    },
    "sort": []
}



# Make the request for data based on the filter defined above
filteredLeads = requests.post(BASE_URL+"/data/search/",json=filterJson, headers=headers, auth=auth).json()

##counter = 1
##for i in filteredLeads["data"]:
##    print(counter)
##    counter += 1
##    print(i)

states = []
# Iterate through the results. Find a list of states
for i in filteredLeads["data"]:

    # If there are no addresses for a particular lead
    # append an empty string if there is no empty string
    i["addresses"].append({"state":"None"})
    
    # Append the state as the first item of a list
    if [i["addresses"][0]["state"]] not in states:
        states.append([i["addresses"][0]["state"]])

##print(states)

# Iterate through the list of states and get the count of the number of leads
for state in states:
    countLeads = 0
    #Iterate through the data returned from the filter request
    for i in filteredLeads["data"]:

        # If the lead has that state as the filter
        if i["addresses"][0]["state"] == state[0]:
            countLeads += 1
            
    state.append(countLeads)

# Iterate through the list of states and find the highest revenue lead
for state in states:
    highestRevenueLead = ""
    highestRevenue = 0
    #Iterate through the data returned from the filter request
    for i in filteredLeads["data"]:
        i.setdefault("custom.cf_Z2nC2Lb2D9yRpbvsF8sKAiI7zUtDpKrwQblTHNMAdkx","$0")
        revenue = float(i['custom.cf_Z2nC2Lb2D9yRpbvsF8sKAiI7zUtDpKrwQblTHNMAdkx'][1:])
        if revenue > highestRevenue and i["addresses"][0]["state"] == state[0]:
            highestRevenue = revenue
            highestRevenueLead = i["name"]

    state.append(highestRevenueLead)


# Iterate through the list of states and find the total revenue
for state in states:
    totalRevenue = 0
    #Iterate through the data returned from the filter request
    for i in filteredLeads["data"]:
        revenue = float(i['custom.cf_Z2nC2Lb2D9yRpbvsF8sKAiI7zUtDpKrwQblTHNMAdkx'][1:])
        if i["addresses"][0]["state"] == state[0]:
            totalRevenue+=revenue

    state.append(totalRevenue)

# Iterate through the list of states and find the median revenue
for state in states:

    # Gather a list of the revenues of the leads
    revenueList = []
    
    #Iterate through the data returned from the filter request
    for i in filteredLeads["data"]:
        if i["addresses"][0]["state"] == state[0]:
            revenueList.append(float(i['custom.cf_Z2nC2Lb2D9yRpbvsF8sKAiI7zUtDpKrwQblTHNMAdkx'][1:]))

    state.append(statistics.median(revenueList))

# Now that the states have been generated, append the header row to the beginning of the list
states.insert(0,["US State", "Total Number of Leads", "Highest Revenue Lead", "Total Revenue", "Median Revenue"])

filename = "/Users/weiyiwang/Desktop/personal/Close/CloseAssessmentOutput.csv"
with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
    csvwriter = csv.writer(csvfile) 
        
        
    # writing the data rows 
    csvwriter.writerows(states)
    

