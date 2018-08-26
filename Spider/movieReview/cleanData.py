import re

def cleanData(HTMLDic):
    # for key in HTMLDic.keys():
    print(type(HTMLDic[str(6)]))   # 内容
    content = HTMLDic[str(6)]
    for i in range(len(content)):
        content[i] = re.sub(r'\*|\'|\ |\\|\/', "", str(content[i]))
    print(content)
    '''
    jasdfj
    '''


def getHTMLDic():
    tempFile = "./cleanData.txt"
    with open(tempFile, "r", encoding = "utf-8") as f:
        tempStr = f.read()
    tempDic = eval(tempStr)     # str to dic
    return tempDic


def main():
    HTMLDic = getHTMLDic()
    cleanData(HTMLDic)

main()

