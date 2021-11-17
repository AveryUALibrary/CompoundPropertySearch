# Give the program a list of compounds and a list of properties you wish to find, and it will output a list of the given specifications
# needed for api calling
import requests
# allows for the program to wait between api calls
from time import sleep

# the url that is used for ever api call
BASE_URL = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/'
# list of possible properties to search
property_list = "MolecularFormula | MolecularWeight | CanonicalSMILES | IsomericSMILES | IUPACName | Title | XLogP | ExactMass | MonoisotopicMass | TPSA | Complexity | Charge | HeavyAtomCount "

#creation of global variables
inputValues = {}
propertyValues = []


# grabs the list of compounds
def user_input_loop():
    print("add what compound you wish to check. enter q once done")
    user_input = input("compound: ")
    while user_input != "q":
        grab = requests.get(BASE_URL+"compound/name/"+user_input+"/cids/txt").text.strip()
        inputValues[user_input] = grab
        sleep(.25)
        user_input = input("Compound: ")

# grabs the list of properties
def property_loop():
    print(property_list)
    print("add what property you wish to check. enter q once done")
    properties = ""
    user_input = input("property: ")
    if user_input != "q":
        propertyValues.append(user_input)
        properties = user_input
        user_input = input("property: ")
    while user_input != "q":
        propertyValues.append(user_input)
        properties = properties + "," + user_input
        user_input = input("property: ")
    return properties

# goes through each compound and generates its own property list using api calling and json parsing
def output_loop():
    output_json = ""
    formation = ""
    user_input_loop()
    print()
    property_output = property_loop()
    print()
    item_number = 0
    for name, cid in inputValues.items():
        request = requests.get(BASE_URL + "compound/cid/" + cid + "/property/" + property_output + "/json").json()
        data_list = request["PropertyTable"]["Properties"][0]
        print(name + " has an id number of " + cid)
        print("its following properties include:")
        for props in propertyValues:
            print("    * " + props + ": " + str(data_list[props]))
        print()
        item_number += 1
        sleep(1)




if __name__ == '__main__':
    output_loop()


