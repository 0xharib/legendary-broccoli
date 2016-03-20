# -*- coding: utf-8 -*-
# Data Source: Homeprice Property Valuation - homeprice.com.hk
# Copyright © 2014
url = 'http://en.homeprice.com.hk/'
url_apt = 'http://en.homeprice.com.hk/building/'
writefile = "C:\pricelinedata.txt"
printinfo = ' '.encode('utf-8')
import mechanize
import cookielib
import io
import time
f = io.open(writefile, 'w', encoding='utf8')
from bs4 import BeautifulSoup as bs

linecount = 0;

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

br2 = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br2.set_cookiejar(cj)
br2.set_handle_equiv(True)
br2.set_handle_gzip(True)
br2.set_handle_redirect(True)
br2.set_handle_referer(True)
br2.set_handle_robots(False)
br2.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br2.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]

br3 = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br3.set_cookiejar(cj)
br3.set_handle_equiv(True)
br3.set_handle_gzip(True)
br3.set_handle_redirect(True)
br3.set_handle_referer(True)
br3.set_handle_robots(False)
br3.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
br3.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')]

printinfo = ""
br.open(url)
br.select_form(name = "valuation_form")
br['region'] = ['Hong Kong']
br.submit()
br.select_form(name = "valuation_form")
for control_a in br.form.controls:
	if control_a.name == "district18":  # means it's class ClientForm.SelectControl
		for item_a in control_a.items:
			if item_a.name != "":
				 br['district18'] = [ item_a.name ]
				 br.submit()
				 br.select_form(name = "valuation_form")
				 for control_b in br.form.controls:
				    if control_b.name == 'estate_web_id':
					     for item_b in control_b.items:
							 if item_b.name == "":
								continue
							 else:
								 estate_code = item_b.name
								 estate_name = str(item_b.get_labels()[0].text)
								 estate_name = "_".join(estate_name.split())
								 url_apt = 'http://en.homeprice.com.hk/building/' + str(estate_name) + '/' + str(estate_name) + '/' + str(estate_code) + '/'
								 Html = br2.open(url_apt)
								 for link in br2.links():
									 linktext = str(link.text)
									 if linktext.endswith("M") == False:
										continue
									 else:
										 linktext2 = str(link.url)
										 building_floor = str( linktext2.split('/')[4] )
										 building_apt   = str( linktext2.split('/')[5] )
										 url3 = 'http://en.homeprice.com.hk' + str( link.url )
										 Html_Page = br3.open( url3 )
										 print url3
										 soup = bs(Html_Page, "html.parser")
										 locatetable = soup.find(text="Valuation Date")
										 try:
											 getattr(locatetable, 'find_parent')         
										 except AttributeError:
											 continue
										 else:
											 table = locatetable.find_parent("table")
											 range_x = [0,1,3,4,5]  
											 for r_index in range_x:
												 row = table.find_all("tr")[r_index]
												 third_column = row.findAll('td')[2]
												 i = -1
												 for elem in third_column.contents:
													 i = i + 1
													 if i == 0:
														if   r_index == 0:
															 valuation_date = str( elem )
														elif r_index == 3:
															 valuation_range  = str(elem)
															 valuation_range  = valuation_range[0:valuation_range.find('\n')-1]	
														elif r_index == 4:
															 avg_price_per_sft = str(elem) 
														elif r_index == 5:
															 construction_area = str(elem)
															 construction_area = construction_area[0:construction_area.find('\n')-1]
														elif r_index == 1:
															 valuation_amount = str(elem)
															 valuation_amount = valuation_amount[0:valuation_amount.find('M')]
											 printinfo += item_a.name + "^" + estate_name + "^" + estate_code + "^" + building_floor + "^" + building_apt + "^" + str( url3 ) + "^" + valuation_amount + "^" + valuation_range + "^" + avg_price_per_sft + "^" + construction_area + "^"  + valuation_date + "\n"
											 linecount = linecount + 1
											 if linecount == 100:
												linecount = 0
												f = io.open(writefile, 'w', encoding='utf8')
												f.write(printinfo.decode('utf-8'))
												f.close()
											 
										 #break
							   	 #break				 				    

f = io.open(writefile, 'w', encoding='utf8')
f.write(printinfo.decode('utf-8'))
f.close()
br.close()	
br2.close()
br3.close()
