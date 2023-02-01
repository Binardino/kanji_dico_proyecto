import xml.etree.ElementTree as ET

#read raw kanji XML document
tree = ET.parse('kanjidic2.xml')
root = tree.getroot()

#create own dict
kanji_dict = {}

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