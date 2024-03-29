import xml.etree.ElementTree as ET
import pandas as pd

#define function
def get_key(meaning):
    for key, value in kanji_dict.items():
        if meaning in value['meanings']:
            print(f"""-----------------------------
                  Kanji for {meaning} is {key}""")
            print(f'Kanji has the following info : {kanji_dict[key]}')
            
        else : "kanji not found"


#read raw kanji XML document
tree = ET.parse('../data/kanjidic2.xml')
root = tree.getroot()

#create own dict
kanji_dict = {}

radical_number = []

print("parsing Kanji XML doc")
#iteration through kanji in character beacon
for kanji in root.findall('character'):
    #get kanji symbol
    symbol = kanji.find('literal').text
    print('kanji', symbol)
    
    #not all kanji have JLPT level defined
    jlpt_level   = kanji.find('misc/jlpt').text if kanji.tag == 'misc/jlpt' else None
    stroke_count = kanji.find('misc/stroke_count').text
    #fetching radical value from classical kanji numerotation
    radical      = kanji.find('radical/rad_value').text
    
    radical_number.append(kanji.find('radical/rad_value').text)

    #instantiate variables
    meanings = []
    reading_kun = []
    reading_on = []
    
    #fetching all meanings of kanji to append to list
    for meaning in kanji.findall('reading_meaning/rmgroup/meaning'):
        meanings.append(meaning.text)
        
    #fetching all pronunciations - split in kun-yomi & on-yomi - to append to relevant list        
    for pronunciation in kanji.findall('reading_meaning/rmgroup/reading'):
        if pronunciation.attrib['r_type'] == 'ja_kun':
            print('ja_on',pronunciation.text)
            reading_kun.append(pronunciation.text)
        elif pronunciation.attrib['r_type'] == 'ja_on':
            reading_on.append(pronunciation.text)
            # reading_kun[pronunciation] = pronunciation
            print(reading_kun)
        
        #Add entry to kanji_dict
        kanji_dict[symbol] = {'meanings'     : meanings,
                             'jlpt_level'   : jlpt_level,
                             'stroke_count' : stroke_count,
                             'radicals' 	: radical,
                             'reading_kun' : reading_kun,
                              'reading_on'   : reading_on
                             }
        
print("parsing XML doc done !")

print("exporting copy in csv")
df_kanji = pd.DataFrame.from_dict(kanji_dict, orient='index')
df_kanji.to_csv("../data/df_kanji.csv", index=False)

#%%
print('input needed kanji')
print(get_key('great'))
