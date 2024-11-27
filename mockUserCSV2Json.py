import os
import csv
import json

# 配置存放csv和json文件的目录
path = "/Users/bytedance/Downloads/mockUser"
# 配置value列是csv文件中的第几列，下标从0开始
valueIndex = 1


def mockUserSort(i):
    return i[1], int(i[0])


if __name__ == "__main__":
    didMap = {}
    csvList = []
    jsonList = []

    pathList = os.listdir(path)
    for filename in pathList:
        if os.path.splitext(filename)[1] == ".csv":
            csvList.append(filename)
        elif os.path.splitext(filename)[1] == ".json":
            jsonList.append(filename)

    for filename in csvList:
        with open(path + "/" + filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[valueIndex].lower() == "value":
                    continue
                if row[valueIndex] not in didMap:
                    didMap[row[valueIndex]] = True
            csvfile.close()

    for filename in jsonList:
        with open(path + "/" + filename, "r") as jsonFile:
            dataDict = json.load(jsonFile)
            for user in dataDict["did_list"]:
                if user["can_use"]:
                    if user["did"] not in didMap:
                        didMap[user["did"]] = True
                else:
                    didMap[user["did"]] = False
            jsonFile.close()

    itemsList = list(didMap.items())
    mockUserList = sorted(itemsList, key=mockUserSort)
    # print(mockUserList)

    dataDict = {
        "did_list": []
    }
    for user in mockUserList:
        did, canUse = user
        dataDict["did_list"].append({
            "did": did,
            "can_use": canUse
        })

    with open(path + "/" + "did_mock_user_multi.json", "w", encoding="utf-8") as outFile:
        json.dump(dataDict, outFile, indent=4, ensure_ascii=False)
        outFile.close()

    os.system("cat " + path + "/" + "did_mock_user_multi.json")
    print("\nTCC配置文件已输出至", path + "/" + "did_mock_user_multi.json", "\n按回车退出")
    input()
