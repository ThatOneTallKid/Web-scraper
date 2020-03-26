import requests,os
from bs4 import BeautifulSoup as bs
from pathlib import Path as path
import pyinputplus as pypi
import re


def manga():
    user=input("\nGive us the link of the manga you want(from this website (https://manganelo.com)):\n")#Link for manga
    if not user.startswith('https://manganelo.com/'):
        while True:
            warningLink=input('\nPlease make sure that you used this link(https://manganelo.com/manga/)to choose your manga/or make sure you choose a manga anyway:\n ')
            if warningLink.startswith('https://manganelo.com/manga/'):
                break


    while True:#Make sure that the user will enter a number or a nothing but not string
        try:
            chStart=int(input('\nFrom which chapter do you want to start?:\n'))#need this to go the ordered chapter of the manga

        except:
            print('Enter a number')
            continue
        if chStart:
            break
        
        if not chStart:
            break
    
    ch=chStart
    
    try:
        chEnd=int(input(f"\nYou want to download from chapter{chStart} to? or if you want to download all after don't type anything:\n"))
    except ValueError:
        chEnd=False
        pass
    
    folderName=input('\nGive us a name to the manga folder you want to download:\n')


    try:
        os.makedirs(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}')#The folder which will contain the manga files and chapters folders
    except:
        pass
    
    replaceLink=user.replace('/manga/','/chapter/',1)
    
    link=replaceLink+f'/chapter_{chStart}/'#create the link which request will go for
    
    if not chEnd:#If user did't choose an end chapter
        while True:#This allow us to go for another chapter 
                nameRegex=re.compile(r'chapter_\w+\.?\w*/?')#Get the chapter name/number
              
                regexFind=nameRegex.search(link).group()
                fullName=regexFind.replace('/','')#Get the full name of the chapter
                res=requests.get(link)
                res.raise_for_status()
                soup=bs(res.text,'html.parser')

                imgElem=soup.select('body > div.body-site > div.container-chapter-reader > img')#Get the css selector for the manga image
                
              
                    

                for i in range(len(imgElem)):#Page loop

                   
                    src=imgElem[i].get('src')

                    fullLink=src
                    res=requests.get(fullLink)
                    if not os.path.exists(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}'):
                        os.makedirs(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}')  #create the chapter file  
                    animeFile=open(os.path.join(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}',os.path.basename(fullLink)),'wb+')#file name
                   
                    print(f'\nDownloading  {fullLink}')
                    for chunk in res.iter_content(100000):#File download
                        animeFile.write(chunk)
                    animeFile.close()
                print(f'\n{fullName} Is Done\n')
                nextElem=soup.select('a.navi-change-chapter-btn-next')#Get the css selector for the next button
                try:
                    href=nextElem[0].get('href')#Link for the next chapter
                except IndexError:
                    print(f'\nSeems like theres an error in you code... try this:\n1-Make sure you choosed to start from a vaild chapter. example:you choosed chapter 0 and the manga starts from chapter 1\n2-Make sure that the link you put is a link for normal manga page(The page that you see from  info for the manga).\n3-Sometimes there is no error in your link just the program didnt found another chapter so its stopped(that usually happen when you dont put an end chapter so its normal dont worry).')
                    break

                
                link=href
               
        print('Thanks for using this app')
    if chEnd:#if user choose an end chapter
        

        fullRange=chEnd-chStart
        for i in range(int(fullRange+1)):
            nameRegex=re.compile(r'chapter_\w+\.?\w*/?')#Get the chapter name

            regexFind=nameRegex.search(link).group()

            fullName=regexFind.replace('/','') 
            res=requests.get(link)
            res.raise_for_status()
            soup=bs(res.text,'html.parser')

            imgElem=soup.select('body > div.body-site > div.container-chapter-reader > img')#Get the css selector for the manga image
            if not os.path.exists(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}'):
                        os.makedirs(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}')  #create the chapter file  
        
            for i in range(len(imgElem)):#Page loop

                src=imgElem[i].get('src')
                fullLink=src
                res=requests.get(fullLink)
            
                animeFile=open(os.path.join(f'C:\\Users\\Administrator\\Desktop\\manga\\{folderName}\\{fullName}',os.path.basename(fullLink)),'wb+')#file name
                   
                print(f'\nDownloading  {fullLink}')
                for chunk in res.iter_content(100000):#File download
                    animeFile.write(chunk)
                animeFile.close()
            
            print(f'\n{fullName} Is Done\n')
            nextElem=soup.select('a.navi-change-chapter-btn-next')#Get the css selector for the next button
            try:
                href=nextElem[0].get('href')#Link for the next chapter
            except IndexError:
                print(f'\nSeems like theres an error in you code... try this:\n1-Make sure you choosed to start from a vaild chapter. example:you choosed chapter 0 and the manga starts from chapter 1\n2-Make sure that the link you put is a link for normal manga page(The page that you see from  info for the manga).\n3-Sometimes there is no error in your link just the program didnt found another chapter so its stopped(that usually happen when you dont put an end chapter so its normal dont worry).')
                break

                
            link=href
           


        print('Thanks for using this app')

        
manga()
