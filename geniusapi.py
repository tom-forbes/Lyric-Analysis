#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 12:44:33 2019

@author: tomforbes
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')





def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    auth_code = ''
    headers = {'Authorization': 'Bearer ' + auth_code}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    remote_song_info = None
    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
        if remote_song_info:
            song_url = remote_song_info['result']['url']
            page = requests.get(song_url)
            html = BeautifulSoup(page.text, 'html.parser')
            lyrics = html.find('div', class_='lyrics').get_text()
            print(lyrics)
            if lyrics == []:
                pass
            else:
                return lyrics
            
class Song(object):
    def __init__(self, artist_name, song_title, lyric):
        self.artist_name = artist_name
        self.song_title = song_title
        self.lyric = lyric


    
    def getStructure(self):
        return [line for line in self.lyric.splitlines() if line[:1] == '[']
        
    def bagofwords(self):
        main_body = [line for line in self.lyric.splitlines() if line[:1] != '[']
        main_body = " ".join(str(x) for x in main_body)
        return [word.replace('!', '').replace(':', '').replace(',', '').replace(')', '').replace('(', '').replace('?', '').upper() for word in main_body.split()]
    
    def lyrical_dexterity(self):
        main_body = [line for line in self.lyric.splitlines() if line[:1] != '[']
        main_body = " ".join(str(x) for x in main_body)
        remove_punctuation = [word.replace('!', '').replace(':', '').replace(',', '').replace(')', '').replace('(', '').replace('?', '').upper() for word in main_body.split()]
        number_of_words = len(remove_punctuation)
        vocabulary = list(set(remove_punctuation))
        return len(vocabulary)*100/number_of_words
    
    def countOccurences(self, word): 
    # search for pattern in a 
        word = word.upper()
        main_body = [line for line in self.lyric.splitlines() if line[:1] != '[']
        main_body = " ".join(str(x) for x in main_body)
        remove_punctuation = [word.replace('!', '').replace(':', '').replace(',', '').replace(')', '').replace('(', '').replace('?', '').upper() for word in main_body.split()]
        
        count = 0
        for i in remove_punctuation: 
            # if match found increase count  
            #print(word,i,count)
            if word == i: 
                count = count + 1
        return count    
    
    def plotOccurences(self):
        main_body = [line for line in self.lyric.splitlines() if line[:1] != '[']
        main_body = " ".join(str(x) for x in main_body)
        remove_punctuation = [word.replace('!', '').replace(':', '').replace(',', '').replace(')', '').replace('(', '').replace('?', '').upper() for word in main_body.split()]
        
        countlist = []
        wordlist = []
        for word in list(set(remove_punctuation)):
            count = 0
            for i in remove_punctuation: 
                # if match found increase count  
                if word == i: 
                    count = count + 1
            wordlist.append(word)
            countlist.append(count)
        
        df = pd.DataFrame()
        df['wordlist'] = wordlist
        df['countlist'] = countlist
        
        df = df.sort_values('countlist', ascending=False)
        #df = df[df['countlist']>df['countlist'].mean()]
        df = df[:20]

        
        countlist = df['countlist']
        wordlist = df['wordlist']
        
        
        N = 20
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35 
        fig, ax = plt.subplots(figsize=(10, 10))
        plt.xticks(rotation=90)
        ax.bar(ind, df['countlist'], width, color='r')
        ax.set_ylabel('Count')
        ax.set_title('Word Frequency')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(df['wordlist'])
        plt.show()
        
        
    
def main():
    artistlist = []
    songtitlelist = []
    dexteritylist = []
    song_title = ''
    artist_name = ''
    song_information = Song(artist_name, song_title, request_song_info(song_title, artist_name))
    song_information.getStructure()
    #song_information.countOccurences('claim')
    song_information.plotOccurences()
    song_information.lyrical_dexterity()
    
    
    artistlist.append(artist_name)
    songtitlelist.append(song_title)
    dexteritylist.append(song_information.lyrical_dexterity())

    stats = pd.DataFrame()
    stats['artist'] = artistlist
    stats['song'] = songtitlelist
    stats['dexterity'] = dexteritylist

    print(stats)


if __name__ == "__main__":
    main()



