pagerange = 465
writefile = "c:\Users\8u1x0\Studies\Python\data.txt"
url  = "http://singapore.lib.overdrive.com/3E1CF67D-D9A9-4853-AB5B-A61264B4F3CF/10/50/en/SearchResults.htm?SearchID=43587634s&SortBy=title&SortOrder=asc&Page="
import mechanize
import cookielib
import io
f = io.open(writefile, 'w', encoding='utf8')
from bs4 import BeautifulSoup as bs
printinfo = 'title*copiesavail*link'.encode('utf-8')
for pagecount in range (1,pagerange):
	 br = mechanize.Browser()
	 cj = cookielib.LWPCookieJar()
	 br.set_cookiejar(cj)
	 br.set_handle_equiv(True)
	 br.set_handle_gzip(True)
	 br.set_handle_redirect(True)
	 br.set_handle_referer(True)
	 br.set_handle_robots(False)
	 br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	 br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]
	 Html = br.open(url + str(pagecount)).read()
	 soup = bs(Html, "html.parser")
	 content = soup.select("div[data-rtltitle]")
	 print 'page' + str( pagecount ) + '\n'
	 for tag in content:
	     if hasattr(tag, 'data-rtltitle'):
			 print tag[ 'data-rtltitle' ].encode('utf-8')
			 printinfo += tag[ 'data-rtltitle' ].encode('utf-8')+'*'+tag[ 'data-rtlauthor' ].encode('utf-8')+'*'+url2+str(tag[ 'data-rtlcriddata' ])+'\n'			 
	 br.close()
f.write(printinfo.decode('utf-8'))