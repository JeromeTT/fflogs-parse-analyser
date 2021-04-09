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

def ranking_query(encounterid, job, page):
    query = """ {{
    worldData {{
    encounter (id: {}) {{
        characterRankings (specName: "{}", page: {})}}
    }}
    }}""".format(encounterid, job, page)
    return query

def time_query(reportcode, fightID):
    query = """
    {{
    reportData {{
        report(code: "{}") {{
        fights(fightIDs: {}) {{
            startTime
            endTime
        }}
        }}
    }}
    }}
    """.format(reportcode, fightID)
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

def make_query(tokenData, query, mainURL):
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
                writer.write('rank,name,rdps,rawdps,killtime,report,fightid,starttime,endtime\n')
                page = 1
                
                while True and (pages == -1 or page <= pages):
                    print('Retrieving Page ' + str(page) + ' for ' + job + ' for encounter ' + str(encounterid))
                    rawRankingJson = make_query(tokenData, ranking_query(encounterid, job, page), mainURL)
                    parseData = rawRankingJson['data']['worldData']['encounter']['characterRankings']['rankings']
                    hasMorePages = rawRankingJson['data']['worldData']['encounter']['characterRankings']['hasMorePages']
                    # iterate through the data
                    for index in range(len(parseData)):
                        parse = parseData[index]
                        # Getting the start time and end time of each individual parse
                        test = time_query(parse['report']['code'], parse['report']['fightID'])
                        rawTimeJson = make_query(tokenData, test, mainURL)
                        timeData = rawTimeJson['data']['reportData']['report']['fights'][0]
                        
                        writer.write('{},{},{},{},{},{},{},{},{}\n'.format(100 *(page-1) + index + 1, parse['name'], parse['amount'], parse['rawDPS'], parse['duration'], parse['report']['code'], parse['report']['fightID'], timeData['startTime'],timeData['endTime']))
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

def job_prompt(jobs):
    ''' Prompts the user for a list of jobs.
    '''
    print("\n-----------------------------")
    print("Choose jobs (seperated by comma)")
    print("For example: Red Mage, Black Mage, Bard")
    print("Input 'All' for all jobs, or 'None' for no jobs")
    options = str(input("Choice: "))    
    if options == "None":
        return []
    elif options == "All":
        return jobs
    else:
        return [item for item in options.split(', ')]

def encounter_prompt(encounters):
    ''' Prompts the user for a list of encounterIDs.
    '''
    print("\n-----------------------------")
    print("Choose encounters (seperated by comma)")
    print("For example: 73, 75")
    print("Input 'All' for all encounters in Eden's Promise, or 'None' for no encounters.")
    options = str(input("Choice: "))    
    if options == "None":
        return []
    elif options == "All":
        return encounters
    else:
        return [int(item) for item in options.split(', ')]

def page_prompt():
    ''' Prompts the user for an integer (representing a page).
    '''
    print("\n-----------------------------")
    print("Choose the number of pages")
    print("Input 'All' for all pages")
    options = str(input("Choice: ")) 
    if options == "All":
        return -1
    else:
        return int(options)
test_query = """
{
reportData {
  report(code: "RPp1JCGMwnXNB2fY") {
    events(fightIDs: [27], endTime: 6000000000, sourceClass: "Bard", limit: 10000){
      data
    }
    }
  }
}
"""


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
            jobchoice = job_prompt(jobslst)
            encounterchoice = encounter_prompt(encounterlst)
            pagechoice = page_prompt()
            ranking_parser(encounterchoice, jobchoice, pagechoice)

        elif option == 3:

            # for a singular report
            '''
            response = make_query(tokenData, timequery, mainURL)
            starttime = response['data']['reportData']['report']['fights']['starttime']
            endtime = response['data']['reportData']['report']['fights']['starttime']
            for event in rawdata:
                print(event['timestamp'] if event['abilityGameID'] == 3559 else '')
            '''
        elif option == 10:
            # End the program.
            print('Goodbye.')
            break