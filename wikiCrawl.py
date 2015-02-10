from urllib.request import urlopen
import re
import copy

def crawl(verbose=False):
    # firstLink = "/Special:Random"
    # firstLink = "/Port_Macquarie-Hastings_Council" # Randfall <p><span>...
    # firstLink = "/Schl%C3%B6sser" # Randfall lists (<li>)
    # firstLink = "/Liste_der_Abk%C3%BCrzungen_antiker_Autoren_und_Werktitel/L"
    firstLink = "/Mensch"
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

def getLinks(article, noParantheses, includeLI):
    """ Returns a list with all links and titles on wiki article
    in a form of:
    [("link1", "title1"), ("link2", "title2")]
    do not enter the whole url, just like above
    noParantheses is boolean and decides whether or not to cut paras
    includeLI is boolean and decides whether or not to include <li>"""
    while (True):
        print(article)
        url = "http://de.wikipedia.org/wiki" + article
        code = urlopen(url).read().decode("utf-8")
        # delete all content in parentheses with preceding [ |>] or trailing [ |,|<]
        if noParantheses: code = re.sub(r'(?<=[ |>]\().+?(?=\)[ |<|,])', '', code)
        code = re.sub(r'(?<=<p>)<span.+?(?=</span>)', '', code)
        code = re.sub(r'(?<=<div class="NavContent">).+?(?=</div>)', '', code, flags=re.DOTALL)
        code = re.sub(r'<td.+?(?=</td>)', '', code, flags=re.DOTALL)
        # first paragraph
        p = re.compile('(?<=<p>).+?(?=</p>)', flags=re.DOTALL)
        # first list element
        li = re.compile('(?<=<li>).+(?=</li>)')
        # match links and titles only
        link = re.compile('(?<=href\="\/wiki)([^:]+?)" title="(.*?)(?=".*</a>)')
        # go through article
        listOfParagraphs = p.findall(code)
        listOfListElements = li.findall(code)
        listOfLinks = []
        for paragraph in listOfParagraphs:
            listOfLinks.extend(link.findall(paragraph))
        # if no link in the paragraphs, look for <li> elements
        if includeLI:
            for listElement in listOfListElements:
                listOfLinks.extend(link.findall(listElement))
        return listOfLinks

def firstLink(start):
    """always "clicks" on first link in article ... (philosophy)"""
    if (start.split('/')[::-1][0] == 'Philosophie'):
        print("Philosophie! Hooray!")
    else:
        links = getLinks(start, True, False)
        if len(links) != 0:
            print(links[0][1])
            firstLink(links[0][0])
        else:  # Try to include <li>-elements
            print("Accessing list elemtns")
            firstLink(getLinks(start, True, True)[0][0])

def BFS(start, stop):
    """Idea: Follow every way, detect loops, detect end-of-the-lines, detect end
    path is a list of lists, after iterations:
    [[link1], [link2], [link3]]
    [[link1, link1.1], [link1, link1.2], [link2, link2.1], [link2, link2.2], ... ]
    ...
    representing the paths. every link consists of (link, title)
    """
    links = getLinks(start, True, False)
    paths = []
    for link in links:
        if link[0] == stop:
            print("Path found:")
            return link
        paths.append([(start, start), link])
    # bis hierher richtig
    while(len(paths) != 0):
        path = paths.pop(0)
        links = getLinks(path[-1][0], True, False)
        for link in links:
            path.append(link)
            paths.append(copy.deepcopy(path))
            path.pop(-1)
            if link[0] == stop:
                print("Path found:")
                path = []
                for article in paths[-1]:
                    path.append(article[1])
                return path

if __name__ == "__main__":
    # crawl(verbose=True)
    print(BFS("/Drillich", "/Billerbeck"))
