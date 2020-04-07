import json
import urllib

import xmltodict


class XMLHelper:

    def getXML(url):
        xmlFile = urllib.request.urlopen(url)
        xmlResponse = xmlFile.read().decode('ISO-8859-1').encode('latin-1')
        xmlResponse = xmlResponse
        xmlFile.close()
        return xmlResponse
        pass

    def makeDict(xmlFile):
        data = xmltodict.parse(xmlFile)
        return data

    def saveJSON(dictionary):
        currentDayData = dictionary
        file = open('data.json', 'w')
        # Write the currentDay as JSON
        file.write(json.dumps(currentDayData))
        file.close()
        return True
        pass
