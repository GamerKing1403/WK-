import requests
import requests_cache
import json
import pandas as pd


headers = None
df = None
CompRes = []
requests_cache.install_cache(cache_name='github_cache', backend='sqlite', expire_after=180)


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


def request():  # This function requests the wk server for info.
    for i in range(0, 10000, 1000):
        CompRes.append(json.loads(requests.get(url=f'https://api.wanikani.com/v2/subjects?page_after_id={i}',
                                               headers=headers).content.decode('utf-8')))
    return CompRes


def reqResponse(identity):
    global CompRes
    res = -1
    if identity < 1000:
        res = CompRes[0]['data'][identity - 1]
    elif identity < 2000:
        res = CompRes[1]['data'][identity - 1001]
    elif identity < 3000:
        res = CompRes[2]['data'][identity - 2001]
    elif identity < 4000:
        res = CompRes[3]['data'][identity - 3001]
    elif identity < 5000:
        res = CompRes[4]['data'][identity - 4001]
    elif identity < 6000:
        res = CompRes[5]['data'][identity - 5001]
    elif identity < 7000:
        res = CompRes[6]['data'][identity - 6001]
    elif identity < 8000:
        res = CompRes[7]['data'][identity - 7001]
    elif identity < 9000:
        res = CompRes[8]['data'][identity - 8001]
    elif identity < 10000:
        res = CompRes[9]['data'][identity - 9001]
    return res


def CalcHalf(identity, typ, lvl, comp, kanjilvl=None):
    # This Function is for Calculating the Half in which The vocab belongs.
    res = reqResponse(identity)

    if typ == 'vocabulary':  # If its a vocab it will go through the comp kanji's and re-run this function.
        for ids in comp:
            result = CalcHalf(ids, 'kanji', lvl, res['data']['component_subject_ids'], res['data']['level'])
            if result == 2:
                return 2

    elif typ == 'kanji':  # If its a kanji it will go through the specific radicals to check the level of each.
        if lvl == kanjilvl:
            for ids in comp:
                if lvl == res['data']['level']:
                    return 2
                else:
                    return 1
    return 0


if __name__ == '__main__':  # Main loop which loops through the complete response and gets the required things in df.
    Initialization()
    request()
    for i in range(0, 10):  # Loop through different pages of The result.
        for j in range(1000):  # Loop through the 1000 data in a Specific Page
            try:
                # Getting all the required Data out of the JSON File.
                subject = CompRes[i]['data'][j]
                identity = subject['id']
                obj = subject['object']
                level = subject['data']['level']
                char = subject['data']['characters']
                if obj != 'radical':
                    components = subject['data']['component_subject_ids']
                else:
                    components = None

                #  This is the code for getting the Half in which the Kanji or Vocab will be.

                half = CalcHalf(identity, obj, level, components, level)

                #  Creating a Dict to append to the dataframe.
                compData = {'ID': identity, 'Object': obj, 'Level': level, 'Char': char, 'Components': components,
                            'Half': half}
                df = df.append(compData, ignore_index=True)

            except IndexError:
                ''' Since the last page doesn't have 1000 Items it will ignore the error which will be raise when trying 
                to use 999 in the last page. '''
                continue
        print('#'*(i+1) + '-'*(9-i))
    # df.to_excel('test.xlsx')  # Exports the data to an Excel File.
    print(df.tail())
