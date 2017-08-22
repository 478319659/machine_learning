# coding=gbk
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

#KNN�㷨ʵ��
#���ڷ��������������inX,ѵ������dataSet,��ǩ����labels,ѡ�����ڽ�����Ŀk
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0] #4
    print inX
    print tile(inX, (dataSetSize,1))
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    print diffMat
    sqDiffMat = diffMat**2
    print sqDiffMat
    sqDistances = sqDiffMat.sum(axis=1)
    print sqDistances
    distances = sqDistances**0.5
    print distances
    sortedDistIndicies = distances.argsort()
    print sortedDistIndicies
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1 # ����ѡ��ֵ���м�1�Ĳ���
        #���ڷ���ı�ǩ�ͱ�ǩ��������,����
        sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]  #ȡ����һ�е�һ��,��ֵΪԤ��ı�ǩ

def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index +=1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet/tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals

def classifyPerson():
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person:", resultList[classifierResult-1]


def datingClassTest():
    hoRatio = 0.10      #hold out 10%
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')       #load data setfrom file
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
            print '---------------------------'
    print "the total error rate is: %f" % (errorCount/float(numTestVecs))
    print errorCount







if __name__ == '__main__':
    group,labels = createDataSet()
    # print group
    # print labels
    # print group.shape[0]
    # a=[[1,2,3],[5,4]]
    # print a
    # print tile(a,(4,1))
    classify0([0,0],group,labels,3)
    # datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    # print datingDataMat,datingLabels[0:20]
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
    # plt.show()
    # normMat,ranges,minVals = autoNorm(datingDataMat)
    # print normMat,ranges,minVals
    # datingClassTest()
    # classifyPerson()