import glob

path='./YOLOX_outputs/yolox_x/vis_res/2022_03_02_03_24_02/result.txt'

#test_li=glob.glob(path)
f=open(path,'r')
lines = f.readlines()
f.close()

cnt_n1, cnt_n2, cnt_a, cnt_p0, cnt_p1, cnt_p2, cnt_p3 = 0,0,0,0,0,0,0
cnt_n1_tp, cnt_n2_tp, cnt_a_tp, cnt_p0_tp, cnt_p1_tp, cnt_p2_tp, cnt_p3_tp = 0,0,0,0,0,0,0


for i in range(len(lines)):
         
    # GT
    gt_clas = lines[i].split('_')[-1][:2]
    
    # label
    label = int(float(lines[i].split(',')[1]))
    

    if gt_clas=='N1':
        cnt_n1+=1
        if label==0:
            cnt_n1_tp+=1
            
    elif gt_clas=='N2':
        cnt_n2+=1
        if label==0:
            cnt_n2_tp+=1

    elif gt_clas=='A1':
        cnt_a+=1
        if label==0:
            cnt_a_tp+=1

    elif gt_clas=='P0':
        cnt_p0+=1
        if label==1:
            cnt_p0_tp+=1
            
    elif gt_clas=='P1':
        cnt_p1+=1
        if label==1:
            cnt_p1_tp+=1

    elif gt_clas=='P2':
        cnt_p2+=1
        if label==1:
            cnt_p2_tp+=1

    elif gt_clas=='P3':
        cnt_p3+=1
        if label==1:
            cnt_p3_tp+=1

print('    N1, N2, A, P0, P1, P2, P3')
print('GT=',cnt_n1, cnt_n2, cnt_a,cnt_p0,cnt_p1,cnt_p2,cnt_p3)
print('TP=',cnt_n1_tp,cnt_n2_tp,cnt_a_tp,cnt_p0_tp,cnt_p1_tp,cnt_p2_tp,cnt_p3_tp)