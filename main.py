# Important! Please Make Sure You Have Installed the following libraries before running the code:
# Libraries: re, requests, json, pubchempy, smptlib, ssl

# import necessary libraries
import json
import requests

# Author: Jerry

# Global Variables used to store data into the json file
cid = 31236
compound_name = ' '
ghs_classification = ' '
health_hazards = ' '

# ghs_classification: returns the Globally Harmonized System (GHS) of Classification and Labelling of Chemicals
def get_ghs_classification(cid):
    api_endpoint = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/' + str(cid) + '/JSON'
    dat = {}
    headers = {'authorization': 'Bearer', 'Content-Type': 'application/json'}

    # sends a POST request
    response = requests.post(api_endpoint, headers=headers, json=dat)
    info = json.loads(response.content)

    # json_extract: returns an array that only contains the json that contains the key
    # Source: https://hackersandslackers.com/extract-data-from-complex-json-python/
    def json_extract(obj, key):

        arr = []

        def extract(obj, arr, key):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif v == key:
                        arr.append(obj)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        value = extract(obj, arr, key)
        return value

    # get the result using the key 'GHS Classification'
    result = json_extract(info, 'GHS Classification')
    # see if the chemical is not classified using the key 'Not Classified'
    result_not_classified = json_extract(result, 'Not Classified')

    # update the compoundName to the global variable compoundName
    global compound_name
    compound_name = info['Record']['RecordTitle']

    response_title = "GHS Classification: "

    if len(result_not_classified) != 0:
        # if its key is Not Classified
        if result_not_classified[0]['String'] == 'Not Classified':
            response_api = "The ghs classification is NOT CLASSIFIED so that it may not be dangerous, " \
                           "please look for other professional resources "
            response_ghs_classification = response_title + response_api
            # return the classification
            return response_ghs_classification
        # if it has a GHS classification
    else:
        # get the info using the key 'Pictogram(s)'
        results = json_extract(info, 'Pictogram(s)')
        ghs_classification = {}
        # use a for loop to get the value of the classification
        for key, value in results[0].items():
            if value not in ghs_classification.values():
                ghs_classification[key] = value

        ghs_response = ""
        # amount of classification
        number_classified = len(ghs_classification['Value']['StringWithMarkup'][0]['Markup'])

        ghs_class = ghs_classification['Value']['StringWithMarkup'][0]['Markup']

        for ghs in range(number_classified):
            # get the response for ghs classification
            response = ghs_class[ghs]['Extra'] + " "
            ghs_response += response
        response_ghs_classification = response_title + ghs_response
        # return the response ghs classification
        return response_ghs_classification


# health_hazards: returns the health hazards of a given chemical compound id
def get_health_hazards(cid):
    api_endpoint = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/' + str(cid) + '/JSON'
    dat = {}
    headers = {'authorization': 'Bearer', 'Content-Type': 'application/json'}
    # sends a POST request
    response = requests.post(api_endpoint, headers=headers, json=dat)
    health_info = json.loads(response.content)

    # json_extract: returns an array that only contains the json that contains the key
    # Source: https://hackersandslackers.com/extract-data-from-complex-json-python/
    def json_extract(obj, key):

        arr = []

        def extract(obj, arr, key):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif v == key:
                        arr.append(obj)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        values = extract(obj, arr, key)
        return values

    result = json_extract(health_info, 'Health Hazards')
    # result_not_classified = json_extract(result, 'Not Classified')

    # response_title = 'Health Hazard Summary:\n'

    if len(result) == 0:
        # check if the result is not classified
        # if len(result_not_classified) >= 1:
        response_message = "There are no records of health hazard information so that it may not be dangerous, " \
                           "please look at other professional resources "
        return response_message
    else:
        # get the health hazard information
        hazards = {}
        for key, value in result[0].items():
            if value not in hazards.values():
                hazards[key] = value

        result_health_hazard = hazards['Information'][0]['Value']['StringWithMarkup'][0]['String']

        return result_health_hazard


# get the compound name, GHS classification and healthHazard updated
get_ghs_classification(cid)
ghs_classification = get_ghs_classification(cid)
health_hazards = get_health_hazards(cid)

# debug
print(cid)
print(compound_name)
print(ghs_classification)
print(health_hazards)

# store the data in a dictionary and write it into a json file
data = {compound_name: []}
data[compound_name].append({
    'cid': cid,
    'ghs_classification': ghs_classification,
    'health_hazard': health_hazards
})
json_object = json.dumps(data, indent=4)
with open('data.json', 'a') as outfile:
    outfile.write(json_object)
