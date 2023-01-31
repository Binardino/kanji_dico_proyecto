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
        print('kanji', kanji)
        
        
        if element.tag == 'misc/jlpt':
        #not all kanji have JLPT level defined
            jlpt_level   = element.find('misc/jlpt').text
        else:
            jlpt_level   = None
        stroke_count = element.find('misc/stroke_count').text
        #fetching radical value from classical kanji numerotation
        radical      = element.find('radical/rad_value').text

        
        #instantiate variables
        meanings = []
        pronunciations = {}

        #get sublevel keys
        # for child in element:
                        # if child.tag == 'reading_meaning':
            #     for subchild in child:
            #         if subchild.tag == 'rmgroup':
            #     meaning      = child.find('meaning').text
            #     if == r_type="ja_kun":
            #         reading_kun  = element.find('meaning').text
            #     elif == r_type="ja_on":
            #         reading_on   = element.find('meaning').text
            
        
        #Add entry to kanji_dict
        kanji_dict[kanji] = {'meanings'     : meanings,
                             'jlpt_level'   : jlpt_level,
                             'stroke_count' : stroke_count,
                             'radicals' 	: radical
                             # 'reading_kun'  : reading_kun,
                             # 'reading_on'   : reading_on
                             }