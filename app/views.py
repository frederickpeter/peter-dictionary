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
    # 2. to get synonym
    request2 = requests.get(f"https://www.thesaurus.com/browse/{word}")

    # if request1 is successful
    if request1:
        #  get a BeautifulSoup object, which represents the document as a nested data structure:
        soup = BeautifulSoup(request1.text, "html.parser")
        # find all divs whose class = NZKOFkdkcvYgD3lqOIJw because on the site, those are where the meanings are
        meanings = soup.find_all("div", {"class": "NZKOFkdkcvYgD3lqOIJw"})
        if meanings:
            # get the first index since we only display 1 meaning
            meaning = meanings[0].text.strip()
        else:
            meaning = ""
    else:
        word = 'Sorry, "' + word + '" Is Not Found In Our Database'
        meaning = ""

    # if request2 is successful
    if request2:
        soup = BeautifulSoup(request2.text, "html.parser")
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
    else:
        ss = ""

    results = {"word": word, "meaning": meaning, "synonyms": ss}

    return render(request, "search.html", {"results": results})
