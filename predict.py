import sys
import pickle
import numpy as np
from collections import defaultdict

from test import predict, read_translation_lengths
from train import load_features, clamp

def score_testfiles(model, feature_filename, translations_filename):
    features = load_features(feature_filename)
    labels_predicted = predict(model, features) 
    lengths = read_translation_lengths(translations_filename) 
    if labels_predicted.ndim==2 and np.shape(labels_predicted)[1]==4:
        ter_predicted = []
        for (i,d,s,b), l in zip(labels_predicted, lengths):
            i = clamp(round(i, 0))
            d = clamp(round(d, 0), 0, l-1)
            s = clamp(round(s, 0), 0, l)
            b = clamp(round(b, 0), 0, l)
            ter_predicted.append(clamp((i+d+s+b)/(l+i-d), 0, 1))
        labels_predicted = ter_predicted
    return labels_predicted

def print_labels(labels, export_format="simple"):
    rounded_labels = [round(l,3) for l in labels]
    sorted_labels = sorted(rounded_labels)
    
    for i, label in enumerate(labels):
        if export_format=="submission":
            print "MLP4\t{}\t{}\t{}".format(i+1, round(label, 5), sorted_labels.index(round(label, 3))+1)
        else:
            print label
        
if __name__ == "__main__":
    model_filename = sys.argv[1]
    test_feature_filename = sys.argv[2]
    test_translations_filename = sys.argv[3]
    
    export_format = "simple"
    
    try:
        if sys.argv[4] == "--submissionformat":
            export_format = "submission"
    except:
        pass        
    
    model = pickle.load(open(model_filename))
    labels = score_testfiles(model, test_feature_filename, test_translations_filename)
    print_labels(labels, export_format)
    
    
    
    
