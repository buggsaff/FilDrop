from django.shortcuts import render,redirect
from FilDrop.models import *
import os
from API_KEYS.keys import keys
from pathlib import Path
from utility.nftstorage import NftStorage
import json

#global Keys
base_uri = "ipfs://"
NFTSTORAGE_API_KEY = keys['NFTSTORAGE']
PINATA_JWT = keys['PINATA']

#project_name= "Test_Pro"

img_file_list = [] 
meta_file_list = []
gen_imgs = {}

user_d = {}


# Create your views here.
def Home(request):
    
    return render(request,'home.html')


def Login(request):
    request.session['WalletAddress'] = "xxx"
    if request.POST:
        WalletAddress = request.POST.get('WalletAddress')
        request.session['WalletAddress'] = WalletAddress
        obj = User.objects.get_or_create(WalletAddress=WalletAddress)
        return redirect('userpage')
    else:
        return redirect('home')

def AddCollection(request):
    WalletAddress = request.session['WalletAddress']
    print('Collection')
    print(WalletAddress)
    if request.POST:
        user = User.objects.get(WalletAddress=WalletAddress)
        collection_name = request.POST.get('collection-item')
        obj = UserCollection.objects.get_or_create(user=user,collection_name=collection_name)

    return redirect('userpage')

def UserPage(request):
    WalletAddress = request.session['WalletAddress']
    user = User.objects.get(WalletAddress=WalletAddress)
    usercollection_objects=None
    try:
        usercollection_objects=UserCollection.objects.filter(user=user)
    except:
        usercollection_objects = None

    try:
        user_c_img = UserCollectionImage.objects.filter(user=user)
    except:
        user_c_img = None

    return render(request,'userpage.html',{'WalletAddress':WalletAddress,'usercollection_objects':usercollection_objects,'user_c_img':user_c_img})

def update_meta_cid(file, cid):
    for i in file:
        with open(i) as f:
             data = json.load(f)
             img_file = data['image'].replace(base_uri, '')
             data['image'] = base_uri + cid + '/' + img_file
        
        with open(i, 'w') as outfile:
            json.dump(data, outfile, indent=4)    


def ImageUpload(request,pkk):
    global gen_imgs
    global user_d
    global img_file_list
    files = request.FILES.getlist('allimages')
    WalletAddress = request.session['WalletAddress']
    usercollection_obj = UserCollection.objects.get(id=pkk)
    meta_file_list = []
    user = User.objects.get(WalletAddress=WalletAddress)
    # full_path = os.path.normpath(str(BASE_DIR)+str('/')+str(pkk)+"/images/"+str(usercollection_obj.collection_name))
    ############################################################
    metadata_path = os.path.normpath(str(BASE_DIR)+str('/')+str(pkk)+str(usercollection_obj.collection_name)+'/metadata//')
    print(pkk)

    path =Path(os.path.normpath( str(BASE_DIR) + '/'+ str(pkk) + '/'+str(usercollection_obj.collection_name)+'/metadata/'))
    print(path)
    path_images =Path(os.path.normpath( str(BASE_DIR) + '/'+ str(pkk) + '/'+str(usercollection_obj.collection_name)+'/images/'))


    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)
    

    ############
    images = {}
    image_count = 0
    for f in files:
        a = UserCollectionImage.objects.get_or_create(usercollection=usercollection_obj,image=f,user=user)

    i=1
    for filename in os.listdir(path_images):
        os.rename(os.path.join(path_images,filename),os.path.join(path_images,str(i)+'.jpg'))
        i+=1
    
    for filename in os.listdir(path_images):
        img_file_list.append(str(Path(os.path.normpath(str(path_images)+'\\'+str(filename)))))
    
    print('-----------------------------')
    print(img_file_list)


    for k in img_file_list:
        image_count +=1
        token = {
            "name": str(usercollection_obj.collection_name) + ' ' + str(image_count),
            "image": base_uri + str(image_count),
            "desc": "Hello World"
        }
        meta_file =   Path(str(path)+'/' + str(image_count) + '.json')
        meta_file_list.append(meta_file)
        print(meta_file)

        with open(meta_file, 'w') as outfile:
            json.dump(token, outfile, indent=4)
    
    nstorage = {}
    c = NftStorage(NFTSTORAGE_API_KEY)
    cid = c.upload(img_file_list, 'image/png')
    usercollection_obj = UserCollection.objects.get(id=pkk)
    usercollection_obj.collection_hash=cid
    usercollection_obj.is_active=False
    usercollection_obj.save()
    print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    print(cid)


    return redirect('userpage')
