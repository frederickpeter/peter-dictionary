from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    return render(request, "index.html")


def search(request):
    # get word
    word = request.GET["search"]
    # perform 2 get requests:
    # 1. to get definition
    request1 = requests.get(f"https://www.dictionary.com/browse/{word}")
    # 2. to get synonym + antonym
    request2 = requests.get(f"https://www.thesaurus.com/browse/{word}")

    # if request1 is successful
    if request1:
        #  get a BeautifulSoup object, which represents the document as a nested data structure:
        soup = BeautifulSoup(request1.text, "html.parser")
        # find all divs whose value = 1 because on the site, those are where the meanings are
        meanings = soup.find_all("div", {"class": "NZKOFkdkcvYgD3lqOIJw"})
        if meanings:
            # get the first index since we only display 1 meaning
            meaning1 = meanings[0].getText(strip=True)
        else:
            meaning1 = ""
    else:
        word = 'Sorry, "' + word + '" Is Not Found In Our Database'
        meaning1 = ""

    # if request2 is successful
    if request2:
        #  get a BeautifulSoup object, which represents the document as a nested data structure:
        soup = BeautifulSoup(request2.text, "html.parser")
        # find all anchor tags whose class = 'css-1kg1yv8 eh475bn0' because on the site, those are where the synonyms are
        synonyms = soup.find_all(
            "a",
            {
                "class": [
                    "Bf5RRqL5MiAp4gB8wAZa",
                    "CPTwwN0qNO__USQgCKp8",
                    "u7owlPWJz16NbHjXogfX",
                ]
            },
        )
        ss = [synonym.text.strip() for synonym in synonyms]
        # if not ss:
        #     synonyms = soup.find_all("a", {"class": "CPTwwN0qNO__USQgCKp8"})
        #     ss = [synonym.text.strip() for synonym in synonyms]

    else:
        ss = ""

    results = {"word": word, "meaning": meaning1, "synonyms": ss}

    return render(request, "search.html", {"results": results})
