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
        print(kanji)