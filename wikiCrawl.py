from urllib.request import urlopen
import re

def crawl(verbose=False):
    # firstLink = "/Special:Random"
    firstLink = "/Mensch" # fiction/narrative
    print(firstLink)
    while (True):
        url = "http://de.wikipedia.org/wiki" + firstLink
        firstLink = ''
        # print(url)
        code = urlopen(url).read().decode("utf-8")
        # delete all content in parentheses with preceding [ |>] or trailing [ |,|<]
        code = re.sub(r'(?<=[ |>]\().+?(?=\)[ |<|,])', '', code)
        code = re.sub(r'<p><span.+?(?=</span>)', '', code)
        code = re.sub(r'<td.+?(?=</td>)', '', code)
        print(code)
        break;
        # first paragraph
        p = re.compile('(?<=<p>).+')
        p2 = re.compile('(?<=href\="\/wiki)[^:]+?(?=")')
        # print(p.findall(code)[0])
        # print(p2.findall(p.findall(code)[0]))
        i = 0
        while (p2.findall(p.findall(code)[i]) == []):
            i += 1
        firstLink = p2.findall(p.findall(code)[i])[0]
        print(firstLink)
        if (firstLink.split('/')[::-1][0] == 'Philosophie'):
            break
    # if (verbose):
        # print("Downloaded {} of {} referenced files\n({:.3f} kB in {:.3f} sec)"
              # .format(counter - failed, counter, totalSize, totalTime))

if __name__ == "__main__":
    crawl(verbose=True)
