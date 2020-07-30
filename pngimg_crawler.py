#!/usr/bin/python
# _*_ coding:utf _*_

import os
import os.path
import requests
from lxml import etree
from imp import reload
from PIL import Image



def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)



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



def crawl_and_save(save_folder_path):

    create_folder_if_not_exist(save_folder_path)


    user_agent = 'Mozilla/5.0 AppleWebKit/537.36 Chrome/65.0.3325.181 Safari/537.36'
    url = 'http://pngimg.com/imgs/'
    main_url = 'http://pngimg.com/'
    html = set_header(url,user_agent)
    selector = etree.HTML(html)
    name_list = []
    pdf_list = []

    index = 0
    for category_url in selector.xpath('//tr/td/a/@href'):
        if category_url != '/' and category_url !='alphabet/':
            print(category_url)
            save_category = save_folder_path+category_url
            create_folder_if_not_exist(save_category)
            
            sub1_url = url+category_url
            sub1_html = set_header(sub1_url,user_agent)
            sub1_selector = etree.HTML(sub1_html)
            print('------------')
            class_name = category_url[:-1]
            print(f'Crawl class: {class_name}')
            for sub1_category in sub1_selector.xpath('//div[@class="png_png"]/a/@href'):
                
                sub_class_name = sub1_category[sub1_category.rfind('/')+1:]
                print(f'Crawl sub-class: {sub_class_name}')
                save_category2 = save_folder_path+sub1_category[5:]
                
                create_folder_if_not_exist(save_category2)
                sub2_url = url+sub1_category[5:]
                sub2_html = set_header(sub2_url,user_agent)
                sub2_selector = etree.HTML(sub2_html)

                for sub2_category in sub2_selector.xpath('//div[@class="png_png png_imgs"]/a/@href'):
                    
                    create_folder_if_not_exist(save_category2+'/png/')
                    create_folder_if_not_exist(save_category2+'/alpha/')
                    sub3_url = 'https:'+sub2_category
                    sub3_html = set_header(sub3_url,user_agent)
                    sub3_selector = etree.HTML(sub3_html)

                    for sub3_category in sub3_selector.xpath('//div[@class="png_big"]/a/@href'):
                        img_url = 'https://pngimg.com'+sub3_category
                        img_name = sub3_category[sub3_category.rfind('/')+1:]
                        

                        with open(save_category2+'/png/'+img_name, 'wb') as f:
                            try:
                                f.write(requests.get(img_url).content)
                                f.close()
                            except Exception as e:
                                print(f'Error when saving png: {str(e)}')

                        try:
                            img = Image.open(save_category2+'/png/'+img_name)
                            red, green, blue, alpha = img.split()
                            alpha.save(save_category2+'/alpha/'+img_name)
                        except Exception as e:
                            print(f'Error when extracting alpha: {str(e)}')





if __name__ == "__main__":

    save_folder_path = '/save/path/'
    crawl_and_save(save_folder_path)

    