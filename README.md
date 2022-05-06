# YOLOX - classification

1. 학습/테스트 Dataset 준비
- train2017/, val2017/ 내부에 이미지 있어야 함
- annotations/ 빈 폴더 <- 아래에서 json 만들어줘서 넣어줄 것임.

2. 학습/테스트 Json 파일 생성
- ```python tools/Imgproc_exel2json.py```
- 학습시킬 annotation 유무에 따라 주석 해제(185번줄)
- 결과로 annotations/instances_train2017.json 생성됨

3. Train
- ```python -m yolox.tools.train -n yolox-x -d 1 -b 8 --fp16 -c ./yolox_x.pth```
- ./YOLOX_OUTPUTS 에 결과 저장(best_ckpt.pth, tensorboard log)
- 데이터위치는 ./yolox/data/datasets/coco.py, coco_classes.py 에서 자동으로 불러옴
- 클래스 개수는 ./yolox/exp/yolox_base.py 에서 자동으로 불러옴.

4. Test
```python tools/predict_savetxt_clas_score_box.py image -n yolox-x -c [모델파일 저장된 위치] --path [테스트 할 폴더 위치] --conf [confidence level] --nms 0.45 --tsize 640 -expn [저장할 폴더명] --save_result```
```python tools/predict_savetxt_clas_score_box.py image -n yolox-x -c ./YOLOX_outputs/yolox_x_20220302/best_ckpt.pth --path ./datasets/NP/val2017/ --conf 0.25 --nms 0.45 --tsize 640 -expn np_annotation --save_result```
- -> [저장할 폴더명] 에 box image, result.txt 저장됨

5. Evaluation
- ```python eval.py```
- ```python eval_byclass.py```
- -> eval.py 와 eval_byclass.py 파일 내에 path 부분 수정하여 사용

6. Visualization(필요시)
- ```python vis_overlayImgSave.py```
- Path 수정하여 사용
- GT, pred box overlay 해서 저장
