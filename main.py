import requests
import json
import pandas as pd


headers = None
df = None


def Initialization():  # Initializes all the variables
    global headers, df
    Authorization()
    with open('Auth.txt', 'r') as apiFile:
        api = apiFile.readline()
    headers = {"Authorization": "Bearer " + api}
    df = pd.DataFrame({''})


def Authorization():  # This function checks if the file named auth.txt is there or not if not it adds the apikey to it.
    with open('Auth.txt', 'r+') as authFile:
        if authFile.readline() == '':
            api = input('Please Enter your WaniKani Api v2:- ')
            authFile.write(api)
        else:
            pass


def request(url):  # This function requests the wk server for info.
    return json.loads(requests.get(url=url, headers=headers).content.decode('utf-8'))


def CalcHalf(typ, lvl, comp, kanjilvl=None):  # This Function is for Calculating the Half in which The vocab belongs.
    if typ == 'vocabulary':  # If its a vocab it will go through the comp kanji's and re-run this function.
        for ids in comp:
            res = request(f'https://api.wanikani.com/v2/subjects/{ids}')
            result = CalcHalf('kanji', lvl, res['data']['component_subject_ids'], res['data']['level'])
            if result == 2:
                return 2

    elif typ == 'kanji':  # If its a kanji it will go through the specific radicals to check the level of each.
        if lvl == kanjilvl:
            for ids in comp:
                res = request(f'https://api.wanikani.com/v2/subjects/{ids}')
                if lvl == res['data']['level']:
                    return 2
                else:
                    return 1
    return 0


if __name__ == '__main__':  # Main loop which loops through the complete response and gets the required things in df.
    Initialization()
    for i in range(0, 10000, 1000):  # Loop through different pages of The result.

        response = request(f'https://api.wanikani.com/v2/subjects?page_after_id={i}')

        for j in range(1000):  # Loop through the 1000 data in a Specific Page

            try:

                # Getting all the required Data out of the JSON File.
                subject = response['data'][j]
                identity = subject['id']
                obj = subject['object']
                level = subject['data']['level']
                char = subject['data']['characters']
                if obj != 'radical':
                    components = subject['data']['component_subject_ids']
                else:
                    components = None

                #  This is the code for getting the Half in which the Kanji or Vocab will be.

                half = CalcHalf(obj, level, components, level)

                #  Creating a Dict to append to the dataframe.
                compData = {'ID': identity, 'Object': obj, 'Level': level, 'Char': char, 'Components': components,
                            'Half': half}
                df = df.append(compData, ignore_index=True)

            except IndexError:
                ''' Since the last page doesn't have 1000 Items it will ignore the error which will be raise when trying 
                to use 999 in the last page. '''
                continue

    df.to_excel('test.xlsx')  # Exports the data to an Excel File.
