"""
Extract all the relevant info from reviews of a given site. 
Directory Structure : ./data/ -> this folder contains all the folders (g2691262,g4141 etc) 
                      ./extracted_info/ -> the created jsons (one for all reviews of a site) will be saved here
Change the paths accordingly in the indicated lines(total 5)
The folders are always iterated in fixed order, the script can be resumed from the same folder incase it stops by changing the folders loop
"""
from bs4 import BeautifulSoup
import re
import os
import time
from tqdm import tqdm as tqdm
import json

############################ Change the path:1 ############################ 
folders = os.listdir('./data/')

############################ Change the path:2 ############################ 
folders = [f for f in folders if os.path.isdir(os.path.join(os.getcwd(),'data',f))]

folders = sorted(folders)


############################ Change to resume the script from a different file ############################
for i in range(len(folders)):
    folder = folders[i]
    review_data = {}

    ############################ Change the path:3 ############################ 
    files = os.listdir('./data/'+folder)
    print(str(i)+":"+folder)
    for file in tqdm(files):

        ############################ Change the path:4 ############################ 
        soup = BeautifulSoup(open('./data/'+folder+'/'+file), 'html.parser')


        reviews = soup.findAll('div',attrs={'class':'location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw'})
        try:
            if len(reviews) > 0:
    #             print(file,len(reviews))
                for review in reviews:
                    user_name = review.find('a',attrs={'class':'ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC'})
                    loc = review.find('span',attrs={'class':'default social-member-common-MemberHometown__hometown--3kM9S small'})
                    rating = review.find('span',\
                                    attrs={'class':re.compile('ui_bubble_rating bubble_[0-9]+')})['class'][-1].split('_')[-1]
                    text = (review.find('q')).find('span')
                    title_link = review.find('a',attrs={'class':'location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT'},href=True)
                    title = title_link.find('span')
                    date = review.find('span',attrs={'class':'location-review-review-list-parts-EventDate__event_date--1epHa'})
                    info = title_link['href'].split('-')
                    
                    code = info[1] + "-" + info[2] + "-" + info[3]
                    review_data[code] = {}
                    if user_name != None:
                        review_data[code]['user_name'] = user_name.text
                    if loc != None:
                        review_data[code]['user_loc'] = loc.text
                    if rating != None:
                        review_data[code]['rating'] = rating
                    if title != None:
                        review_data[code]['title'] = title.text
                    if text != None:
                        new_text = re.sub(r'([\?\(\)])',r'\\\1',text.text)
                        full_text = re.findall(new_text[0:15]+'.+\",',str(soup))
                        if len(full_text)>0:
                            review_data[code]['text'] = full_text[0].split('\"')[0]
                        else:
                            review_data[code]['text'] = text.text
                    if date != None:
                        review_data[code]['exp_date'] = (date.text).split(":")[-1]
            #         print(code)
            else:
                reviews = soup.findAll('div',attrs={'class':'review-container'})
    #             print(file,len(reviews))
                for review in reviews:
                    user_info = review.find('div',attrs={'class':'info_text'})
                    data = {}
                    rating = review.find('span',attrs={'class':re.compile('ui_bubble_rating bubble_[0-9]+')})['class'][-1].split('_')[-1]
                    user_name = user_info.find('div')
                    loc = user_info.find('strong')
                    title = review.find('span',attrs={'class':'noQuotes'})
                    text = review.find('p',attrs={'class':'partial_entry'})
                    date = review.find('div',attrs={'class':'prw_rup prw_reviews_stay_date_hsx'})
                    info = review.find('a',attrs={'class':'title '},href=True)['href'].split("-")
            
                    code = info[1] + "-" + info[2] + "-" + info[3]
                    review_data[code] = {}
                    if user_name != None:
                        review_data[code]['user_name'] = user_name.text
                    if loc != None:
                        review_data[code]['user_loc'] = loc.text
                    if rating != None:
                        review_data[code]['rating'] = rating
                    if title != None:
                        review_data[code]['title'] = title.text
                    # if text != None:
                    #     review_data[code]['text'] = text.text
                    if text != None:
                        new_text = re.sub(r'([\?\(\)])',r'\\\1',text.text)
                        full_text = re.findall(new_text[0:15]+'.+\",',str(soup))
                        if len(full_text)>0:
                            review_data[code]['text'] = full_text[0].split('\"')[0]
                        else:
                            review_data[code]['text'] = text.text
                    if date != None:
                        review_data[code]['exp_date'] = (date.text).split(":")[-1]
        except Exception as e:
            print('err: ',file)
            # print(e)

    ############################ Change the path:5 ############################ 
    with open('./extracted_data/'+folder+'.json','w') as fil:
        json.dump(review_data,fil)
