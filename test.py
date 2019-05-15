from nltk.tokenize import word_tokenize, sent_tokenize
import datetime
sent ="mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamedmohamed mohamed mohamed mohamed mohamed mohamedmohamed momohamed mohamed mohamed mohamed mohamed mohamed hamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamed mohamedmohamed mohamed mohamed mohamed mohamed mohamedmohamed momohamed mohamed mohamed mohamed mohamed mohamed hamed mohamed mohamed mohamed mohamed" * 100000

def f1(sent):
    words = word_tokenize(sent)
    return len(words)

def f2(sent):
    count=0
    words = word_tokenize(sent)
    for word in words:
        count+=1
    return count
print("************* With a loop *************")
start = datetime.datetime.now()
print(f2(sent))
end = datetime.datetime.now()
print(end - start) 

print("********** Oprimized **************")
start = datetime.datetime.now()
print(f1(sent))
end = datetime.datetime.now()
print(end - start) 