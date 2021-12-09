import json
import pandas as pd


def load_json():
    f = open('cubaparsel.json')
    data = json.load(f)
    f.close()
    return data


def main():
    data = load_json()
    df = pd.DataFrame()
    flag = False

    for i in data.keys():
        # print(i)
        for j in data[i].keys():
            data[i][j]['category'] = i
        # print(data)
        df1 = pd.DataFrame(data[i])
        df1 = df1.transpose()
        print(df1)
        # pd.concat(df, df1)
        if flag:
            df = df.append(df1, ignore_index=True)
        else:
            flag = True
            df = df1
    # df = df.transpose()
    df.to_csv("cubaparsel.csv", index=False)


if __name__ == "__main__":
    main()
