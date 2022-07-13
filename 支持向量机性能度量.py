import jieba
import datetime
# 向量\测试集\训练集\得分比对
from sklearn.model_selection  import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
# 支持向量机
from sklearn import svm

# 忽略警告
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="sklearn", lineno=196)

m_current_sklearn = "LinearSVC"
# 不适合的SVM算法：LinearSVR、NuSVC、NuSVR、OneClassSVM、SVR、l1_min_c
# 适合的SVM算法：LinearSVC、SVC
m_sklearn_list = ["LinearSVC","SVC"]

m_count = [1000,3000,5000,8000,10000,15000,20000]

# all
m_list_allText = []
m_list_allL4ID = []
# 内容的训练集、测试集
m_text_test = []
m_text_train = []
m_label_test = []
m_label_train = []

m_map_list = []
m_map_all = {}


# 读取文件里面数据,获取标签和内容
def getFile(filename, count):
    with open(filename, 'r' ,encoding='utf-8') as fp:
        global m_list_allL4ID,m_list_allText
        m_list_allL4ID = []
        m_list_allText = []
        for i in range(count):
            text = fp.readline()
            if ":" in text:
                L4ID = text.split(":")[-2]
                Msg = text.split(":")[-1]
                m_list_allL4ID.append(L4ID)
                m_list_allText.append(Msg)

# 随机分为 测试集 和 训练集 2-8分
def randomTestAndTrain():
    # 生成训练集和测试集
    global m_text_test, m_text_train, m_label_test, m_label_train
    m_text_train, m_text_test, m_label_train, m_label_test = train_test_split(m_list_allText, m_list_allL4ID, test_size=0.2, random_state=1)

def jiabaToVector(list, isTest, isTFIDF = False):
    tmp_list = []
    for sentence in list:
        tmp_list.append(" ".join(jieba.cut(sentence.strip())))
    # 利用TFIDF生成词向量
    transformer = TfidfTransformer()
    if isTest:
        if isTFIDF:
            tfidf = transformer.fit_transform(vectorizer.transform(tmp_list))
        else:
            tfidf = vectorizer.transform(tmp_list)
    else:
        if isTFIDF:
            tfidf = transformer.fit_transform(vectorizer.fit_transform(tmp_list))
        else:
            tfidf = vectorizer.fit_transform(tmp_list)
    return tfidf


# 创建默认参数的逻辑回归
def predict_4(X, Y):
    if m_current_sklearn == "LinearSVC":
        clf = svm.LinearSVC()
    elif m_current_sklearn == "SVC":
        clf = svm.SVC()
    clf = clf.fit(X, Y)
    return clf




def test(count):
    # getFile("./rg_test.train", count)
    getFile("./rg_train_20190102_20181227114134.train", count)
    # print("获取全部已知数据的label和text")

    # 随机分为 测试集 和 训练集 2-8分
    randomTestAndTrain()

    global vectorizer
    # 全局向量
    vectorizer = CountVectorizer()

    # 生成训练向量
    vector_train = jiabaToVector(m_text_train, False)
    # 生成训练向量-tfidf
    # vector_train = jiabaToVector(m_text_train, False, True)

    # 数据大小
    lenall = len(m_list_allText)
    print("总集大小:", lenall)

    # 训练
    startT_Train = datetime.datetime.now()
    clf = predict_4(vector_train, m_label_train)
    endT_Train = datetime.datetime.now()
    print("训练Time:", (endT_Train - startT_Train).microseconds)

    # 生成测试向量
    vector_test = jiabaToVector(m_text_test, True)
    # 生成测试向量-tfidf
    # vector_test = jiabaToVector(m_text_test, True, True)

    # 测试
    startT = datetime.datetime.now()
    result = clf.predict(vector_test)
    endT = datetime.datetime.now()
    print("测试Time:", (endT - startT).microseconds)

    # 计算百分比
    percent = accuracy_score(result, m_label_test)
    print("准确率:", round(percent, 3))

    map_all = {}
    map_all["精确率"]=round(percent, 3)
    map_all["数据量"]=lenall
    map_all["训练时间/us"]=(endT_Train - startT_Train).microseconds
    map_all["测试时间/us"]=(endT - startT).microseconds
    m_map_list.append(map_all)

def runOne():
    global m_map_list
    print ("-- 开始 --",m_current_sklearn)
    m_map_list = []
    for testC in m_count:
        test(testC)
    m_map_all[m_current_sklearn] = m_map_list
    print ("-- 结束 --",m_current_sklearn)


if __name__ =="__main__":
    for tmpItem in m_sklearn_list:
        m_current_sklearn = tmpItem
        runOne()
    # 打印表格
    for tmpItem in m_sklearn_list:
        print("当前算法：",tmpItem)
        print("数据量\t准确度\t训练时间/us\t测试时间/us")
        for key in m_map_all[tmpItem]:
            print("%d\t%f\t%d\t%d"%(key["数据量"],key["精确率"],key["训练时间/us"],key["测试时间/us"]))
    # m_sklearn_list = ["LinearSVC","LinearSVR","NuSVC","NuSVR","OneClassSVM","SVC","SVR","l1_min_c"]
