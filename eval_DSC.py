def get_iou2(boxA, boxB_li): # pred, gt
    
    #if xB-xA > 0 and yB-yA > 0:
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)

    interArea=0
    boxBArea=0
    for boxB in boxB_li:    
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        if xB-xA > 0 and yB-yA > 0:
            interArea += (xB - xA + 1) * (yB - yA + 1) ## 
            boxBArea += (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1) ##
            print('interArea=',interArea)

    iou=interArea / float(boxAArea + boxBArea - interArea)
        
    #else:
    #    iou = 0
    
    return iou
    
    
def main(pred,gt):

    tot_iou_li=[]
    tmp_iou_li=[]
    TP,FP=0,0
    for i in range(len(pred)):
            
        nameonly = pred[i].split(',')[0].split('/')[-1]
        
        x1 = int(float(pred[i].split(',')[3]))
        y1 = int(float(pred[i].split(',')[4]))
        x2 = int(float(pred[i].split(',')[5]))
        y2 = int(float(pred[i].split(',')[6][:-1]))
    
        gt_box_li=[]
        for j in range(len(gt)):
            nameonly2 = gt[j].split(',')[0].split('/')[-1]
            if nameonly==nameonly2:
                x11 = int(float(gt[j].split(',')[1]))
                y11 = int(float(gt[j].split(',')[2]))
                x22 = int(float(gt[j].split(',')[3]))
                try:
                  y22 = int(float(gt[j].split(',')[4])) # ,696,
                except:
                  y22 = int(float(gt[j].split(',')[4][:-1])) # ,696\n
                gt_box_li.append([x11, y11, x22, y22])
    
        
        pred_box=[x1,y1,x2,y2]
        iou =  round(get_iou2(pred_box, gt_box_li),4)
        print(i,'/',len(pred), nameonly)
        print('iou=', iou)
        #print('gt_box_li=',gt_box_li)
        
        
        if len(tmp_iou_li)==0:
            tmp_iou_li.append(iou)
        elif len(tmp_iou_li)>0 and pred[i-1].split(',')[0].split('/')[-1] == nameonly :
            tmp_iou_li.append(iou)
        elif (len(tmp_iou_li)!=0 and pred[i-1].split(',')[0].split('/')[-1] != nameonly) or i==len(pred)-1:
            TP+=1
            if len(tmp_iou_li)>1:
                FP += len(tmp_iou_li)-1
        
            print('max(tmp_iou_li)====',max(tmp_iou_li))
            tot_iou_li.append(max(tmp_iou_li))
            tmp_iou_li=[]
            tmp_iou_li.append(iou)
            
    
        #print('tmp_iou_li=',tmp_iou_li)
    
    #print('tot_iou_li=',tot_iou_li)
    
    tot_iou_li=[x for x in tot_iou_li if x>=0.3]
    
    print('======================= RESULT ============================')
    print('len(tot_iou_li)=',len(tot_iou_li))
    print('TP FP=',TP,FP)
    print('FP/image=', round(FP/len(tot_iou_li),4))
    print('DSC = ',round(sum(tot_iou_li)/len(tot_iou_li),4))





if __name__=="__main__":
    
    ## Load annotations of GT, Pred

    # predict
    path='./YOLOX_outputs/yolox_x_erosion/vis_res/2022_04_15_07_53_31/result.txt'
    with open(path,'r') as f:
        pred=f.readlines()
    # GT 
    path2='./datasets/Erosion2/test.txt'
    with open(path2, 'r') as f:
        gt=f.readlines()
        
    pred.sort()
    gt.sort()
    
    main(pred,gt)

    
    
    