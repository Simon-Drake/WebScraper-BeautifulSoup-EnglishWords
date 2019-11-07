from bs4 import BeautifulSoup
import requests as req

englishWords = "/home/simon/Documents/Brain/BeautifulSoup - Language/english.txt"
wordsDone = "/home/simon/Documents/Brain/BeautifulSoup - Language/englishDone.txt"
wrt_fl_url = "/home/simon/Documents/Brain/BeautifulSoup - Language/qa.txt"
numberFile = "/home/simon/Documents/Brain/BeautifulSoup - Language/nextNumber.txt"
bs_url = "https://www.lexico.com/en/definition/"
dictUrl = "https://www.dictionary.com/browse/"
frenchTranslationUrl = "https://www.larousse.fr/dictionnaires/anglais-francais/"

# Read in the words to look up. 
def readEnglishFile(URL):
    wrds = list()
    with open(URL, "r") as rd:
        for line in rd:
            # first letter caps, rest low
            word = line.strip().lower().title()
            wrds.append(word)
    return wrds[1:]

def readNumber():
    with open(numberFile, "r") as f:
        line = f.readline()
        return line[0]


def updateNumber(lastN):
    with open(numberFile, "w") as f:
        f.write(lastN)

# Use BeautifulSoup to get the definitions. 
def getInfo(ls):

    dne = list()

    it = 1
    for i in ls:
        print("Iteration: " + str(it) + "...")

        itrs = list()
        dfs = list()
        egs = dict()
        itr = 0

        # Make request and create a soup object. 
        result = req.get(bs_url + i.lower())
        soup = BeautifulSoup(result.text, "lxml")

        # Store definitions and examples. 
        for element in soup.find_all(True, {"class":["ind", "ex", "iteration", "subsenseIteration"]}):
            if (element['class'][0] == "iteration" or element['class'][0] == "subsenseIteration"):
                itrs.append(element.text)
                itr +=1
                egs[itr] = list()
            elif (element['class'][0] == "ind"):
                dfs.append(element.text)
            else:
                ls = egs[itr]
                ls.append(element.text)
                egs[itr] = ls


        result = req.get(dictUrl + i)
        soup = BeautifulSoup(result.text, "lxml")
        # Related forms
        relatedWords = list()
        for element in soup.find_all(True, {"class":["one-click-content css-bhupyz e614id60", "one-click-content css-1p89gle e1q3nk1v4" , "one-click-content css-a8m74p e15kc6du6"]}):
            if "noun" in element.text or "adjective" in element.text or "adverb" in element.text:
                relatedWords.append(element.text.replace("·", ""))

        relatedWords = list(set(relatedWords))

        # Get the translation
        result = req.get(frenchTranslationUrl + i)
        soup = BeautifulSoup(result.text, "lxml")

        
        translations = soup.find_all(True, {"class":["Traduction", "Traduction2"]})
        translation = list()


        if len(translations) > 0 :
            for element in translations:
                translation.append(element.text.replace("\n", "").replace(" f", "").replace("Conjugaison", ""))
        else:
            translation.append("NULL")
        
        dne.append((list(zip(itrs, dfs)), egs, relatedWords, translation))
        it += 1

    return dne

# Write neatly in a txt file. 
def writeQA(dne, wrds, lastN):
    # previousDef = list()
    # with open(wrt_fl_url , "r") as f:
    #     previousDef =  f.readlines()
    with open(wrt_fl_url , "w") as wt:
        # wt.writelines(previousDef)
        for i, item in enumerate(dne):
            s = lastN + ". " + wrds[i] + "\n\n"
            for j in range(0, len(dne[i][0])):
                s += dne[i][0][j][0] + " " + dne[i][0][j][1] + "\n\n"
                s += "\n\nExamples: \n\n"
                for k in range(0, len(dne[i][1][j+1])):
                    # if k>5:
                    #     continue
                    s += dne[i][1][j+1][k] + "\n\n"
                    if k == len(dne[i][1][j+1]) - 1:
                        s += "\n\n"
            s += "Related Forms: \n\n"
            for j in dne[i][2]:
                s += j + "\n"  
            s += "\n"     
            s += "\n\nFrench: \n\n"
            for j in dne[i][3]:
                s += j + "\n"  
            s += "\n\n\n"  
            wt.write(s)
            lastN = str(int(lastN) + 1)
            updateNumber(lastN)
                            
def writeWordsDone(wordsToAdd):
    wordsToAdd = [word + "\n" for word in wordsToAdd]
    done = list()
    with open(wordsDone, "r") as f:
        done = f.readlines()

    with open(wordsDone, "w") as f:
        done += wordsToAdd
        f.writelines(done)


if __name__ == "__main__":
    lastNumber = readNumber()
    wrds = readEnglishFile(englishWords)
    wordsDone_ = readEnglishFile(wordsDone)
    wordsToDo = [word for word in wrds if word not in wordsDone_]
    dne = getInfo(wordsToDo)
    if len(dne[0]) == 0:
        print(dne)
        input("no definitions, continue?")
    writeQA(dne, wordsToDo, lastNumber)
    writeWordsDone(wordsToDo)
