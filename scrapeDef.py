from bs4 import BeautifulSoup
import requests as req

rd_fl_url = "/home/simon/Documents/Brain/BeautifulSoup - Language/english.txt"
wrt_fl_url = "/home/simon/Documents/Brain/BeautifulSoup - Language/QA.txt"
dictUrl = "https://www.dictionary.com/browse/"
frenchTranslationUrl = "https://www.larousse.fr/dictionnaires/anglais-francais/"

# Read in the words to look up. 
def readEnglishFile():
    wrds = list()
    with open(rd_fl_url, "r") as rd:
        for line in rd:
            # first letter caps, rest low
            word = line.strip().lower().title()
            wrds.append(word)
    # with open(rd_fl_url, "w") as f:
    #     f.write('BYTEORDER')
    return wrds[1:]

# Use BeautifulSoup to get the definitions. 
def getInfo(ls):

    dne = list()

    it = 1
    for i in ls:
        print("Iteration: " + str(it) + "...")

        dfs = list()
        egs = list()

        
        # Store definitions and examples. 
        # for element in soup.find_all(True, {"class":["ind", "ex", "iteration", "subsenseIteration"]}):
        #     print(element)
        #     if (element['class'][0] == "iteration" or element['class'][0] == "subsenseIteration"):
        #         itrs.append(element.text)
        #         itr +=1
        #         egs[itr] = list()
        #     elif (element['class'][0] == "ind"):
        #         print(element.text)
        #         dfs.append(element.text)
        #     else:
        #         ls = egs[itr]
        #         ls.append(element.text)
        #         egs[itr] = ls


        result = req.get(dictUrl + i)
        soup = BeautifulSoup(result.text, "lxml")
        subIt = 0
        # Related forms
        relatedWords = list()
        for element in soup.find_all(True, {"class":["one-click-content css-bhupyz e614id60", "one-click-content css-1p89gle e1q3nk1v4" , "one-click-content css-a8m74p e15kc6du6"]}):
            print(element.contents[0])
            if (element['class'][0] == "one-click-content css-1p89gle e1q3nk1v4"):
                dfs.append(element.text)
                print(element.contents[0])
            elif (element['class'][0] == "one-click-content css-a8m74p e15kc6du6"):
                egs.append(element.text)
            elif (element['class'][0] == "one-click-content css-bhupyz e614id60"):
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
        
        dne.append((dfs, egs, relatedWords, translation))
        it += 1

    return dne

# Write neatly in a txt file. 
def writeQA(dne, wrds):
    # previousDef = list()
    # with open(wrt_fl_url , "r") as f:
    #     previousDef =  f.readlines()
    with open(wrt_fl_url , "w") as wt:
        # wt.writelines(previousDef)
        for i, item in enumerate(dne):
            s = str(i+1) + ". " + wrds[i] + "\n\n"
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
                            

if __name__ == "__main__":
    wrds = readEnglishFile()
    dne = getInfo(wrds)
    print(dne)
    # writeQA(dne, wrds)
