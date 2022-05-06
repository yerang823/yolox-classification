import numpy as np
import cv2
import matplotlib.pyplot as plt



def Eval(txt_pred, txt_gt, root):     
    
    
    ## Load annotations of GT, Pred

    # predict
    with open(path,'r') as f: 
        pred=f.readlines()
    # GT 
    with open(path2, 'r') as f:
        gt=f.readlines()
    
    pred.sort()
    gt.sort()
    
    
    pred_new=[]
    for i in range(len(pred)):
        pred_new.append(pred[i].split('/')[-1])
        
    pred_gt_li = pred_new + gt
    pred_gt_li.sort()
    pred_gt_li[:5]
    
    tot_dsc = []
    tot_tp = []
    tot_fp = []
    tot_fn = []
    for i in range(len(pred_gt_li)):
        
        if i==0:
            # 그냥 이미지 읽어
            img = cv2.imread(root + pred_gt_li[i].split(',')[0])
            empty = np.zeros((img.shape[0],img.shape[1]))
        
        else:
            if pred_gt_li[i].split(',')[0] != pred_gt_li[i-1].split(',')[0]: # 새로운 이미지 네임, 이전거랑 지금거랑 이름 다르면
                #print(pred_gt_li[i-1].split(',')[0])
                #print(np.unique(empty))
                #plt.imshow(empty,cmap='gray')
                #plt.show()
                
                if len(np.unique(empty)) != 2: # pred 아예 없는경우 제외하려고
                    fn = len(empty[empty==1])
                    fp = len(empty[empty==2])
                    tp = len(empty[empty==3]) + len(empty[empty==4]) +len(empty[empty==5])
                    DSC = 2*tp / (2*tp+fp+fn)
                    tot_dsc.append(DSC)
                    tot_tp.append(tp)
                    tot_fp.append(fp)
                    tot_fn.append(fn)
                
                img = cv2.imread(root + pred_gt_li[i].split(',')[0])
                empty = np.zeros((img.shape[0],img.shape[1]))
                
        
        
        if pred_gt_li[i].split(',')[1]=='0.0': # pred
            value = 2
            x1=int(float(pred_gt_li[i].split(',')[3]))
            y1=int(float(pred_gt_li[i].split(',')[4]))
            x2=int(float(pred_gt_li[i].split(',')[5]))
            y2=int(float(pred_gt_li[i].split(',')[6]))
        else: # gt
            value = 1
            x1=int(float(pred_gt_li[i].split(',')[1]))
            y1=int(float(pred_gt_li[i].split(',')[2]))
            x2=int(float(pred_gt_li[i].split(',')[3]))
            y2=int(float(pred_gt_li[i].split(',')[4]))
            
        empty[y1:y2, x1:x2] += value
        
        if i==len(pred_gt_li)-1:
            if len(np.unique(empty)) != 2: # pred 아예 없는경우 제외하려고
                fn = len(empty[empty==1])
                fp = len(empty[empty==2])
                tp = len(empty[empty==3]) + len(empty[empty==4]) +len(empty[empty==5])
                DSC = 2*tp / (2*tp+fp+fn)
                tot_dsc.append(DSC)
                tot_tp.append(tp)
                tot_fp.append(fp)
                tot_fn.append(fn)
                
                
    print('len(tot_dsc)=',len(tot_dsc))
    print('avg DSC = ', sum(tot_dsc)/len(tot_dsc))
    print('avg TP = ', sum(tot_tp)/len(tot_tp))
    print('avg FP = ', sum(tot_fp)/len(tot_fp))
    print('avg FN = ', sum(tot_fn)/len(tot_fn))
    
    
    return 0



if __name__=='__main__':    
    path='./YOLOX_outputs/yolox_x_discolor/vis_res/2022_04_15_01_47_29/result.txt' #predict txt
    path2='./datasets/Discolor/test.txt' # gt txt
    root = './datasets/Discolor/val2017/'
    
    Eval(path, path2, root)