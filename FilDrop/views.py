from django.shortcuts import render,redirect
from FilDrop.models import *
import os
from API_KEYS.keys import keys
from pathlib import Path
from utility.nftstorage import NftStorage
import json
import shutil
from pathlib2 import Path as Path2_
import requests
base_uri = "ipfs://"
NFTSTORAGE_API_KEY = keys['NFTSTORAGE']
PINATA_JWT = keys['PINATA']


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
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        print(WalletAddress)
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
    data=[]
    try:
        usercollection_objects=UserCollection.objects.filter(user=user)
        for i in usercollection_objects:
            temp = []
            for j in range(i.collection_count):
                temp.append(i.collection_hash)

            data.append([i.collection_name,i.collection_hash,temp])

        # for i in range(len(usercollection_objects)):
        #     print('i---'+str(i))
        #     for j in range(i.collection_count):
        #         temp = []
        #         print('j---'+str(j))
        #         temp.append('https://ipfs.io/ipfs/'+ usercollection_objects[i][j][collection_hash]+str(j))
        #         data.append(temp)
                
    except:
        print('fuk')
        usercollection_objects = None

    print('Hello world dta')
    print(data)
    print(usercollection_objects)
    print(type(usercollection_objects))
    return render(request,'userpage.html',{'WalletAddress':WalletAddress,'usercollection_objects':usercollection_objects,'data':data})

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

    path =Path(os.path.normpath( str(BASE_DIR) + '/'+ str(user.id) + '/'+str(usercollection_obj.collection_name)+'/metadata/'))
    print(path)
    path_images =Path(os.path.normpath( str(BASE_DIR) + '/'+ str(user.id) + '/'+str(usercollection_obj.collection_name)+'/images/'))


    try:
        Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(e)
    
    count_image=0
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
    print('LISTSTSTST----------------------------------------------------------------------')
    print(img_file_list)
 
    cid = c.upload(img_file_list, 'image/png')
    usercollection_obj = UserCollection.objects.get(id=pkk)
    usercollection_obj.collection_hash=cid
    usercollection_obj.is_active=False
    usercollection_obj.collection_count=image_count
    usercollection_obj.save()
    print(cid)
    img_file_list.clear()
    user_id = str(user.id)
    try:
        shutil.rmtree(user_id)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


    return redirect('userpage')



def Deploy(request,collectionname):
    path =Path(os.path.normpath( str(BASE_DIR) +'/NFT.sol'))
    path2 =Path(os.path.normpath( str(BASE_DIR) +'/contracts/NFT.sol'))
    WalletAddress = request.session['WalletAddress']
    print(WalletAddress)



    user = User.objects.get(WalletAddress=WalletAddress)
    obj = UserCollection.objects.get(collection_name=collectionname,user=user)
    print(obj.collection_hash)
    shutil.copyfile(path,path2)
    file = Path2_(path2)
    data = file.read_text()
    data = data.replace("USER_ADDRESS", WalletAddress)
    file.write_text(data)
    



    file = Path2_(path2)
    data = file.read_text()
    data = data.replace("TOKENURI", str("https://ipfs.io/ipfs/")+str(obj.collection_hash))
    file.write_text(data)
    #https://mumbai.polygonscan.com/tx/0xec4fb2c38a2cee48c6019c009c0866850d793533e5511d96ab3ece421a67fc2b

    try:
        shutil.rmtree("contracts/artifacts")
        shutil.rmtree("contracts/cache")
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))


    os.system("npx hardhat run scripts/deploy.js --network mumbai")


    q = open('address.txt','r')
    pqrq=q.read()
    print(pqrq)
    
    deployed_url = "https://mumbai.polygonscan.com/tx/"+str(pqrq)
    print('xxxxxxxxxxxxxxxxxxx')
    print(deployed_url)

    return render(request,'deploy.html',{'response':deployed_url})




    # url = "https://api.nftport.xyz/v0/contracts"
    # payload = "{\n  \"chain\": \"polygon\",\n  \"name\": \"CRYPTOPUNKS\",\n  \"symbol\": \"CYBER\",\n  \"owner_address\":wallet,\n  \"metadata_updatable\": false,\n  \"type\": \"erc721\"\n}"
    

    # payload = payload.replace('CRYPTOPUNKS',"NFTGEN")
    # payload = payload.replace('CYBER',"MATIC")
    # payload = payload.replace('wallet','"'+WalletAddress+'"')

    # headers = {
    #     'Content-Type': "application/json",
    #     'Authorization': "4c658b59-2263-4cb8-a3c4-dacca73e4700"
    # }

    # response = requests.request("POST", url, data=payload, headers=headers)
    # #print(response.text)
    # print('--------------------')
    # print(response)





    




# full_path = os.path.normpath(str(BASE_DIR)+str('/')+str(pkk)+"/images/"+str(usercollection_obj.collection_name))
############################################################
# metadata_path = os.path.normpath(str(BASE_DIR)+str('/')+str(pkk)+str(usercollection_obj.collection_name)+'/metadata//')
