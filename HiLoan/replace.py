# 复制工程文件到文件夹内
import csv
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET


def read_csv_map_0_1(file_path):
    # 读取csv至字典
    csvFile = open(file_path, "r", encoding="UTF-8")
    reader = csv.reader(csvFile)

    # 建立空字典
    result = {}
    for item in reader:
        if len(item) > 1:
            result[item[0]] = item[1]

    csvFile.close()
    return result


def repalcebytext(address, ori_str, target_str):
    all_data = ''
    with open(address, 'r+', encoding="UTF-8") as f:
        for line in f.readlines():
            #    print(line)
            if line.find(ori_str) != -1:
                line = target_str
                # print("==name===" + ori_str + "====" + str(line.find(ori_str)))
            all_data += line
        f.close()

    with open(address, 'r+', encoding="UTF-8") as f:
        f.truncate()
        f.write(all_data)
        f.close()


# 替换某个文件
def replayFile(oldFile, newFile):
    os.remove(oldFile)
    shutil.copyfile(newFile, oldFile)


# 替换xml 键值
def replaceXmlValue(xmlPath, map):
    xml = ET.parse(xmlPath)
    r = xml.getroot()
    for ch in r:
        for k in map:

            if ch.attrib["name"] == k:
                print("====name==" + k)
                ch.text = map[k]
    xml.write(xmlPath, "utf-8")

res = "D:/android/project/hujin/cashLoan_mx/mx_relaseMajia/HiLoan/2018-10-26/"
ori = 'D:/android/project/hujin/cashLoan_mx/iLoan-cashloan_dev/'
# 替代xml文件
ori_xhdpi = ori + 'app/src/main/res/drawable-xhdpi/'
for xhpdi_name_ in os.listdir(res + 'res/'):
    os.remove(ori_xhdpi + xhpdi_name_)
    shutil.copyfile(
        res + 'res/' + xhpdi_name_,
        ori_xhdpi + xhpdi_name_)
# 替代color
color_value_address = res + "color.csv"
color_value_map = read_csv_map_0_1(color_value_address)

color_xml = ori + "app/src/main/res/values/colors.xml"
updateTree = ET.parse(color_xml)
root = updateTree.getroot()

for child in root:
    for key in color_value_map:
        if child.attrib['name'] == key:
            child.text = color_value_map[key]

updateTree.write(color_xml)
# 替代 apkType
apkType_adr = res + "apkType.txt"
apkType = ''
with open(apkType_adr, 'r+', encoding="GBK") as f:
    list = f.readlines()
    apkType = list[1]
    f.close()
apkType_java_address = ori + 'app/src/main/java/com/panshi/hujin2/iloan/Constant.java'
repalcebytext(apkType_java_address, 'public static final String apkType',
              'public static final String apkType = "' + apkType + '";\n')
#替换签名
appscreate = "appSecret.properties"
replayFile(ori + appscreate, res + appscreate)
# 替换string
stringRes = ori+'app/src/main/res/values/strings.xml'
color_value_address = res + "string.csv"
stringMap = read_csv_map_0_1(color_value_address)
for m in stringMap:
    print(m)
replaceXmlValue(stringRes, stringMap)
stringRes = ori+'app/src/main/res/values-es-rES/strings.xml'
replaceXmlValue(stringRes, stringMap)
stringRes = ori+'app/src/main/res/values-zh-rCN/strings.xml'
replaceXmlValue(stringRes, stringMap)
# # 签名打包
subprocess.call(
    'gradle -b ' + ori + 'build.gradle assembleRelease', shell=True)
