import os, cv2, json

path1='./YOLOX_outputs/yolox_x_erosion/vis_res/2022_04_15_07_53_31/'
path2='./datasets/Erosion2/annotations/instances_val2017.json'

with open(path2, 'r') as f:
    data = json.load(f)

for i in range(len(data['images'])):
    try:
        print(i,'/',len(data['images']))
        filename = data['images'][i]['file_name']
        img_id = data['images'][i]['id']
        img=cv2.imread(path1+filename)
        #img2=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2=img

        for j in range(len(data['annotations'])):

            img_id2 = data['annotations'][j]['image_id']
            if img_id ==img_id2 :

                bbox=data['annotations'][j]['bbox']
                x1=bbox[0]
                y1=bbox[1]
                x2=bbox[0]+bbox[2]
                y2=bbox[1]+bbox[3]

                cv2.rectangle(img2, (x1,y1), (x2,y2), (0,0,255),2)

                savepath = './YOLOX_outputs/yolox_x_erosion/vis_res/overlay/'
                if os.path.isdir(savepath)==False:
                    os.mkdir(savepath)
                cv2.imwrite(savepath +filename, img2)
#                 plt.figure(figsize=(10,10,))
#                 plt.imshow(img2)
#                 plt.axis('off')
#                 plt.show()
                
    except:
        print('ERROR===================================', i,'/',len(data['images']))