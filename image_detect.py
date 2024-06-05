import cv2
from ultralytics import YOLO
import requests 
import torch
import requests



#トークンを設定
token = 'SmKI9F8ABC5Wl1M2sl23mYJFKSjmMBAzXtfRonvp4Kj' #発行されたトークンをここにコピペ


#学習済みモデル
model =YOLO('/Users/suzukamichiyo/iot2024/last.pt')

#カメラ起動
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Don't open camera")
    exit()


#Lineに通知を送る
def send_line(msg):

    #サーバーに送るパラメータを用意
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + token}
    payload = {'message': msg}
    #requestsモジュールのpost関数を利用してメッセージを送信する
    #ヘッダにトークン情報，パラメータにメッセージを指定する
    requests.post(url, headers=headers, params=payload)


while True:

    #キャプチャ
    ret, frame = cap.read()

    if not ret:
        print("Don't get frame. exit")
        break

    #モデルにカメラのフレームを渡す
    results = model(frame)
    print("^^^^^^^^^^^^^^^")

    #カメラのフレームのクラス分類時に割り当てた数字をtensor_valueに代入．
    # resultに関してはhttps://docs.ultralytics.com/ja/reference/engine/results/を参考にしてください．
    for result in results:
        tensor_value = result.boxes.cls
    

    img_annotated = results[0].plot()


    #classes.txtの0が"water_close"であるため，tensor_value==0と設定
    if (tensor_value == 0.).all():
          send_line('水の栓が閉まっています')
          print('close')

    #classes.txtの1が"water_open"であるため，tensor_value==1と設定
    elif (tensor_value == 1.).all():
          send_line('水の栓が開いています')
          print('open')

    else:
         pass
         


    cv2.imshow('Camera', img_annotated)

    if cv2.waitKey(1) == ord('q'):  # qキーで終了
        break


cap.release()
cv2.destroyAllWindows()


# """
# CLOSE
#  [[ 73  98 112]
#   [ 73  97 111]
#   [ 74  97 111]
#   ...
#   [ 77  96 107]
#   [ 76  94 107]
#   [ 77  95 108]]

#  [[ 73  98 112]
#   [ 73  97 111]
#   [ 73  96 110]
#   ...
#   [ 79  97 108]
#   [ 77  96 108]

#   OPEN
#  [[ 82  97 112]
#   [ 83  98 113]
#   [ 84  99 114]
#   ...
#   [ 93 110 121]
#   [ 93 110 121]
#   [ 94 111 122]]

#  [[ 82  97 112]
#   [ 83  98 114]
#   [ 84  99 115]
#   ...
#   [ 94 111 122]
#   [ 94 111 122]
#   [ 94 111 122]]]


# """


# from ultralytics import YOLO
# import cv2

# # Load a model
# model = YOLO('/Users/suzukamichiyo/iot2024/last.pt')  # pretrained YOLOv8n model

# cap = cv2.VideoCapture(0)

# if not cap.isOpened():
#     print("Don't open camera")
#     exit()


# while True:
#     ret, frame = cap.read()

#     if not ret:
#         print("Don't get frame. exit")
#         break

#     #モデルにカメラのフレームを渡す
#     results = model(frame)

#     # Process results list
#     for result in results:
#         boxes = result.boxes  # Boxes object for bounding box outputs
#         masks = result.masks  # Masks object for segmentation masks outputs
#         keypoints = result.keypoints  # Keypoints object for pose outputs
#         probs = result.probs  # Probs object for classification outputs
#         print("probs")
#         print(probs)


#PythonのHTTP通信ライブラリをimport
# import requests 

# #トークンを設定
# token = 'ここに発行されたトークンをコピペしてください' #発行されたトークンをここにコピペ


# #Lineにメッセージを送れるか検証
# def send_line(msg):

#     #サーバーに送るパラメータを用意
#     url = 'https://notify-api.line.me/api/notify'
#     headers = {'Authorization': 'Bearer ' + token}
#     payload = {'message': msg}

#     #requestsモジュールのpost関数を利用してメッセージを送信する
#     #ヘッダにトークン情報，パラメータにメッセージを指定する
#     requests.post(url, headers=headers, params=payload)

# if __name__ == '__main__':

#     #メッセージを送信
#     send_line('Hello, world!')

