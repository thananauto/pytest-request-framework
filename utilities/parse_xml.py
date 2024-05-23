import xml.etree.ElementTree as ET 

def getXmlValue_with_path(xmlfile, xpath):
        """ Method to read the xml value with xpath"""
        tree = ET.fromstring(xmlfile)
        #__readfile(filePath=filepath)
        value = []
        root = tree.tag
        for version in root.findall(xpath):
            value.append(version.text)
        return "".join(value) if len(value) == 1 else value;

def getXmlValue_with_keyword( xmlfile, keyword):
    """ Method to read the xml value with keyword"""
    tree = ET.fromstring(xmlfile)
    value = []
    root = tree.tag
    for version in root.iter(keyword):
        value.append(version.text)
    return "".join(value) if len(value) == 1 else value;

def __readfile(self, filePath):
        with open(f'{filePath}', 'r') as xmlfile:
            file_content = ET.parse(xmlfile)
        return file_content
