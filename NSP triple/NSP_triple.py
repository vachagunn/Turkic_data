import nltk
import random
import csv

nltk.download('punkt')

file_name = 'file.txt'
delimiter = '$$$'

file = open(file_name, 'r')
tmp = file.read()

csv_file = open('NSP.csv', 'w', newline="", encoding="utf-8")
writer = csv.writer(csv_file)

# Записываем заголовки полей
writer.writerow(["sentence_A", "sentence_B", "sentence_C", "NSP", "new_url", "main_url"])

textsWithUrls = tmp.split(delimiter)

for textWithUrls in textsWithUrls:
    text = textWithUrls.split("###")[0]
    url = textWithUrls.split("###")[1]
    mainUrl = textWithUrls.split("###")[2]
    sentences = nltk.sent_tokenize(text)

    last = ''
    iterator = 0
    count = len(sentences)
    for j in range(0, count , 3):
        if(j+2 >= count):
            continue
        k = random.randint(0, 1)
        if k == 1:
            writer.writerow([sentences[j], sentences[j+1], sentences[j+2], k , url, mainUrl])
        else:
            pos = random.randint(0, 2)
            if pos == 0:
                writer.writerow([sentences[random.randint(0, count-1)], sentences[j+1], sentences[j+2], k , url, mainUrl])
            elif pos == 1:
                writer.writerow([sentences[j], sentences[random.randint(0, count-1)], sentences[j+2], k , url, mainUrl])
            elif pos == 2:
                writer.writerow([sentences[j], sentences[j+1], sentences[random.randint(0, count-1)], k , url, mainUrl])

