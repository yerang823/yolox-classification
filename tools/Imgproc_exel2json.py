import pandas as pd
import cv2
import matplotlib.pyplot as plt
import re
import shutil, os
import json
import glob,copy
from collections import OrderedDict



def exel2df(exel_path, root_clas, root, save_foldername):
    
    df = pd.read_excel(exel_path)
    df_new = df[df['label']==root_clas]
    df_new = df_new.reset_index(drop=True)
    print('number of images = ',len(df_new))
    
    return df_new




def visualize_GT_bbox(df_new, num_to_show, root):
    
    for i in range(num_to_show):
        filename = df_new.loc[i]['idx_cvg']
        img = cv2.imread(root+str(filename)+'.jpg')
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        string = df_new.loc[i]['custom_roi']
        numbers = re.findall(r'\d+', string)
        for j in range(int(len(numbers)/4)):
            x1 = int(numbers[j*4 + 0])
            y1 = int(numbers[j*4 + 1])
            x2 = int(numbers[j*4 + 2])
            y2 = int(numbers[j*4 + 3])

            cv2.rectangle(img2, (x1,y1),(x2,y2), (255,255,0), 3)

        plt.figure(figsize=(10,10))
        plt.imshow(img2)
        plt.axis('off')
        plt.show()
        
        
        
        
def filecopy_maketxt(df_new, dataset_name, datasetname_path, test_ratio):

    print('======================================')
    print('dataset = ', dataset_name)
    print('======================================')
    
    # 폴더 없으면 만들기
    if os.path.isdir(datasetname_path)==False: 
        os.mkdir(datasetname_path)


    if dataset_name=='train2017':
        st_num, end_num = 0, int(len(df_new)*(1-test_ratio))
    else:
        st_num, end_num = int(len(df_new)*(1-test_ratio)), int(len(df_new))
        
        
    # train.txt, val.txt 생성
    # train2017/ , val2017/ 생성하여 이미지 복사
    
    f=open('./datasets/%s/%s.txt'%(foldername,dataset_name[:3]),'w')
    for i in range(st_num, end_num):
        filename = df_new.loc[i]['idx_cvg']   
        string = df_new.loc[i]['custom_roi']
        numbers = re.findall(r'\d+', string)
        for j in range(int(len(numbers)/4)):
            x1 = int(numbers[j*4 + 0])
            y1 = int(numbers[j*4 + 1])
            x2 = int(numbers[j*4 + 2])
            y2 = int(numbers[j*4 + 3])
            f.write(str(filename)+'.jpg,'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+'\n')
        
        print(i, '/', end_num)
        shutil.copy(root+str(filename)+'.jpg', datasetname_path+str(filename)+'.jpg') 

    f.close()
    
    return 0




def GetJsonAnnotation(i,cnt, filedata_img, filedata_anno, txt_path, bbox_li, img_shape):
    
    nameonly = txt_path.split('/')[-1].split('.')[0]
        
    
    img_height = img_shape[0]
    img_width = img_shape[1]
    
    filedata_img.append({'file_name':nameonly+'.jpg', 'id':i+1, 'height': img_height, 'width':img_width})
    
    for bbox in bbox_li:
        x1,y1,b_width,b_height = bbox[0],bbox[1],(bbox[2]-bbox[0]),(bbox[3]-bbox[1])
        filedata_anno.append({'area':b_width*b_height, \
                                'iscrowd':0, 'image_id':i+1, \
                                'bbox':[x1,y1,b_width,b_height], \
                                'category_id': 1, 'id':cnt}) # 'category_id': 1 --- AW 이니깐
        cnt+=1
  
    return filedata_img,filedata_anno,cnt




def txt2json_save(foldername, dataset_name, task):

    f=open('./datasets/%s/%s.txt'%(foldername, dataset_name[:3]), 'r')
    li=f.readlines()
    f.close()


    name_li=[]
    for i in range(len(li)):
        name_li.append(li[i].split(',')[0])    
    name_unq_li = list(set(name_li))
    name_unq_li.sort()


    img_root_path='./datasets/%s/%s/'%(foldername, dataset_name)
    filedata = OrderedDict()
    fd_img=[]
    fd_anno=[]


    li_cp = copy.deepcopy(li)
    cnt = 1
    for i in range(len(name_unq_li)):

        nameonly = name_unq_li[i].split('/')[-1].split('.')[0]
        img= cv2.imread(img_root_path + nameonly + '.jpg')

        bbox_li=[]
        for j in range(len(li_cp)):
            if name_unq_li[i] in li_cp[j]:
                x1=int(float(li_cp[j].split(',')[1]))
                y1=int(float(li_cp[j].split(',')[2]))
                x2=int(float(li_cp[j].split(',')[3]))
                y2=int(float(li_cp[j].split(',')[4]))
                bbox_li.append([x1,y1,x2,y2])


        fd_img, fd_anno, cnt = GetJsonAnnotation(i,cnt, fd_img, fd_anno, name_unq_li[i], bbox_li, img.shape)
        print(i,'/',len(name_unq_li))



    filedata['images'] = fd_img
    filedata['annotations'] = fd_anno 
    
    # morphology detection
    if task=='detection':
        filedata['categories'] = [{'id':1, 'name':'%s'%foldername}] 
    elif task=='classification':
        # N vs P classification
        filedata['categories'] = [{'id':1, 'name':'negative'},
                                 {'id':2, 'name':'positive'}] 
    else:
        print('TASK ERROR !!!!')
    
    
    save_root = './datasets/%s/annotations/'%foldername
    if os.path.isdir(save_root) == False:
        os.mkdir(save_root)

    with open('./datasets/%s/annotations/instances_%s.json'%(foldername, dataset_name), "w") as json_file:
        json.dump(filedata, json_file)
        
    
    return 0
    
    
    
if __name__=='__main__':

    # 1. 학습시킬 annotation 없을 때
    #!python ForGetAnnotation.py image -n yolox-x -c ./YOLOX_outputs/yolox_x_20220227/best_ckpt.pth --path ./datasets/NP/val2017/ --conf 0.25 --nms 0.45 --tsize 640 --expn np_annotation
    
    
    # result.txt -> train.txt,  test.txt
    path = './YOLOX_outputs/np_annotation/vis_res/2022_04_27_08_43_51/result.txt' 
    with open(path,'r') as f:
        li = f.readlines()
    
    print('dataset length = ',len(li))
    
    f=open('./datasets/NP/train.txt','w')
    ff=open('./datasets/NP/test.txt','w')
    for i in range(len(li)):
        if i<=round(len(li)*0.8):
            f.write(li[i])
        else:
            ff.write(li[i])
    f.close()
    ff.close()

    
    # txt -> json
    foldername = 'NP' # 저장할 폴더명

    dataset_name = 'train2017'
    datasetname_path = './datasets/%s/%s'%(foldername,dataset_name) # './datasets/NP/val2017'
    txt2json_save(foldername, dataset_name, 'classification')
    
    dataset_name = 'val2017'
    datasetname_path = './datasets/%s/%s'%(foldername,dataset_name) # './datasets/NP/val2017'
    txt2json_save(foldername, dataset_name, 'classification')