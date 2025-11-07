import webbrowser
inp = "what is a frop"
url = "http://www.google.com/search?q="
search = url+inp.replace(" ","+")
webbrowser.open(search)
