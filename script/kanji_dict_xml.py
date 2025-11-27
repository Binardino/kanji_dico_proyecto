import logging
import xml.etree.ElementTree as ET
import pandas as pd
import json
from typing import Optional, Dict, List, Any

#logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a logger object
logger = logging.getLogger(__name__)
#%%
"""
XML document is inconsistent & nodes are often missing

JMdict, KANJIDIC2, and KANA dictionaries all contain optional elements.

Creating those 2 functions to avoid NoneType error if the node is not present for a particular kanji entry

Avoid repeating try & except OR if statement for each entry
"""

def get_text(parent : Optional[ET.Element], tag: Optional[str]=None, default=None) -> Optional[str]:
    """Flexible text extractor.
       Return node.text safely with a default None output.
       Lookup inside a parent element
       
       - Handles parent = None
       - Handles missing subtag
       - Handles missing .text
       
       Usage:
           Case #1 - get_text(node)            -> node.text
           Case #2 - get_text(parent, "tag")   -> parent.find('tag').text 
    """
    
    #Case 1 : called as get_text(node)
    if tag is None:
        return parent.text if parent is not None else default
    
    if parent is None:
        return default
    node = parent.find(tag)

    return node.text if node is not None else default

def get_all_text(nodes):
    """Return all .text values from a list of nodes.
       Avoid repeating same n.text for n in X loop for each kanji entry"""
       
    return [n.text for n in nodes if n.text is not None]

def find_nodes(parent : Optional[ET.Element], path: str) -> List[ET.Element]:
    """Safe wrapper around parent.findall() 
    Avoid having "AttributeError: 'NoneType' object has no attribute 'findall'" if a node is None
    
    Output : List - Empty if None
    """
    if parent is None:
        return []
    return parent.findall(path)


#%% Main Parser
def kanji_XML_parser_dic2(xml_path):
    logging.info(f"loading XML file : {xml_path}")
    #read raw kanji XML document
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    #create own dict
    kanji_dict = {}
    
    logging.info("Starting parsing Loop : Kanji XML doc")
    
    #iteration through kanji in character beacon
    for kanji in root.findall('character'):
        #get kanji symbol
        literal = kanji.find('literal').text
        logging.info(f"Processing kanji: {literal}")
        
        #codepoints fetching
        #codepoints store list of Unicode values ie. Unicode hex | Japanese JIS | variants
        codepoints = {cp.get('cp_type') : get_text(cp) for cp in kanji.findall("codepoint.cp_value")} 
        
        #radicals
        #fetching radical value from classical kanji numerotation - range 1 to 214
        #various classifications (classical, Shibano "JIS Kanwa Jiten", nelson_c...) 
        #stored in rad_type attribute
        radicals   = {rad.get('rad_type') : get_text(rad) for rad in kanji.findall("radical/rad_value")} 
        
        #multiple readings & meanings for each kanji
        readings_on  = []
        readings_kun = []
        readings_ch  = []
        readings_kr  = []
        meanings     = []
        
        #fetching all pronunciations - split in kun-yomi & on-yomi - to append to relevant list        
        for readings in kanji.findall('reading_meaning/rmgroup/reading'):
            if readings.attrib['r_type'] == 'ja_kun':
                readings_kun.append(readings.text)
                print('ja_kun',readings_kun)
                
            elif readings.attrib['r_type'] == 'ja_on':
                readings_on.append(readings.text)
                # reading_kun[pronunciation] = pronunciation
                print('ja_on', readings_on)
            
            elif readings.attrib['r_type'] == 'pinyin':
                readings_ch.append(readings.text)
                # reading_kun[pronunciation] = pronunciation
                print('chinese pinyin', readings_ch)

            elif readings.attrib['r_type'] == 'korean':
                readings_kr.append(readings.text)
                # reading_kun[pronunciation] = pronunciation
                print('chinese pinyin', readings_kr)
                
        #fetching all meanings of kanji to append to list
        #create dictionary of meanings per languages
        for meaning in kanji.findall('reading_meaning/rmgroup/meaning'):
            meanings.append({"lang" : meaning.get('m_lang', 'en'), #default meaning in EN but exist sometimes meanings in FR, ES, PT
                             "text" : get_text(meaning)}
                )
            
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
