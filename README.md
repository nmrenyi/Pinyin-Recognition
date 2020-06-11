# 拼音输入法 2018011423 任一
## 文件说明

1. Python3环境下，在src文件夹下运行pinyin.py即可进入拼音输入法，有多种运行方式。不加参数直接运行，即python3 pinyin.py即可进入手动输入模式，手动输入拼音可以看到对应的汉字结果。加入一个参数, python3 pinyin.py ../data/TestSet.txt 即可看到测试集上的逐字准确率和逐句准确率，注意这里的的TestSet.txt需要是拼音序列和汉字序列每个各一行的输入，具体格式与同学们一起建立的测试集格式相同。加入两个参数，即为实验要求中说的 python3 ../data/input.txt ../data/output.txt，输入为input.txt, 输出为output.txt，这里的input.txt为每个拼音输入序列各占一行，即为作业压缩包中提供的input.txt格式。

2. src文件夹下的pinyin_core_function.py是pinyin.py中用到的函数，为了pinyin.py的方便起见，将函数另存为一个文件。

3. data文件夹下，input.txt和TestSet.txt在前面介绍过。pinyin2word.txt为拼音到对应汉字的查询表。

4. src文件夹下，words_dict_small.npy为仅含新浪新闻语料的词频统计词典，words_dict_small_more.npy为含新浪新闻与近3个月的人民日报语料的词频词典，words_dict_small_more_jieba.npy为在新浪新闻和人民日报语料基础上增加jieba分词并将分词结果转换为一元和二元词的词频词典。这3个词典调用方式完全相同，在pinyin.py中可以替换使用。
