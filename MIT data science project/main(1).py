import pandas as pd
import requests


def scrape_info(person_id):
    cookies = {
        'ai_user': 'jan9H|2021-10-05T22:24:01.609Z',
        '__RequestVerificationToken': 'my4GQ72W-3zLFQUvjt3iTUnrYVRwEuegGRIT7Y0HvOrO9FbEgUkftCf-jQ7paKVXTkQo4i_q8e_lVsMBdOj82o4V4DRA1XA2sJZNYjRe_QI1',
        'ai_session': 'pf3B9|1635876991025|1635877595105.2',
    }

    headers = {
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Request-Id': '|tKYbI.8z+In',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        'Request-Context': 'appId=cid-v1:4dffb025-978a-4446-bff4-fe8bb67be793',
        'Origin': 'http://collaboration.mit.edu',
        # 'Referer': 'http://collaboration.mit.edu/search//person/1485',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
        'searchTerms': '',
        'collaboratorIds': '23990',
    }

    url = 'http://collaboration.mit.edu/Home/Productivity/' + str(person_id)

    r = requests.post(url, headers=headers, cookies=cookies,
                      data=data, verify=False)
    content = r.json()
    return content


# Find index
def find_index(passage, target):
    for i in range(len(passage)):
        if target in passage[i]:
            return i
    return -1


# Clean html text
def html_clean(result):
    result_lines = result.replace('\u2028', ' ').splitlines(True)
    # result_lines = result.splitlines("/div>\n")
    # print(result_lines)
    index = find_index(result_lines, 'Collaborators<span class=')
    # print("------")
    # print(index)
    print(result_lines[index])
    result_lines = list(filter(lambda x: x.strip() != "", result_lines[:index]))
    result_lines = list(filter(lambda x: len(x.replace("</div>", "").strip())!=0, result_lines))
    result_lines = list(filter(lambda x: len(x.replace("<div></div>", "").strip())!=0, result_lines))
    # result_lines = list(filter(lambda x: "=" in x or "-" in x or "No USPTO" in x, result_lines))
    return result_lines


# Get info of 1 person
def generate_df(result_lines):
    # for line in result_lines:

    name_idx = find_index(result_lines, "padding:1px;font-size:14pt")
    name = result_lines[name_idx].split(">")[1].split("<")[0]
    department = result_lines[name_idx + 1].split(">")[1].split("<")[0]
    lst = [name, department]

    idx = [find_index(result_lines, "Articles<span class="),
           find_index(result_lines, "Conference Proceedings<span class="),
           find_index(result_lines, "Grants<span class="), find_index(result_lines, "Patents<span class="),
           find_index(result_lines, "Courses<span class=")]

    for i in idx:
        if i != -1:
            lst.append(int(result_lines[i].split(">")[3].split("<")[0]))
        else:
            lst.append('NaN')

    df = pd.DataFrame([lst],
                      columns=['Name', 'Department', 'TotalArticleCount', 'TotalConfProcCount', 'TotalGrantCount',
                               'TotalPatentCount', 'TotalCourseCount'])

    return df


def main():
    df = pd.DataFrame(
        columns=['Name', 'Department', 'TotalArticleCount', 'TotalConfProcCount', 'TotalGrantCount', 'TotalPatentCount',
                 'TotalCourseCount'])
    ids = pd.read_csv("./data/professor_id.csv").head(5)[['Id']]

    for person_id in ids['Id']:
        person_df = generate_df(html_clean(scrape_info(person_id)))
        df = df.append(person_df)
    print(df.shape)
    print(df.head())

    # result = scrape_info(3255)
    # result = result


if __name__ == "__main__":
    main()
