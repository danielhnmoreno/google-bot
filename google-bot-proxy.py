import requests
# A função para remoção de tags HTML foi retirado de http://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
##########
import re
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&amp;', '&')
    return cleantext
#########
count = 0
query = 'daniel moreno pentest'
num = 100
# Lista de proxies anônimos, defina na forma IP:PORTA. Exemplo:
lista = ['127.0.0.1:3128', '6.6.6.6:666']
# Deixe a lista vazia caso não seja usado proxies
#lista = []
if len(lista) == 0:
    no_proxy = True
else:
    no_proxy = False
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0'}
proxy_item = 0
proxy_fail = []
proxy_detected_by_google = []
fim = False
while True:
    params = {'q' : query, 'start':count, 'num':num}
    if no_proxy:
        request = requests.get('http://www.google.com.br/search', headers=headers, params=params)
    elif proxy_item < len(lista):
        proxy = { 'http' : lista[proxy_item]}
        try:
            request = requests.get('http://www.google.com.br/search', headers=headers, params=params, proxies=proxy)
        except:
            proxy_fail.append(lista[proxy_item])
            proxy_item += 1
            continue
    else:
        break
    html_page = request.text
    #print(html_page)
    if ("Our systems have detected unusual traffic from your computer network" in html_page):
        proxy_item += 1
        proxy_detected_by_google_IP = html_page[html_page.find('IP address:') +12: html_page.rfind('<br>Time:')]
        proxy_detected_by_google.append(proxy_detected_by_google_IP)
        no_proxy = False
        continue
    count_cite = html_page.count('<cite')
    if(count_cite == 0):
        fim = True
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
    count+=100
if ( len(proxy_fail) != 0 or len(proxy_detected_by_google) != 0 ):
    if ( len(proxy_fail) != 0 ):
        print('Os proxys/IPs a seguir falharam, troque-os: ')
        for x in range( len(proxy_fail) ):
            print( ' ' + proxy_fail[x])
    if( len(proxy_detected_by_google) != 0):
        print('Os proxys/IPs a seguir foram detectados pelo Google, troque-os: ')
        for x in range( len(proxy_detected_by_google) ):
            print( ' ' + proxy_detected_by_google[x])
    if not fim:
        print("Altere o valor da variável 'count' para", count)
