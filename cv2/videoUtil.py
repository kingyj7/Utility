import os
import cv2
import numpy as np

## ================VIDEO RELATED============    
def extract_frames(video_path, dst_folder,EXTRACT_FREQUENCY=1):
    '''
    EXTRACT_FREQUENCY: sample rate
    '''
    print('open %s' % video_path)
    
    video = cv2.VideoCapture()
    index = 1
    if not video.open(video_path):
        print("can not open the video")
        exit(1)
    count = 1
    while True:
        _, frame = video.read()
        if frame is None:
            break
        if count % EXTRACT_FREQUENCY == 0:
            save_path = "{}/{:>06d}.jpg".format(dst_folder, index)
            cv2.imwrite(save_path, frame)
            index += 1
        count += 1
    video.release()

    print("{} Totally save {:d} pics".format(os.path.basename(video_path), index - 1))


def extract_from_folder(VIDEO_DIR,EXTRACT_DIR,EXTRACT_FREQUENCY=1):
    '''
    EXTRACT_FREQUENCY: sample rate
    '''
    import shutil
    
    videos = os.listdir(VIDEO_DIR)
    for video in videos:
        if os.path.splitext(video)[1] != '.mp4':
            continue
        video_path = os.path.join(VIDEO_DIR, video)
        modi_name = os.path.basename(VIDEO_DIR)+'_'+video.split('.')[0]
        extract_folder = os.path.join(EXTRACT_DIR, modi_name)
        try:
            shutil.rmtree(extract_folder)
        except OSError:
            pass

        os.mkdir(extract_folder)
        extract_frames(video_path, extract_folder,EXTRACT_FREQUENCY)

if __name__ == '__main__':
    video_dir = '/home/data/wangjunchu/Projects/count_repeat_times/For_Yang/demo_v4_S/data/'
    video_name  = 'WIN_20200512_14_35_14_Pro_3.mp4'
    video_path = os.path.join(video_dir,video_name)
    dst_folder = '/home/data/wangjunchu/Projects/count_repeat_times/For_Yang/demo_v4_S/data/image'
    #EXTRACT_FREQUENCY = 1
    extract_frames(video_path, dst_folder)
    
