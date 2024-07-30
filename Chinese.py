from pypinyin import lazy_pinyin
import pandas as pd
    #读入EXCEL文件
ex = pd.read_excel("name.xls")
result = ""
for i in range(ex.shape[0]):
    zh_word = (ex.iloc[i,0])
    test_list = lazy_pinyin(zh_word)
    #result = result + ''.join(test_list) + ' '#输出结果不换行
    result = result +''.join(test_list)+'\n'#输出结果换行
print(result)

