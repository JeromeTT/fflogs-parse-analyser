from oauth import *
from datetime import datetime
import os
tokenloc = 'tokendata.txt'
credentialsloc = 'credentials.txt'
outputloc = 'output.txt'

mainURL = 'https://www.fflogs.com/api/v2/client'
authURL = 'https://www.fflogs.com/oauth/authorize'
tokenURL = 'https://www.fflogs.com/oauth/token'

jobslst = jobs = ['Paladin', 'Warrior', 'Dark Knight', 'Gunbreaker','White Mage','Scholar','Astrologian', 'Monk', 'Dragoon', 'Ninja', 'Samurai', 'Bard', 'Machinist', 'Dancer', 'Black Mage', 'Summoner', 'Red Mage']
encounterlst = [73,74,75,76,77]
clientID = ''
clientSecret = ''
tokenData = ''
query = ''

def query_creator(encounterid, job, page):
    query = """ {{
    worldData {{
    encounter (id: {}) {{
        characterRankings (specName: "{}", page: {})}}
    }}
    }}""".format(encounterid, job, page)
    return query

def saveJson(loc, data):
    ''' Saves JSON to a textfile.
    '''
    with open(loc, 'w') as writer:
        writer.write(json.dumps(data))

def loadJson(loc):
    ''' Loads JSON from a textfile.
    '''
    with open(loc, 'r') as reader:
        output = json.loads(reader.read())
    return output

def new_token(clientID, clientSecret, tokenURL, loc):
    ''' Creates new token using credentials and saves it.
    '''
    tokenData = get_token(clientID, clientSecret, tokenURL)
    saveJson(loc, tokenData)

def make_query(tokenData, query, mainURL, outputloc):
    ''' Makes a query and stores in an output.
    '''
    TOKEN = tokenData["access_token"]
    response = make_request(TOKEN, query, mainURL)
    return response.json()

def reload(credentialsloc, tokenloc):
    ''' Reloads credentials from files.
    '''
    with open(credentialsloc, 'r') as reader:
        clientID, clientSecret = reader.read().split(',')
    tokenData = loadJson(tokenloc)
    return (clientID, clientSecret, tokenData)

def ranking_parser(encounterlst, classlst, pages):
    ''' Gets all the data for top parses
    '''
    foldername = 'outputs/' + datetime.now().strftime('%Y_%m_%d_%H%M%S')
    os.mkdir(foldername)
    for encounterid in encounterlst: 
        for job in classlst:
            with open(foldername +'/' + job + str(encounterid) + '.txt', 'w+') as writer:
                writer.write('rank,rdps,rawdps,killtime,report,fightid\n')
                page = 1
                
                while True and page <= pages:
                    print('Retrieving Page ' + str(page) + ' for ' + job + ' for encounter ' + str(encounterid))
                    query = query_creator(encounterid, job, page)
                    rawJson = make_query(tokenData, query, mainURL, outputloc)
                    parseData = rawJson['data']['worldData']['encounter']['characterRankings']['rankings']
                    hasMorePages = rawJson['data']['worldData']['encounter']['characterRankings']['hasMorePages']
                    # iterate through the data
                    for index in range(len(parseData)):
                        parse = parseData[index]
                        writer.write('{},{},{},{},{},{}\n'.format(100 *(page-1) + index + 1, parse['amount'], parse['rawDPS'], parse['duration'], parse['report']['code'], parse['report']['fightID']))
                    if hasMorePages:
                        page += 1
                    else:
                        break
    print("\nRetrieval complete, location: " + foldername)                      

def credentials_menu():
    ''' Menu for Option 1: Credentials.
        Return True if something was changed
        Return False if nothing was changed
    '''
    while True:
        print("\n-----------------------------")
        print("Manage Credentials")
        print("1. New token")
        print("10. Back")
        option = int(input("Option: "))
        if option == 1:
            new_token(clientID, clientSecret, tokenURL, 'tokendata.txt')
            return True
        elif option == 2:
            return True
        elif option == 3:
            return True
        elif option == 10:
            return False

if __name__ == "__main__":
    # Initialize the original stats
    clientID, clientSecret, tokenData = reload(credentialsloc, tokenloc)
    print("Some Weird Parsing Thing idek")
    while True:
        print("\n-----------------------------")
        print("1. Manage Credentials.")
        print("2. Get top rankings")
        print("3. Parse Output.")
        print("10. Quit")
        option = int(input("Option: "))

        if option == 1:
            if credentials_menu():
                clientID, clientSecret, tokenData = reload(credentialsloc, tokenloc)
                print("New data updated.")

        elif option == 2:

            # Choose jobs
            jobchoices = []
            print("\n-----------------------------")
            print("Choose jobs (seperated by comma)")
            print("For example: Red Mage, Black Mage, Bard")
            print("Input 'All' for all jobs, or 'None' for no jobs")
            options = str(input("Choice: "))    
            if options == "None":
                pass
            elif options == "All":
                jobchoices = jobslst
            else:
                jobchoices = [item for item in options.split(', ')]

            # Choose encounters
            encounterchoices = []
            print("\n-----------------------------")
            print("Choose encounters (seperated by comma)")
            print("For example: 73, 75")
            print("Input 'All' for all encounters in Eden's Promise, or 'None' for no encounters.")
            options = str(input("Choice: "))    
            if options == "None":
                pass
            elif options == "All":
                encounterchoices = encounterlst
            else:
                encounterchoices = [int(item) for item in options.split(', ')]

            # Specify number of pages
            print("\n-----------------------------")
            print("Choose the number of pages")
            options = int(input("Choice: ")) 
            pages = options
            
            ranking_parser(encounterchoices, jobchoices, pages)

        elif option == 3:
            pass
            
        elif option == 10:
            # End the program.
            print('Goodbye.')
            break