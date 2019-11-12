import re
num = re.compile("\d+\. ")


ans = {}
qs = {}      
with open("QA.txt", "r") as qa:
    qsas = qa.readlines()
it = 0
lines = ""
for i, item in enumerate(qsas):
    lines += item
    if(num.search(item)):
        ans[it] = lines.replace(item,"")
        qs[it+1] = item
        lines = ""
        it += 1
    ans[it] = lines

del ans[0]
qsas = [(' ', ' ')]+ list(zip([elem.split(" ")[1].replace("\n", "") for elem in qs.values()], ans.values()))
dict_qsas = dict(qsas)

wrds = list()
with open("englishDone.txt", "r") as rd:
    for line in rd:
        word = line.strip().lower().title()
        wrds.append(word)


with open("QA.txt", "w") as f:
    for i in range(1, len(wrds)):
        f.write(str(i) + ". " + wrds[i] + "\n\n" + dict_qsas[wrds[i]])