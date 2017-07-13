import requests
# A função para remoção de tags HTML foi retirado de http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
##########
import re
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&amp;', '&')
    return cleantext
##########
count = 0
query = 'daniel moreno pentest'
num = 100
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'}
while True:
    params = {'q' : query, 'start':count, 'num':num}
    request = requests.get('http://www.google.com.br/search', headers=headers, params=params)
    html_page = request.text
    count_cite = html_page.count('<cite')
    if(count_cite == 0):
        break
    end = 0
    for x in range( count_cite ):
        start = html_page.find('<div class="g">',end)
        if(start == -1):
            continue
        end = html_page.find('<div class="g">', start+1)
        pagina = html_page[start:end]
        title = pagina[ pagina.find('>', pagina.find('href') ) +1: pagina.find('</a>')]
        print('Title: ', cleanhtml(title) )
        url = pagina[ pagina.find('"', pagina.find('<a href=') ) +1: pagina.find('"', pagina.find('<a href=') +9) ]
        print('URL: ', cleanhtml(url) )
        text = pagina[ pagina.find('<span class="st">') : pagina.find('</span></div>')]
        print('Text: ', cleanhtml(text) )
        print()
    count+=10
