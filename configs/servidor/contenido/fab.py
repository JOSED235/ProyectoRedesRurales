import sys,json,urllib.request,urllib.parse,re,html
import os,time,hashlib
CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fabcache"); os.makedirs(CACHE,exist_ok=True)
def get(t):
    f=os.path.join(CACHE,hashlib.md5(t.encode()).hexdigest()+".txt")
    if os.path.exists(f): return open(f).read()
    for i in range(5):
        try: x=_get(t); break
        except Exception as e:
            if i==4: raise
            time.sleep(10*(i+1))
    open(f,"w").write(x); time.sleep(2); return x
def _get(t):
    u="https://es.wikisource.org/w/api.php?action=parse&format=json&prop=text&disablelimitreport=1&page="+urllib.parse.quote(t)
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"hub-rural-lab/1.0"}),timeout=30))
    h=d["parse"]["text"]["*"]
    h=re.sub(r'(?s)<(style|script)[^>]*>.*?</\1>','',h)
    h=re.sub(r'(?s)<span[^>]*class="[^"]*(pagenum|ws-pagenum|noprint)[^"]*"[^>]*>.*?</span>','',h)
    h=re.sub(r'(?s)<div[^>]*class="[^"]*(ws-noexport|noprint|cabecera|header)[^"]*".*?</div>','',h)
    h=re.sub(r'<br\s*/?>','\n',h); h=re.sub(r'</(p|div|dd|li|h\d)>','\n',h)
    t=html.unescape(re.sub(r'<[^>]+>','',h))
    t=re.sub(r'\[\d+\]','',t); t=re.sub(r'[ \t]+\n','\n',t); t=re.sub(r'\n{3,}','\n\n',t)
    return t.strip()
for t in sys.argv[1:]:
    print("#####",t); print(get(t))
