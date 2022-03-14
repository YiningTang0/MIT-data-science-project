import requests
import pandas as pd

# Initialize df
df = pd.DataFrame(columns=['Id', 'Name', 'PersonId', 'LastName', 'FirstName', 'Department', 'RankName',
                           'TotalArticleCount', 'TotalConfProcCount', 'TotalGrantCount'])

# Prepare department ID
depart_ids = ['8926', '8928', '8929', '8930', '8931', '8932', '8933', '8937', '8942', '8944', '8945', '8946', '8950']


# Aeronautics and Astronautics - 8926
# Biological Engineering - 8928
# Biology - 8929
# Brain and Cognitive Sciences - 8930
# Chemical Engineering - 8931
# Chemistry - 8932
# Civil and Environmental Engineering - 8933
# Electrical Engineering and Computer Sciences - 8937
# Materials Science and Engineering - 8942
# Mechanical Engineering - 8944
# Media Arts and Sciences - 8945
# Nuclear Engineering - 8946
# Physics - 8950

# Web scraping
def scrape_id(depart_id):
    cookies = {
        'ai_user': 'jan9H|2021-10-05T22:24:01.609Z',
        '__RequestVerificationToken': 'my4GQ72W-3zLFQUvjt3iTUnrYVRwEuegGRIT7Y0HvOrO9FbEgUkftCf-jQ7paKVXTkQo4i_q8e_lVsMBdOj82o4V4DRA1XA2sJZNYjRe_QI1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Request-Id': '|tKYbI.ehxJz',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Request-Context': 'appId=cid-v1:4dffb025-978a-4446-bff4-fe8bb67be793',
        'Origin': 'http://collaboration.mit.edu',
        # 'Referer': 'http://collaboration.mit.edu/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'searchTerms': '',
        'searchTermTypeId': '2',
        'unitIdStrings': depart_id,
        'unitTypeId': '2',
        'workTypeIds': '',
        'workYearStart': '0',
        'workYearEnd': '0'
    }

    response = requests.post('http://collaboration.mit.edu/Home/SearchPersons', headers=headers, cookies=cookies,
                             data=data,
                             verify=False)

    response = pd.DataFrame.from_dict(response.json()["searchResults"]).drop(
        columns=['PersonId', 'TotalGrantDollars', 'TotalAwardCount',
                 'TotalCitationCount', 'TotalBookCount'])
    return response


for i in depart_ids:
    id_info = scrape_id(i)
    df = df.append(id_info)

print(df)
df.to_csv("professor_id.csv", index=False)
