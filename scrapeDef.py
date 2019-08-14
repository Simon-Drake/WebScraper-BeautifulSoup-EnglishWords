from bs4 import BeautifulSoup
import requests as req

rd_fl_url = "/home/simon/Documents/Brain/English/english.txt"
wrt_fl_url = "/home/simon/Documents/Brain/English/QA.txt"
bs_url = "https://en.oxforddictionaries.com/definition/"

# Read in the words to look up. 
def readEnglishFile():
    wrds = list()
    with open(rd_fl_url, "r") as rd:
        for line in rd:
            wrds.append(line.strip().lower())
    return wrds[1:-1]

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
        result = req.get(bs_url + i)
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
        dne.append((list(zip(itrs, dfs)), egs))
        it += 1
    return dne

# Write neatly in a txt file. 
def writeQA(dne, wrds):
    with open(wrt_fl_url , "w") as wt:
        for i, item in enumerate(dne):
            s = str(i+1) + ". " + wrds[i] + "\n\n"
            for j in range(0, len(dne[i][0])):
                s += dne[i][0][j][0] + " " + dne[i][0][j][1] + "\n\n"
                s += "Examples: \n\n"
                for k in range(0, len(dne[i][1][j+1])):
                    if k>5:
                        continue
                    s += dne[i][1][j+1][k] + "\n\n"
            wt.write(s)
                            

if __name__ == "__main__":

    wrds = readEnglishFile()
    dne = getInfo(wrds)
    writeQA(dne, wrds)
