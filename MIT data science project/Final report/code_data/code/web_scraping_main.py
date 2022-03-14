from web_scraping_methods import find_index, scrape_info, html_clean
import pandas as pd
import re


def content_clean(article):
    atc_lst, count = [], -1
    for line in article:
        if "<div style=\"font-weight: bold\">" in line:
            count += 1
            atc_lst.append([])
            line = line.split(">")[1].split("<")[0]
            atc_lst[count].append(line)

        # Patent where there's a patent no
        elif "href=\"http://www" in line:
            line = line.split(">")[2].split("<")[0]
            atc_lst[count].append(line)

        else:
            line = line.split(">")[1].split("<")[0]
            atc_lst[count].append(line)
    return atc_lst


# Generate Info for 1 Faculty
def faculty_detail(result_lines):
    idx = [find_index(result_lines, "Articles<span class="),
           find_index(result_lines, "Conference Proceedings<span class="),
           find_index(result_lines, "Grants<span class="),
           find_index(result_lines, "Patents<span class="),
           find_index(result_lines, "Courses<span class=")]

    a, c, g, p = [], [], [], []
    for i in range(4):
        if idx[i] == -1:
            continue
        elif idx[i + 1] == -1:  # When there's no end boundary for this chunk
            # find end index
            end_idx1 = find_index(result_lines[idx[i]:], "personDetailSection panel-group") + idx[i] + 3
            end_idx2 = find_index(result_lines[idx[i]:], "<div id=\"detailsContent\"") + idx[i] + 3
            end_idx = min(end_idx1, end_idx2)

        else:
            end_idx = idx[i + 1]

        comp = result_lines[idx[i] + 3:end_idx - 3]
        # print(comp)
        if i == 0:
            print("Article")
            a = content_clean(comp)
            for j in a:
                j[-3] = get_year(j[-3])
                j[-1] = j[-1].replace("Citation Count: ", "")

        elif i == 1:
            print("Conference Proceeding")
            c = content_clean(comp)
            for j in c:
                j[-3] = get_year(j[-3])
                j[-1] = j[-1].replace("Citation Count: ", "")

        elif i == 2:
            print("Grants")
            g = content_clean(comp)
            for j in g:
                temp = split_year(j[-1])
                j[-1] = temp[0]
                j.append(temp[1])

        else:
            print("Patents")
            p = content_clean(comp)
            for j in p:
                temp = split_year(j[-1])
                j[-1] = temp[0]
                j.append(temp[1])
    return a, c, g, p


# Generate df for 1 Faculty
def generate_detail_df(a, c, g, p):
    a_df = pd.DataFrame(a, columns=['ArticleTitle', 'ArticleSubtitle', 'ArticleYear', 'ArticleNo', 'ArticleCiteCount'])
    c_df = pd.DataFrame(c, columns=['ConfTitle', 'ConfSubtitle', 'ConfYear', 'ConfNo', 'ConfCiteCount'])
    g_df = pd.DataFrame(g, columns=['GrantTitle', 'GrantSubtitle', 'GrantStartDate', 'GrantEndDate'])
    p_df = pd.DataFrame(p, columns=['PatentTitle', 'PatentNo', 'PatentStartDate', 'PatentEndDate'])

    g_df[['GrantYear']] = g_df.GrantStartDate
    # # if g_df.GrantStartDate.item() != "No Issue Date":
    g_df.GrantYear = g_df.GrantStartDate.apply(
        lambda x: x if len(x.split("/")) == 1 else ("20" + x.split("/")[2] if int(x.split("/")[2]) < 22 else "19" + x.split("/")[2]))



    # Patent Year
    p_df[['PatentYear']] = p_df.PatentStartDate
    # if p_df.GrantStartDate != "No Issue Date":
    p_df.PatentYear = p_df.PatentStartDate.apply(
        # lambda x: "20" + x.split("/")[2] if int(x.split("/")[2]) < 22 else ("19" + x.split("/")[2] if int(x.split("/")[2]) >= 22 else x))
        lambda x: x if len(x.split("/")) == 1 else (
            "20" + x.split("/")[2] if int(x.split("/")[2]) < 22 else "19" + x.split("/")[2]))

    return a_df, c_df, g_df, p_df


# Generate Count by Year df
def generate_count_df(a, c, g, p):
    a_count = a.groupby(by=['ArticleYear']).count().reset_index()[['ArticleYear', 'ArticleNo']].rename(columns={'ArticleYear': 'Year'})
    c_count = c.groupby(by=['ConfYear']).count().reset_index()[['ConfYear', 'ConfNo']].rename(columns={'ConfYear': 'Year'})
    g_count = g.groupby(by=['GrantYear']).count().reset_index()[['GrantYear', 'GrantTitle']].rename(columns={'GrantYear': 'Year'})
    p_count = p.groupby(by=['PatentYear']).count().reset_index()[['PatentYear', 'PatentNo']].rename(columns={'PatentYear': 'Year'})

    ac_count = pd.merge(a_count, c_count, on='Year', how='outer')
    # print(ac_count)
    # print("--------")
    gp_count = pd.merge(g_count, p_count, on='Year', how='outer')
    # print(gp_count)
    # print("--------")
    all_count = pd.merge(ac_count, gp_count, on='Year', how='outer')
    # print(all_count)
    # print("--------")
    all_count = all_count.fillna(0).sort_values(by='Year')
    # print(all_count)
    # print("--------")
    return all_count

# Helper Functions
def get_year(string):
    return string.split("(")[1].split(")")[0]


def split_year(string):
    if string != "No Issue Date":
        return string[:8], string[11:]
    else:
        return "No Issue Date", "No Expiration"


def main():
    col = ['Name', 'Department', 'Year', 'ArticleCount', 'ConfProcCount', 'GrantCount', 'PatentCount']
    rename = {'ArticleNo': 'ArticleCount', 'ConfNo':'ConfProcCount', 'GrantTitle': 'GrantCount', 'PatentNo': 'PatentCount'}
    df = pd.DataFrame(columns=col)
    data = pd.read_csv("./data/faculties_with_gender.csv")
    # data = data[data.Id == 1325]
    # print(data.Department)

    ids = data[['Id']]
    for person_id in ids['Id']:
    # id = [3530]
    # for person_id in id:
        print(person_id)
        raw = scrape_info(person_id)
        result_lines = html_clean(raw)
        # for l in result_lines:
        #     print(l)
        article_p, conf_p, grant_p, patent_p = faculty_detail(result_lines)
        article_df, conf_df, grant_df, patent_df = generate_detail_df(article_p, conf_p, grant_p, patent_p)
        count_df = generate_count_df(article_df, conf_df, grant_df, patent_df).rename(columns=rename)
        print("---")

        dept = data[data.Id == person_id].Department.to_string()
        dept = re.sub(r'[0-9]', '', dept)
        dept = dept.strip()
        count_df.insert(0, 'Department', dept)

        name = data[data.Id == person_id].Name.to_string()
        name = re.sub(r'[0-9]', '', name)
        name = name.strip()
        count_df.insert(0, 'Name', name)

        # In case a professor is in different department
        copy = count_df.copy()
        copy = copy.drop_duplicates(ignore_index=True)
        copy.Name = count_df.Name.apply(lambda x: x.splitlines())
        copy.Department = count_df.Department.apply(lambda x: x.splitlines())

        # print(copy)

        copy = copy.apply(pd.Series.explode)
        copy.Name = copy.Name.apply(lambda x: x.strip())
        copy.Department = copy.Department.apply(lambda x: x.strip())
        copy = copy.drop_duplicates()
        # copy = copy.explode('Department').drop_duplicates()


        # count_df = count_df.explode(column=['Name']).explode(column=['Department'])

        # df = df.append(count_df, ignore_index=True)
        df = df.append(copy, ignore_index=True)
    # print(df)
    df.to_csv("./data/faculty_count_by_year.csv", index=False)


if __name__ == "__main__":
    main()
