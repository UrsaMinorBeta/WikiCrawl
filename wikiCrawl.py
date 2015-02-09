from urllib.request import urlopen
import re

def crawl(verbose=False):
    # firstLink = "/Special:Random"
    # firstLink = "/Port_Macquarie-Hastings_Council" # Randfall <p><span>...
    # firstLink = "/Schl%C3%B6sser" # Randfall lists (<li>)
    firstLink = "/Liste_der_Abk%C3%BCrzungen_antiker_Autoren_und_Werktitel/L"
    print(firstLink)
    while (True):
        url = "http://de.wikipedia.org/wiki" + firstLink
        firstLink = ''
        # print(url)
        code = urlopen(url).read().decode("utf-8")
        # delete all content in parentheses with preceding [ |>] or trailing [ |,|<]
        code = re.sub(r'(?<=[ |>]\().+?(?=\)[ |<|,])', '', code)
        code = re.sub(r'(?<=<p>)<span.+?(?=</span>)', '', code)
        code = re.sub(r'<td.+?(?=</td>)', '', code, flags=re.DOTALL)
        # print(code)
        # first paragraph
        p = re.compile('(?<=<p>).+')
        # first list element
        li = re.compile('(?<=<li>).+')
        # first td element
        td = re.compile('(?<=<td).+') # only for strange lists
        # match links only
        link = re.compile('(?<=href\="\/wiki)[^:]+?(?=")')
        # print(p.findall(code)[0])
        # print(p2.findall(p.findall(code)[0]))
        listOfParagraphs = p.findall(code)
        listOfLists = li.findall(code)
        listOfLinks = []
        for paragraph in listOfParagraphs:
            listOfLinks.extend(link.findall(paragraph))
        # if no link in the paragraphs, look for <li> elements
        if len(listOfLinks) == 0:
            for listElement in listOfLists:
                listOfLinks.extend(link.findall(listElement))
        firstLink = listOfLinks[0]
        print(firstLink)
        if (firstLink.split('/')[::-1][0] == 'Philosophie'):
            break
    # if (verbose):
        # print("Downloaded {} of {} referenced files\n({:.3f} kB in {:.3f} sec)"
              # .format(counter - failed, counter, totalSize, totalTime))

if __name__ == "__main__":
    crawl(verbose=True)
