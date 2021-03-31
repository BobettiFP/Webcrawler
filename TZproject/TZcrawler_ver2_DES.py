#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
from urllib import parse
import pandas as pd
import time
import openpyxl
import requests

webpages = ["https://necta.go.tz/results/2015/psle/results/distr_0201.htm",
            "https://necta.go.tz/results/2015/psle/results/distr_0202.htm",
            "https://necta.go.tz/results/2015/psle/results/distr_0203.htm",
            "https://necta.go.tz/results/2015/psle/results/distr_0204.htm",
            "https://necta.go.tz/results/2015/psle/results/distr_0205.htm",
            "https://necta.go.tz/results/2015/psle/results/distr_0206.htm"]          
districts = ["Ilala(V)","Ilala(M)","Kinondoni","Ubungo","Kigamboni","Temeke"]

 
def get_address(url):
    region_link = requests.get(url)
    soup = BeautifulSoup(region_link.content, "html.parser")
    links_with_text = []
    for a in soup.find_all('a', href=True): 
        if a.text: 
            links_with_text.append(a['href'])
    address = []
    for i in links_with_text:
        ###################년도확인#######################
        address.append("https://necta.go.tz/results/2015/psle/results/"+i)
        
    return address

def file_creator(webpage, district):
    ######################지역확인###############
    region = 'Dar es salaam'
    soup = requests.get(webpage, timeout = 10)
    webpage2 = requests.get(webpage, timeout = 10)
    soup = BeautifulSoup(webpage2.content, "html.parser")
    text = soup.get_text()

    contents = []
    for row in text:
        contents.append(row)
        text_in_page = "".join(contents)
    

    school_name = text_in_page.split("\n")[7][:text_in_page.split("\n")[7].rfind("-")]
    print(school_name)
    school_id = text_in_page.split("\n")[7][text_in_page.split("\n")[7].rfind("-")+2:-1]
    print(school_id)
    res_loc = text_in_page.find('PSLE')
    results = text_in_page[res_loc:res_loc+4]
    year = text_in_page[res_loc+5:res_loc+9]
    
    loc = text_in_page.find('MTIHANI')
    school_examiner = text_in_page[loc+10:loc+12].strip()
    loc2 = text_in_page.find("WASTANI WA SHULE")
    school_average = text_in_page[loc2+21:loc2+29]
    loc3 = text_in_page.find("KUNDI LA SHULE")
    school_group = text_in_page[loc3+17:loc3+38]

    loc4 = text_in_page.find("KIWILAYA")
    rank_district = text_in_page[loc4+10:loc4+25]
    rank_district1 = rank_district[:rank_district.find("kati")]
    rank_district2 = rank_district[rank_district.find("kati")+8:]

    schoolrank_district = rank_district1 +"/"+ rank_district2

    
# In[281]:


    loc5 = text_in_page.find("KIMKOA")
    rank_region = text_in_page[loc5+10:loc5+25]
    rank_region1 = rank_region[:rank_region.find("kati")].strip()
    rank_region2 = rank_region[rank_region.find("kati")+8:].rstrip()
    schoolrank_region = rank_region1 +"/"+ rank_region2


    loc6 = text_in_page.find("KITAIFA")
    rank_nation = text_in_page[loc6+10:loc6+30]
    rank_nation1 = rank_nation[:rank_nation.find("kati")].strip()
    rank_nation2 =rank_nation[rank_nation.find("kati")+8:].rstrip()
    schoolrank_nation = rank_nation1 +"/"+ rank_nation2
        


# In[282]:


    loc_cand = text_in_page.find("CAND")
    text_in_page = text_in_page[loc_cand:]
    text_list = text_in_page.split("\n")
    filtered_list = list(filter(None, text_list))
    filtered_list=filtered_list[4:]
    cand_no = []
    sex = []
    cand_name = []
    subjects = []
    for i in filtered_list:
        if 'PS' in i:
            cand_no.append(i)
        elif len(i) == 1:
            sex.append(i)
        elif "Kiswahili" in i:
            subjects.append(i)
        else:
            cand_name.append(i)

    individ_subj = []
    for i in subjects:
        individ_subj.append(i.split(", "))
   
    individ_subj[0][1]
    Kiswahili, English, Maarifa, Hisabati, Science, Average = list(),list(),list(),list(),list(),list()
    for cat in individ_subj:
        try:
            Kiswahili.append(cat[0][-1])
            English.append(cat[1][-1])
            Maarifa.append(cat[2][-1])
            Hisabati.append(cat[3][-1])
            Science.append(cat[3][-1])
            Average.append(cat[3][-1])
        except:
            pass

    index = len(Kiswahili)+1
    dictionary = {"results":results,"year":year, "region": region, "district": district, "school_name":school_name,
                 "school_id":school_id,"school_examiner":school_examiner,"school_average":school_average,
                  "school_group": school_group,"schoolrank_district":schoolrank_district,
                 "schoolrank_region":schoolrank_region,"schoolrank_nation":schoolrank_nation,
                 "cand_no":cand_no,"id":range(1,index),"sex":sex,"cand_name":cand_name, "grade_kiswahili":Kiswahili,"grade_english":English,
                 "grade_Maarifa": Maarifa,"grade_Hisabati":Hisabati,"grade_science": Science,"grade_average":Average}
    df = pd.DataFrame(dictionary)

    name = results+year+" "+school_name+school_id
    df.to_excel(name + ".xlsx")







# In[4]:
progress = 0
for i in range(len(webpages)):
    addresses = []
    addresses.append(get_address(webpages[i]))
    
    print(addresses)
    for address in addresses[0]:
        try:
            print(addresses[0].index(address), len(addresses[0]))
            file_creator(address,districts[i])
            progress+=1
        except:
            pass



