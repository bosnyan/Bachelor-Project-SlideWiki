import random
import glob

pathh = "sample/*.txt"
dirri = glob.glob(pathh)

rand_smpl = [ dirri[i] for i in sorted(random.sample(range(len(dirri)), 100)) ]

for i in rand_smpl:
    text = open(i, 'r+', encoding="utf-16")
    file_name = i[11:]
    print(file_name)
    result = open("sample/" + file_name, 'w+', encoding="utf-16")
    process = text.readlines()
    for sent in process:
        sent = sent.strip()
        result.write(sent)
        result.write('\n')

    text.close()
    result.close()