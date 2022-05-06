import glob
#import argparse
#from utils.callbacks import Callbacks
from sklearn.metrics import confusion_matrix,accuracy_score,f1_score,precision_score,recall_score

def evaluate(pred_path):

    label=[]
    pred=[]
    
    f=open(pred_path,'r')
    lines=f.readlines()
    f.close()
    
    
    for i in range(len(lines)):

        # label        
        clas=lines[i].split('_')[-1][0]
        if clas=='N' or clas=='A':
            label.append(0)
        else:
            label.append(1)

        # pred
        pred.append(int(float(lines[i].split(',')[1])))
        
    cm=confusion_matrix(y_true=label, y_pred=pred)
    specificity = cm[0][0]/(cm[0][0]+cm[0][1])
    sensitivity = cm[1][1]/(cm[1][0]+cm[1][1])
    print(cm)
    print('TP  TN  FP  FN')
    print(cm[1][1], cm[0][0], cm[0][1],  cm[1][0])
    print('sensitivity = ', sensitivity)
    print('specificity = ', specificity)
    



if __name__=='__main__':

    path='./YOLOX_outputs/yolox_x_irregular/vis_res/2022_04_13_01_04_54/result.txt'
    print('path=',path)
    evaluate(path)
