
import os,shutil

def frm2vid_list(frm_lst,root_folder,output):
    fo=open(frm_lst,'r')
    lines=fo.readlines()
    newline=[]
    with open(output,'w') as fw:
        for lid,line in enumerate(lines):
            line=line.strip().split(' ')
            path=line[0].split('/')[1]+'.avi'
            frm=int(line[1])-1
            newline.append("%s%s %d %s\n"%(root_folder,path,frm,line[2]))
            if frm ==0 and lid !=0:
                newline.pop(-2)
        for nl in newline:    
            fw.write(nl)
    fo.close()

def frm2list(frm_lst,root_folder,output):
    fo=open(frm_lst,'r')
    lines=fo.readlines()
    newline=[]
    with open(output,'w') as fw:
        for lid,line in enumerate(lines):
            frm=int(line.split(' ')[1])-1
            if frm > 240: continue
            newline.append("%s%s"%(root_folder,line)) 
            if frm ==0 and lid !=0:
                newline.pop(-2)
        for nl in newline:    
            fw.write(nl)
    fo.close()
    
def frm2list_sub(frm_lst,root_folder,subset,output):
    fs=open(subset,'r')
    cates=fs.readlines()[0].strip().split(' ')
    fo=open(frm_lst,'r')
    lines=fo.readlines()
    newline=[]
    with open(output,'w') as fw:
        for lid,line in enumerate(lines):
            frm=int(line.split(' ')[1])-1
            print(line.split(' ')[0].split('/')[0])
            if line.split(' ')[0].split('/')[0] not in cates:
                continue
            if frm > 240: continue
            newline.append("%s%s"%(root_folder,line)) 
            if frm ==0 and lid !=2233:# baseballpitch appeare firstly
                #print(lid)
                newline.pop(-2)
        for nl in newline:    
            fw.write(nl)
    fo.close()
    
def getCate(txtfile,output):
    fo = open(txtfile,'r')
    lines =fo.readlines()
    with open (output,'w') as fw:
        for line in lines:
            categ=line.strip().split(' ')[1]
            fw.write(categ+' ')

def mvfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print ("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #
        shutil.move(srcfile,dstfile)          #
        #print ("move %s -> %s"%( srcfile,dstfile))
        
def batchmv(srcdir,dstdir):
    dirs=os.listdir(srcdir)
    dirs.sort()
    #dirs=['HandstandPushups']
    for v_dir in dirs:#YOYO
        srcfiles=os.listdir(os.path.join(srcdir,v_dir))
        srcpath = os.path.join(srcdir,v_dir)
        files=os.listdir(srcpath)
        count=0
        for rel_srcfile in files:#YOYO/v_YoYo
            fpath=os.path.join(srcpath,rel_srcfile)
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            images=os.listdir(os.path.join(srcpath,rel_srcfile))
            for img in images:
                rel_dstpath = "{:s}/{:s}/{:>06d}.jpg".format(v_dir,rel_srcfile,int(img.split('.')[0]))
                rel_srcpath = "{:s}/{:s}/{:s}".format(v_dir,rel_srcfile,img)
                srcfile=os.path.join(srcdir,rel_srcpath)
                dstfile=os.path.join(srcdir,rel_dstpath)##rename by overwrite
                #print(srcfile,dstfile)
                mvfile(srcfile,dstfile)
                count+=1
        print('%d images in %s have been moved'%(count,v_dir))
        
def batchmv_all(srcdir,dstdir):
    dirs=os.listdir(srcdir)
    dirs.sort()
    for v_dir in dirs:#v_YOYO
        srcfiles=os.listdir(os.path.join(srcdir,v_dir))
        srcpath = os.path.join(srcdir,v_dir)
        images=os.listdir(srcpath)
        count=0
#        for rel_srcfile in files:#v_YoYo
#            fpath=os.path.join(srcpath,rel_srcfile)
#            if not os.path.exists(fpath):
#                os.makedirs(fpath)
#            images=os.listdir(os.path.join(srcpath,rel_srcfile))
        for img in images:
            rel_dstpath = "{:s}/{:>06d}.jpg".format(v_dir,int(img.split('.')[0]))
            rel_srcpath = "{:s}/{:s}".format(v_dir,img)
            srcfile=os.path.join(srcdir,rel_srcpath)
            dstfile=os.path.join(srcdir,rel_dstpath)##rename by overwrite
            #print(srcfile,dstfile)
            mvfile(srcfile,dstfile)
            count+=1
        print('%d images in %s have been moved'%(count,v_dir))

if __name__=='__main__':

    set1='train'
    set2='test'
    set=set2
    frm_lst='./%s_01.lst'%set
    root_folder='/home/yangjing/data/C3D/UCF101_frm1/'
    root_folder1='/home/yangjing/data/CDC/THUMOS14/train/img/'
    output='./%s_val.lst'%set
    subset='/home/yangjing/data/CDC/THUMOS14/train/20.txt'
    frm2list_sub(frm_lst,root_folder1,subset,output)
    
    a='/home/yangjing/data/C3D/UCF101_frm/'
    b='/home/yangjing/data/C3D/UCF101_frm1/'
    #batchmv_all(a,a)
    
    filename='/home/yangjing/data/CDC/THUMOS14/train/20act.txt'
    output='/home/yangjing/data/CDC/THUMOS14/train/20.txt'
    #getCate(filename,output)
    
