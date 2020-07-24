import numpy as np
import cv2
import collections

#====================
def CC2_judge_in_conts(cont_area,cont_pts,dist_thr):

    #filter to retain 2 contour
    order_area = sorted(cont_area,reverse=True)
    id1 = cont_area.index(order_area[0])
    id2 = cont_area.index(order_area[1])

    cont1,cont2=np.array(cont_pts[id1]),np.array(cont_pts[id2])

    #2.compute the smallest center distance
    center1,center2 = np.mean(cont1),np.mean(cont2)
    #print(center1,center2)
    dist = np.linalg.norm(center1-center2)

    if dist> dist_thr:
        # print('CC dist: %.1f'%dist)
        return True
    else:
        return False

def CC_judge(*mask,nohands_pixel_thr=None,two_part_thr=None,dist_thr=None):
    '''

    :param mask1:
    :param mask2:
    :param nohands_pixel_thr:
    :param two_part_thr:
    :return: if hands_flag is False(small hands or no hands),
            then CC2_flag must be False(won't detect CC), too
    '''
    
    #print(mask)
    
    if len(mask) == 2:
        mask1,mask2 = mask
    else:  
        mask1 = mask[0]
         
    hands_flag1 = False
    CC2_flag1 = False
    
    if np.sum(mask1) > nohands_pixel_thr:
        hands_flag1 = True

    if hands_flag1:
        ## different opencv-3.4.1 will show too many values to unpack (expected 2)
        try:
            contours,hierarchy = cv2.findContours(mask1.astype(np.uint8),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        except:
            _,contours, hierarchy = cv2.findContours(mask1.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cont_area = []
        cont_pts = []
        for cid, contour in enumerate(contours):
            area = cv2.contourArea(contour)

            if area > two_part_thr:
                cont_area.append(area)
                cont_pts.append(contour)


        if len(cont_area) < 2:# make sure num_cc ==0 won't happen
            CC2_flag1 = False
        else:
            CC2_flag1 = CC2_judge_in_conts(cont_area,cont_pts,dist_thr)
    
    if len(mask) == 2:
        hands_flag2 = False
        CC2_flag2 = False
        
        if np.sum(mask2) > nohands_pixel_thr:
            hands_flag2 = True
        
        if hands_flag2:
            contours, hierarchy = cv2.findContours(mask2.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
            cont_area = []
            cont_pts = []
            for cid, contour in enumerate(contours):
                area = cv2.contourArea(contour)
    
                if area > two_part_thr:
                    cont_area.append(area)
                    cont_pts.append(contour)
    
            if len(cont_area) < 2:  # make sure num_cc ==0 won't happen
                CC2_flag2 = False
            elif len(cont_area) == 2:
                CC2_flag2 = True
            else:
                CC2_flag2 = CC2_judge_in_conts(cont_area, cont_pts,dist_thr)

        return hands_flag1,hands_flag2,CC2_flag1,CC2_flag2
        
    else:
        
        return hands_flag1,CC2_flag1


#===========
def get4ColorList():
    color_dict = collections.OrderedDict()

    #gray
    lower_gray = np.array([0, 0, 46])
    upper_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(upper_gray)
    color_dict['gray']=color_list

    #red
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    color_dict['red'] = color_list

    #red2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    color_dict['red2'] = color_list

    #orange
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    color_dict['orange'] = color_list

    return color_dict

def color_feat_cal(mask,maskRGB,color_dict):
    '''
    extract HSV color in image
    '''
    
    def cal_mask_area(binary):
        # mask must be binary
        return binary.shape[0] * binary.shape[1] - np.sum(binary == 0)

    #1.calculate pixel area of hand region
    hand_area = cal_mask_area(mask)

    hsv = cv2.cvtColor(maskRGB, cv2.COLOR_BGR2HSV)
    color_scores = []

    #2.extract 4 main color
    for idx, d in enumerate(color_dict):  # in order [gray,red,red2,orange]
        sub_mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        area_score = cal_mask_area(sub_mask) / hand_area
        color_scores.append(area_score)

        #self.colors_area_dict[d].append(area_score)

    #3. calculate ratio,generate feature vector,where red and red2 are merged
    color_scores = [color_scores[0], color_scores[1] + color_scores[2], color_scores[3]]

    return color_scores

def my_boundingRect(mask,debug=False):
    '''
    return the enclosing_rectangle,given a mask
    '''
    
    mask = mask.astype(np.uint8)
    src_size = mask.shape
    area_thr = [src_size[0] * src_size[1] // 50, src_size[0] * src_size[1] // 3]

    target_box = 4*[0,]
    target_contour = []
    max_area = 0

    _, contours,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for cid, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        if area > max_area and area_thr[1]>area>area_thr[0]:
            max_area = area
            target_contour.append(contour)
    
    if len(target_contour) == 0:
        return target_box
        
    output = cv2.boundingRect(target_contour[0])
    
    if 1:
        cv2.rectangle(mask, (output[0],output[1]),(output[0]+output[2],output[1]+output[3]), (255, 255, 255), 2, 8, 0)
        cv2.imshow('1',mask)
        cv2.waitKey(10000)
        exit()
    return output
 
