from urllib.request import urlopen
import re
import copy

# ToDo:
# Fix problems: - BFS(Spezielle_Zoologie->*)
#               - getLinks(Adolf_Hitler)
# Ideas: - Loop Detection

def getLinks(article, noParantheses, includeLI):
    """ Returns a list with all links and titles on wiki article
    in a form of:
    [("link1", "title1"), ("link2", "title2")]
    
    Arguments: article; url, e.g. "/Rieseneidechse"
               noParantheses; boolean, if True parantheses are cut away (for
                              example for firstLink
               includeLI; boolean, if True lists (<li>) are included
    Returns:   listOfLinks, a list of the form as above           
               """
    url = "http://de.wikipedia.org/wiki" + article
    code = urlopen(url).read().decode("utf-8")
    # delete all content in parentheses with preceding [ |>] or trailing [ |,|<]
    #if noParantheses: code = re.sub(r'(?<=[ |>]\().+?(?=\)[ |<|,])?', '', code,
    if noParantheses: code = re.sub(r'(?<=[ |>]\()[^)]+?(?=\)[ |<|,])', '', code,
        re.DOTALL)
    # delete other stuff that you're usually not allowed to use
    code = re.sub(r'(?<=<p>)<span.+?(?=</span>)', '', code)
    code = re.sub(r'(?<=<div class="NavContent">).+?(?=</div>)', '', code, flags=re.DOTALL)
    code = re.sub(r'<td.+?(?=</td>)', '', code, flags=re.DOTALL)
    # match paragraphs
    p = re.compile('(?<=<p>).+?(?=</p>)', flags=re.DOTALL)
    # match list-elements
    li = re.compile('(?<=<li>).+(?=</li>)')
    # match links and titles only
    link = re.compile('(?<=href\="\/wiki)([^:]+?)" title="(.*?)"[>| ]')
    # split up article
    listOfParagraphs = p.findall(code)
    listOfListElements = li.findall(code)
    # get links from paragraphs
    listOfLinks = []
    for paragraph in listOfParagraphs:
        listOfLinks.extend(link.findall(paragraph))
    # if no link in the paragraphs, look for <li> elements
    if includeLI:
        for listElement in listOfListElements:
            listOfLinks.extend(link.findall(listElement))
    return listOfLinks

def firstLink(start):
    """always "clicks" on first link in article to find a path to philosophy"""
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
    [[link1], [link2], [link3], ...]
    [[link1, link1.1], [link1, link1.2], [link2, link2.1], [link2, link2.2], ... ]
    ...
    representing the paths. every link consists of (link, title)
    """
    paths = [[(start, start)]] # collect all the paths: see above
    # in loop: pop first path, get all links and add the extended version of the
    # path for each link to the paths-list
    while(len(paths) != 0):
        # get links on first path
        path = paths.pop(0)
        links = getLinks(path[-1][0], True, False)
        # add a new path for each of the links
        for link in links:
            path.append(link)
            for el in path:
                print(el[1], end=' -> ')
            print()
            paths.append(copy.deepcopy(path))
            path.pop(-1)
            # only executed if target is reached:
            if link[0] == stop:
                print("Path found:")
                path = []
                for article in paths[-1]:
                    path.append(article[1])
                return path
    return("You shall not path!")

if __name__ == "__main__":
    # crawl(verbose=True)
    print(BFS("/Riesensalamander", "/Raufaser")) # FEHLER! (warum?)
    # print(getLinks("/Adolf_Hitler", True, False)) # FEHLER! (warum?)
    # print(firstLink("/Schlösser"))
