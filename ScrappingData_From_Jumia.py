import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


babies = 'https://www.jumia.com.eg/mlp-free-shipping/baby-products/?page=' 

mens_bags = 'https://www.jumia.com.eg/bags/?page='       

Beauty_health = 'https://www.jumia.com.eg/body-skin-care/?page='        

labtops = 'https://www.jumia.com.eg/laptops/?page='       

Smart_phones = 'https://www.jumia.com.eg/smartphones/?page='    

types = [babies, mens_bags]   # You can add the other products but i will check code on these 2 product types.

def Getting_Data(product_types):
    # Making a folder to save images
    folder_name = 'Images'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    li = []
        
    for product_type in product_types:
        url = product_type
        print(f"\n{'*' * 10}  Products of {url.split('/')[-2]}  {'*' * 10}\n")
        
        Number_of_pages = 1  # getting data from 1 page of each type of products. You can edit it.
        
        for i in range(1, Number_of_pages + 1):  
            response = requests.get(url + str(i))
            soup = BeautifulSoup(response.content, 'lxml')
            data = soup.find('div', {'class': '-paxs row _no-g _4cl-3cm-shs'})
            products = data.find_all('article', {'class': 'prd _fb col c-prd'})
            
            for pr in products: 
            
                title = pr.find('a').find('div', {'class': 'info'}).find('h3').text
                imgLink   = pr.find('a').find('div', {'class': 'img-c'}).find('img', {'class': 'img'})['data-src']
                price = float(pr.find('a').find('div', {'class': 'info'}).find('div', {'class': 'prc'}).text.split()[1].replace(',', ''))
                brand = pr.find('a')['data-brand']
                tags  = pr.find('a')['data-category'].split('/')
                
                # # if we need to add the original scrapped ratings.
                # rating = float(pr.find('a').find('div', {'class': 'info'}).find('div', {'class': 'rev'}).text.split()[0])
                # no_of_rev  = int(pr.find('a').find('div', {'class': 'info'}).find('div', {'class': 'rev'}).text.split()[-1][2:4])
                
                img_data = requests.get(imgLink).content
                try:
                    # path of saving photos
                    path_ = r"{}.jpg".format(os.path.join(folder_name, f"{title.split('-')[0].strip().split('/')[0]}")) 
                    print('>>>>', title)
                    
                    # saving photos in the last path.
                    with open(path_, mode='wb') as handler:
                        handler.write(img_data)
                    
                    li.append(
                        {
                            'Product Name': title,
                            'Price': price,
                            'Brand': brand,
                            'Category': tags[0],
                            'Tags': tags,
                            'Image Link': imgLink,
                            'Total_rate': 1,   # Default value.
                            'Count_of_ratings': 1,
                        }
                )
                
                except:   # if there are any not allowed symbol in the title to use in the path. 
                    continue
                

    print('=' * 50)
    
    return li

def Scrapper():
    Scrapped_Products = Getting_Data(types)
    return Scrapped_Products


def Storing_Data(Data, file_name):
    # making dataframe from the Data we get.
    df = pd.DataFrame(Data, columns=['Product Name', 'Price', 'Brand', 'Category', 'Tags', 'Image Link' 'Total_rate', 'Count_of_ratings'])
    
    # making folder to save the csv file.
    folder_name = 'Scrapped Data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    
    # saving data 'DataFrame' to a csv file.
    with open(os.path.join(folder_name, file_name + '.csv'), 'w', newline='') as file:
        df.to_csv(file, index=False, line_terminator='')
        
if __name__ == "__main__":
    Data = Scrapper()
    Storing_Data(Data, 'Scrapped_Data_For_EcommerceWebsite')