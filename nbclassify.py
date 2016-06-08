import sys
import os
import string

def classifyReview(text,naiveMap,swList):
    ptCount = 0
    pfCount = 0
    ntCount = 0
    nfCount = 0
    ignoreList = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in ignoreList)
    text = refineText(text)
    text = text.replace('\n','').replace('\r',' ')
    
    listWords = text.split(' ')
    for word in listWords:
        if validWords(word,swList):
            if not word.isupper():
                word = word.lower()
            if word in naiveMap:
                ptCount = ptCount + naiveMap[word]['PT']
                pfCount = pfCount + naiveMap[word]['PF']
                ntCount = ntCount + naiveMap[word]['NT']
                nfCount = nfCount + naiveMap[word]['NF']
    maxVal = ptCount
    ptCaption = 'PT'
    if maxVal < pfCount:
        ptCaption = 'PF'
        maxVal = pfCount
    if maxVal < ntCount:
        ptCaption = 'NT'
        maxVal = ntCount
    if maxVal < nfCount:
        ptCaption = 'NF'
        maxVal = nfCount
    return  ptCaption
    
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


def readNBModelTextFile(naiveMap):
    with open('nbmodel.txt') as fileToRead:
        for line in fileToRead:
            pList = line.replace('\n','').replace('\r',' ').split(' ')
            Obj = dict()
            Obj[pList[1]] = float(pList[2])
            Obj[pList[3]] = float(pList[4])
            Obj[pList[5]] = float(pList[6])
            Obj[pList[7]] = float(pList[8])
            naiveMap[pList[0]] = Obj
        

naiveMap = dict()
readNBModelTextFile(naiveMap)
mainDir = sys.argv[1]
positiveDirList = next(os.walk(mainDir))[1]
fileTowrite = open('nboutput.txt','w')
swList = createStopWords()

for positiveDirName in positiveDirList:
    positiveDirPath = os.path.join(mainDir,positiveDirName)
    truthDirList = next(os.walk(positiveDirPath))[1]
    for truthDirName in truthDirList:
        folderePath = os.path.join(positiveDirPath,truthDirName)
        folderList = next(os.walk(folderePath))[1]
        for folderName in folderList:
#             if (folderName != 'fold1'):
#                 continue
            filePath = os.path.join(folderePath,folderName)
            fileList = next(os.walk(filePath))[2]
            for fileName in fileList:
                filePathActual = os.path.join(filePath,fileName)
                f = open(filePathActual)
                text =  f.read() 
                classVal = classifyReview(text,naiveMap,swList)
                
                strToPrint = ''
                if classVal == 'PT':
                    strToPrint = 'truthful positive ' + filePathActual
                if classVal == 'PF':
                    strToPrint = 'deceptive positive ' + filePathActual
                if classVal == 'NT':
                    strToPrint = 'truthful negative ' + filePathActual
                if classVal == 'NF':
                    strToPrint = 'deceptive negative ' + filePathActual
                
                fileTowrite.write(strToPrint + '\n')
