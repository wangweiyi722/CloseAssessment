# CloseAssessment

# Logic

1. Authentication
In order to make requests to my Close account, I need to use an API key to authenticate. I add this as part of any and every request made to the API. The API key is generated on the Close website, and allows users to make requests to Close to create, read, update and delete data on Close.

2. Import the leads
Provided a csv file with a list of leads and contacts information, I will be reading the csv file into my python program. This file will not immediately be in the format necessary to use with the API, so I will be re-arranging the data into a specific format (JSON) that will be accepted by the API.

I need to be careful that the leads each have a name, as it would be nonsense to import a lead without a name. There are several other fields that the close API needs a value for in order to import the lead properly. But some data may not have all of these fields. If those fields don't exist, I will exclude them from being sent to the API, so that the API will not throw an error.

Once the leads are in the proper format, I can use the Close API to add the leads to the list of leads on the website

3. Filter by the date
One requirement for this program is that it would search the list of imported leads, and retrieve leads with a founded date between a start date and end date. So I added a prompt for the user to be able to add his/her own start date and end date.

These dates are then added to a filter that tells the API to only retrieve leads that were founded between the start and end dates

4. Make a summary report
Now that I have a list of the leads that meet the criteria, I am going to create a list of the unique states that the leads are located in. This means that there will be no duplicates. I can then go through the list of leads and calculate all the fields that I need to do, adding them as additional information on the state as I go.

# Dependencies

1. API Key
In order to make a new API Key, register with your email address at https://app.close.com/signup for a 14-day free trial. While
on a free trial, you’ll have full access to all of the Close features, API included.
*If you’ve already registered and your trial has expired,send a message to support@close.com to
extend it.

Open the "APIKey.txt" file and replace the API key with the new API Key.

2. File paths
Adjust the paths to the CloseAssessmentData.csv and CloseAssesmentOutput.csv as appropriate.

3. Run "pip install closeio" in the terminal
