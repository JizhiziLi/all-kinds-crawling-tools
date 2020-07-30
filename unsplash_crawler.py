import urllib.request
import json
import os
import shutil
import requests
from tqdm import tqdm
from lxml import etree
from imp import reload

def crawl_query_and_save(query_string, save_folder_path):

    main_url = "https://unsplash.com/napi/search/photos?query="+query_string
    main_response = urllib.request.urlopen(main_url)
    main_data = json.loads(main_response.read())
    total_pages = main_data['total_pages']
    total_number = main_data['total']

    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)
    # else:
    #     shutil.rmtree(save_folder_path)
    #     os.makedirs(save_folder_path)

    file = open(save_folder_path+'list.txt',"w+")
    index = 0
    limit = 2000

    for i in range(0, total_pages+1):
        page_url = main_url+"&xp=&per_page=20&page="+str(i)
        page_response = urllib.request.urlopen(page_url)
        page_data = json.loads(page_response.read())

        for j in range(len(page_data['results'])):
            index += 1
            if index>limit:
                return
            image_id = page_data['results'][j]['id']+'.jpg'
            image_url = page_data['results'][j]['urls']['full']
            print(f'[{index}/{total_number}]: {image_id}')
            file.write(f"{image_url}\n")
            
            # image_url = image_url+'?format=jpg&fit=crop&w=1080&h=1080'
            # image_url = image_url+'?format=jpg&fit=crop&w=1080'

            with open(save_folder_path + image_id, 'wb') as f:
                try:
                    f.write(requests.get(image_url).content)
                    f.close()
                except:
                    print(f'Error: {index}')


def crawl_collection_and_save(collection_id, save_folder_path):


    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    file = open(save_folder_path+'collection_list.txt',"w+")
    index = 0

    main_url = "https://unsplash.com/napi/collections/"+str(collection_id)+'/'
    main_response = urllib.request.urlopen(main_url)
    main_data = json.loads(main_response.read())
    total_number = main_data['total_photos']
    total_pages = int(total_number/30)+1
    
    for i in range(0, total_pages+1):
        page_url = main_url+"photos?per_page=30&page="+str(i)
        page_response = urllib.request.urlopen(page_url)
        page_data = json.loads(page_response.read())

        for j in range(len(page_data)):
            index+=1
            image_id = page_data[j]['id']+'.jpg'
            image_url = page_data[j]['urls']['full']
            print(f'[{index}/{total_number}]: {image_id}')
            file.write(f"{image_url}\n")


            with open(save_folder_path + image_id, 'wb') as f:
                try:
                    f.write(requests.get(image_url).content)
                    f.close()
                except:
                    print(f'Error: {index}')




def set_header(url, user_agent):

    headers = {"User-Agent": user_agent}
    try:
        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            return req.text.encode('utf8')
        else:
            return ''
    except Exception as e:
        print(e)



def get_download_link_from_photo_id(photo_id):
    
    user_agent = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/65.0.3325.181 Safari/537.36'
    page_url = "https://unsplash.com/photos/"+photo_id

    html = set_header(page_url,user_agent)
    selector = etree.HTML(html)

    try:
        for url in selector.xpath('//img/@src'):
            url_split = url.split()[0]
            if url_split.find('photo')>0:
                img_url = url_split[:url_split.find('?')]
                print(img_url)
                return img_url
    except:
        print(f'*****Error: not exist {photo_id}')
        # url = "https://static." + url.split("images.")[1].split("?")[0]
        # print(url)

def get_download_link_for_txt(txt_file):
    file = open(txt_file, 'r')
    for line in file:
        photo_id = line[:line.find('\n')]
        get_download_link_from_photo_id(photo_id)



if __name__ == '__main__':

    
    query_string = 'antelope'
    save_folder_path = '/save/path/'

    ###############
    # Crawl query
    
    print(f'Crawl category: {query_string}')
    crawl_query_and_save(query_string, save_folder_path)


    ################
    # Crawl collection
    # collection_id = 1358076
    # crawl_collection_and_save(collection_id, save_folder_path)

    ################
    # Crawl url
    # photo_id = '-BC-LrasMKY'
    # get_download_link_from_photo_id(photo_id)
    # txt_file = '/save/txt.txt'
    # get_download_link_for_txt(txt_file)

