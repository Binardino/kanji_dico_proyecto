import xml.etree.ElementTree as ET

#read raw kanji XML document
tree = ET.parse('kanjidic2.xml')
root = tree.getroot()

#create own dict
kanji_dict = {}

for element in root:
    #check if element is a kanji
    if element.tag == 'character':
        #get kanji key as entry
        kanji = element.find('literal').text
        print('kanji' : kanji)
        
        #get sublevel meanings
        jlpt_level   = element.find('jlpt').text
        stroke_count = element.find('stroke_count').text
        radical      = element.find('radical').text
        meaning      = element.find('meaning').text
        reading_on   = element.find('meaning').text
        reading_kun  = element.find('meaning').text
        
        #Add entry to kanji_dict
        kanji_dict[kanji] = {'meanings'     : meanings,
                             'jlpt_level'   : jlpt_level,
                             'stroke_count' : stroke_count,
                             'radicals' 	: radicals,

                             }