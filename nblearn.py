import sys
import os
import math
import string

def validWords(word,swList):
    if not word:
        return False
    if word in swList:
        return False;
    return True

def createStopWords():
    swList = ["a","about","above","after","again","against","all","am","an","and","any","are","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can't","cannot","could","couldn't","did","didn't","do","does","doesn't","doing","don't","down","during","each","few","for","from","further","had","hadn't","has","hasn't","have","haven't","having","he","he'd","he'll","he's","her","here","here's","hers","herself","him","himself","his","how","how's","i","i'd","i'll","i'm","i've","if","in","into","is","isn't","it","it's","its","itself","let's","me","more","most","mustn't","my","myself","no","nor","not","of","off","on","once","only","or","other","ought","our","ours    ourselves","out","over","own","same","shan't","she","she'd","she'll","she's","should","shouldn't","so","some","such","than","that","that's","the","their","theirs","them","themselves","then","there","there's","these","they","they'd","they'll","they're","they've","this","those","through","to","too","under","until","up","very","was","wasn't","we","we'd","we'll","we're","we've","were","weren't","what","what's","when","when's","where","where's","which","while","who","who's","whom","why","why's","with","won't","would","wouldn't","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"]
    return swList


def refineText(text):
    text = text.replace("."," ")
    text = text.replace(","," ")
    text = text.replace("\n"," ").replace("\r"," ")
    text = text.replace(";"," ")
    text = text.replace("!"," ")
    text = text.replace("-"," ")
    text = text.replace("\\"," ")
    text = text.replace("'"," ")
    text = text.replace("("," ")
    text = text.replace(")"," ")
    text = text.replace(":"," ")
    text = text.replace("<"," ")
    text = text.replace(">"," ")
    text = text.replace("{"," ")
    text = text.replace("/"," ")
    text = text.replace("["," ")
    text = text.replace("]"," ")
    text = text.replace("}"," ")
    text = text.replace("_"," ")
    text = text.replace("*"," ")
    text = text.replace("$"," ")
    text = text.replace("#"," ")
    text = text.replace("@"," ")
    text = text.replace("="," ")
    text = text.replace("%"," ")
    text = text.replace("^"," ")
    text = text.replace("&"," and ")
    text = text.replace("\""," ")
    text = text.replace("?"," ")
    return text

def learnBayes(text,naiveMap,isPositive,isTruthful,countMap,swList):
    ignoreList = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in ignoreList)
    text = refineText(text)
    text = text.replace('\n','').replace('\r',' ')
    
    listWords = text.split(' ')
    
    key = ''
    keyWordCount = ''
    if isPositive and isTruthful:
        key = 'PT'
        keyWordCount = 'PTCount'
    if isPositive and not isTruthful:
        key = 'PF'
        keyWordCount = 'PFCount'
    if not isPositive and isTruthful:
        key = 'NT'
        keyWordCount = 'NTCount'
    if not isPositive and not isTruthful:
        key = 'NF'
        keyWordCount = 'NFCount'
    for word in listWords:
        if validWords(word,swList):
            wordObj =  dict()
            if not word.isupper():
                word = word.lower()
            print word
            if word in naiveMap:
                wordObj = naiveMap[word]
            else:
                wordObj['PT'] = 0
                wordObj['PF'] = 0
                wordObj['NT'] = 0
                wordObj['NF'] = 0
                countMap['totalWords'] = countMap['totalWords'] + 1
            countMap[keyWordCount] = countMap[keyWordCount] + 1
            wordObj[key] = wordObj[key] + 1
            naiveMap[word] = wordObj

def smoothingFunction(naiveMap,countMap,probabilityMap):
    ls = list()
    for key in naiveMap:
        obj = naiveMap[key]
        ls.append(key)
        obj['PT'] = obj['PT'] + 1
        obj['PF'] = obj['PF'] + 1
        obj['NT'] = obj['NT'] + 1
        obj['NF'] = obj['NF'] + 1
    
    countMap['PTCount'] = countMap['PTCount'] + countMap['totalWords']
    countMap['PFCount'] = countMap['PFCount'] + countMap['totalWords']
    countMap['NTCount'] = countMap['NTCount'] + countMap['totalWords']
    countMap['NFCount'] = countMap['NFCount'] + countMap['totalWords']
    
    for key in naiveMap:
        obj = naiveMap[key]
        wordObj =  dict()
        wordObj['PT'] = math.log(obj['PT']) - math.log(countMap['PTCount'])
        wordObj['PF'] = math.log(obj['PF']) - math.log(countMap['PFCount'])
        wordObj['NT'] = math.log(obj['NT']) - math.log(countMap['NTCount'])
        wordObj['NF'] = math.log(obj['NF']) - math.log(countMap['NFCount'])
        probabilityMap[key] = wordObj

def writeNBModelTextFile(probabilityMap):
    fileTowrite = open('nbmodel.txt','w')
    for key in probabilityMap:
        strToPrint = key + ' PT ' + str(probabilityMap[key]['PT']) + ' PF ' + str(probabilityMap[key]['PF']) 
        strToPrint = strToPrint + ' NT ' + str(probabilityMap[key]['NT'])+ ' NF ' + str(probabilityMap[key]['NF'])
        fileTowrite.write(strToPrint + '\n')
        

isPositive = True
isTruthful = True
naiveMap = dict()
countMap = dict()
probabilityMap = dict()
countMap['totalWords'] = 0
countMap['PTCount'] = 0
countMap['PFCount'] = 0
countMap['NTCount'] = 0
countMap['NFCount'] = 0
swList = createStopWords()

mainDir = sys.argv[1]
positiveDirList = next(os.walk(mainDir))[1]
for positiveDirName in positiveDirList:
    if ('positive' in positiveDirName.lower()):
        isPositive = True
    else:
        isPositive = False
    positiveDirPath = os.path.join(mainDir,positiveDirName)
    truthDirList = next(os.walk(positiveDirPath))[1]
    for truthDirName in truthDirList:
        if ('truthful' in truthDirName.lower()):
            isTruthful = True
        else:
            isTruthful = False
        folderePath = os.path.join(positiveDirPath,truthDirName)
        folderList = next(os.walk(folderePath))[1]
        for folderName in folderList:
#             if (folderName == 'fold1'):
#                 continue
            filePath = os.path.join(folderePath,folderName)
            fileList = next(os.walk(filePath))[2]
            for fileName in fileList:
                filePathActual = os.path.join(filePath,fileName)
                f = open(filePathActual)
                text =  f.read() 
                learnBayes(text,naiveMap,isPositive,isTruthful,countMap,swList)
                
smoothingFunction(naiveMap,countMap,probabilityMap)
writeNBModelTextFile(probabilityMap)
        
        
