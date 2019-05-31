import urllib.request
import os
from bs4 import BeautifulSoup

#Define functions
def processText(divs, type):
    final_text = ""
    divText = ""
    
    if type is "graduate":
        for div in divs:
            divText = div.text
            if divText is not "":
                # removes whitespace
                lines = (line.strip() for line in divText.splitlines())
                # merge into 1 line
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # remove blank lines
                divText = ' '.join(chunk for chunk in chunks if chunk)
                final_text += divText+'\n\n'
                divText=""
    elif type is "general":
        for idx, div in enumerate(divs):
            divText = div.text
            if idx > 1 and idx < (len(divs)-2):
                # removes whitespace
                lines = (line.strip() for line in divText.splitlines())
                # merge into 1 line
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # remove blank lines
                divText = ' '.join(chunk for chunk in chunks if chunk)
                divText.replace('\n', ' ')
                if divText is not "" and divText != "Print":
                    final_text += divText+'\n\n'
                divText=""
    elif type is "executive":
        for idx, div in enumerate(divs):
            divText = div.text
            if idx > 9 and idx < (len(divs)-3):
                # removes whitespace
                lines = (line.strip() for line in divText.splitlines())
                # merge into 1 line
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # remove blank lines
                divText = ' '.join(chunk for chunk in chunks if chunk)
                divText.replace('\n', ' ')
                if divText is not "" and divText != "Print":
                    final_text += divText+'\n\n'
                divText=""

    return final_text

def stripSoup(containsContact):
    #Strips away all scripts, styles and hyperlinks
    if containsContact:
        for script in soup(["script", "style"]):
            script.extract()
    else:
        for script in soup(["script", "style"]):
            script.extract()

def checkDirectories():
    #Check directories
    directory1 = "generalInfo"
    directory2 = "graduateProgrammes"
    directory3 = "executiveEducation"
    directory4 = "stackableProgrammes"

    if not os.path.exists(directory1):
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        os.makedirs(directory2)
    if not os.path.exists(directory3):
        os.makedirs(directory3)
    if not os.path.exists(directory4):
        os.makedirs(directory4)

#Define variables
categories = ["General Information", "Graduate Programmes", "Executive Education", "Stackable Programmes"]
directoryNames = ["generalInfo", "graduateProgrammes", "executiveEducation", "stackableProgrammes"]
generalInfoURLs = ["https://www.iss.nus.edu.sg/about-us/director-ceo's-welcome",
                   "https://www.iss.nus.edu.sg/about-us/our-story",
                   "https://www.iss.nus.edu.sg/about-us/our-achievements",
                   "https://www.iss.nus.edu.sg/about-us/our-management-board",
                   "https://www.iss.nus.edu.sg/about-us/why-NUS-ISS",
                   "https://www.iss.nus.edu.sg/about-us/contact-us",
                   "https://www.iss.nus.edu.sg/about-us/getting-to-nus-iss"]

graduateProgrammeURLs = ["https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/graduate-diploma-in-systems-analysis",
                            "https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-enterprise-business-analytics",
                            "https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-digital-leadership",
                            "https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-software-engineering",
                            "https://www.iss.nus.edu.sg/graduate-programmes/programme/detail/master-of-technology-in-intelligent-systems"]

executiveEducationURLs = ["https://www.iss.nus.edu.sg/executive-education/discipline/detail/artificial-intelligence",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/cybersecurity",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/data-science",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-agility",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-innovation-design",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-strategy-leadership",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/digital-products-platforms",
                        "https://www.iss.nus.edu.sg/collaboration/professional-conversion-programmes",
                        "https://www.iss.nus.edu.sg/executive-education/skillsfuture-series",
                        "https://www.iss.nus.edu.sg/professional-diploma-in-smart-health-leadership",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/software-systems",
                        "https://www.iss.nus.edu.sg/executive-education/discipline/detail/stackup---startup-tech-talent-development"]

stackableProgrammesURLs = ["https://www.iss.nus.edu.sg/stackable-certificate-programmes/business-analytics",
                            "https://www.iss.nus.edu.sg/executive-education/course/detail/nus-iss-certificate-in-digital-solutions-development",
                            "https://www.iss.nus.edu.sg/stackable-certificate-programmes/Intelligent-systems",
                            "https://www.iss.nus.edu.sg/stackable-certificate-programmes/Software-engineering"]

container = ""

checkDirectories()

for idx, category in enumerate(categories):
    print("Processing: "+category)
    if category is "General Information":
        for url in generalInfoURLs:
            strSplit = url.split("/")
            fileName = strSplit[-1].lower()

            f = open(directoryNames[idx]+"/"+fileName+".txt", "w", encoding='utf-8')
            
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")
            containsContact = "contact" in url or "getting" in url
            stripSoup(containsContact)
            container = processText(soup.findAll("div", {"class":"sfContentBlock"}), "general")
            f.write(container)
            f.close()
    elif category is "Graduate Programmes":
        for url in graduateProgrammeURLs:
            strSplit = url.split("/")
            fileName = strSplit[-1].lower()

            f = open(directoryNames[idx]+"/"+fileName+".txt", "w", encoding='utf-8')

            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")
            stripSoup(False)
            container = processText(soup.findAll("div", {"class":"main-content-entry with-break"}), "graduate")
            f.write(container)
            f.close()
    elif category is "Executive Education":
        for url in executiveEducationURLs:
            strSplit = url.split("/")
            fileName = strSplit[-1].lower()

            f = open(directoryNames[idx]+"/"+fileName+".txt", "w", encoding='utf-8')
            
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")
            stripSoup(True)
            container = processText(soup.findAll("div", {"class":"row"}), "executive")
            f.write(container)
            f.close()
    elif category is "Stackable Programmes":
        for url in stackableProgrammesURLs:
            strSplit = url.split("/")
            fileName = strSplit[-1].lower()

            f = open(directoryNames[idx]+"/"+fileName+".txt", "w", encoding='utf-8')
            
            html = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")
            stripSoup(True)
            container = processText(soup.findAll("div", {"class":"content-wrap js-contentFontResize"}), "stackable")
            f.write(container)
            f.close()