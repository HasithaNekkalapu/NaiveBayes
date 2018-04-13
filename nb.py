# Name: Hasitha Nekkalapu
# ID: 1001511218
# NetID: hxn1218

from math import log
import random
import time
from sklearn.model_selection import train_test_split


#dataset .data contains the instances and .names contains the attribute names
DATASET = 'agaricus-lepiota.data'
ATTRIBUTES = 'agaricus-lepiota.names'

attributes_yes_list = []
attributes_no_list = []

positive_dataset = []
negative_dataset = []

pos_train = []
neg_train = []

training_data = []
test_data = []

g_attributes = [] # Doesn't include poisonous or edible column
g_attributes_dictionary = {}

def prepare_datasets():
    with open(DATASET, 'r+') as dataset_file:
        dataset_lines = dataset_file.readlines()

    for line in dataset_lines:
        attributes = line.split(',')

        # Get rid of newline character on last attribute
        attributes[-1] = attributes[-1].strip()

        #Seperating edible and poisonous data
        if attributes[0] == 'e':
            positive_dataset.append((attributes[0], attributes[1:]))
        else:
            negative_dataset.append((attributes[0], attributes[1:]))

    #Creating training and testing datasets(Splitting the data)
    while len(positive_dataset) and len(negative_dataset):
        rand_pos =  random.randint(0,min(len(positive_dataset),len(negative_dataset))-1)
        if(len(training_data)<  4000):
        	training_data.append(positive_dataset.pop(rand_pos))
        	training_data.append(negative_dataset.pop(rand_pos))
        	#print(len(training_data))

        if len(positive_dataset) and len(negative_dataset):
            rand_pos = random.randint(0, min(len(positive_dataset),len(negative_dataset))-1)
            if(len(training_data)< 4000):
            	training_data.append(positive_dataset.pop(rand_pos))
            	training_data.append(negative_dataset.pop(rand_pos))

        if len(positive_dataset) and len(negative_dataset):
            rand_pos = random.randint(0, min(len(positive_dataset),len(negative_dataset))-1)
            test_data.append(positive_dataset.pop(rand_pos))
            test_data.append(negative_dataset.pop(rand_pos))


def parse_attributes():
    with open(ATTRIBUTES, 'r+') as attributes_file:
        for line in attributes_file:
            pair = line.strip().split()
            g_attributes.append(pair[0])
            g_attributes_dictionary[pair[0]] = pair[1].split(',')

#making a poisonous and edible attribute list
def prepare_attributes_lists():
    attr_count = 0
    val_count = 0

    for i in range(len(g_attributes)):
        attributes_yes_list.append([])
        attributes_no_list.append([])

    for i in attributes_yes_list:
        for j in range(12):
            i.append(0)

    for i in attributes_no_list:
        for j in range(12):
            i.append(0)

    for attr in g_attributes:
        val_count = 0
        for value in g_attributes_dictionary[attr]:
            for example in training_data:
                if value == example[1][attr_count] and example[0] == 'e':
                    attributes_yes_list[attr_count][val_count] += 1
            val_count += 1
        attr_count += 1
    attr_count = 0

    for attr in g_attributes:
        val_count = 0
        for value in g_attributes_dictionary[attr]:
            for example in training_data:
                if value == example[1][attr_count] and example[0] == 'p':
                    attributes_no_list[attr_count][val_count] += 1
            val_count += 1
        attr_count += 1

#NaiveBayes implementation
def naive_bayes(example, neg, pos):
    count = 0
    pos_prob = 1.0
    neg_prob = 1.0

    for attr in example:
        pos_prob *= attributes_yes_list[count][g_attributes_dictionary[g_attributes[count]].index(attr)]
        neg_prob *= attributes_no_list[count][g_attributes_dictionary[g_attributes[count]].index(attr)]
        #print 'neg_prob: %s		pos_prob: %s' % (neg_prob,pos_prob)
        count += 1

    if neg_prob > pos_prob:
        return 'p'
    else:
        return 'e'

if __name__ == '__main__':
    start = time.time()
    prepare_datasets()
    parse_attributes()
    prepare_attributes_lists()

    num_pos = 0
    num_neg = 0
    print('Size of training data set :: '+str(len(training_data)))
    print('Size of Test Set :: '+str(len(test_data)))
    for i in training_data:
        if i[0] == 'e':
            num_pos += 1
            pos_train.append(i[1])
        else:
            num_neg += 1
            neg_train.append(i[1])

    correct = 0
    wrong = 0
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for ex in test_data:
        actual = ex[0]
        calculated = naive_bayes(ex[1], num_neg, num_pos)
        #print 'actual: %s  classified: %s' % (actual,calculated)
        if actual == calculated:
            correct += 1
            if actual == 'e' and calculated == 'e':
            	TP += 1
            if actual == 'p' and calculated == 'p':
            	TN += 1
        else:
        	wrong += 1
        	if actual == 'e' and calculated == 'p':
        		FN += 1
        	if actual == 'p' and calculated == 'e':
        		FP += 1
    print('Confusion Matrix :: ')
    print('TP:%s'%TP+'  '+'FN:%s'%FN)
    print('TN:%s'%TN+'  '+'FP:%s'%FP)
   # print('Percent correct: %f' % (float(correct*100)/float(len(test_data))))
    print('Accuracy is: %f'%((TP+TN)/len(test_data)))
    #print('Runtime: %s' % (time.time() - start))