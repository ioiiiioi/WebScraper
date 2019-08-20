from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# Create your views here.

@api_view(['GET'])
def find_product(request):
	if request.method == 'GET':
		keywo = request.data['keyword']
		
		my_url1 = 'https://www.bukalapak.com'
		kata_kunci = keywo.replace(" ","+")
		my_url2 = '/products?utf8=%E2%9C%93&source=navbar&from=omnisearch&search_source=omnisearch_organic&search%5Bkeywords%5D='
		my_url = my_url1 + my_url2  + kata_kunci

		uClient = uReq(my_url)
		page_html = uClient.read()
		mati = uClient.close()
		page_soup = soup(page_html, "html.parser")

		halaman = page_soup.findAll("span", {"class":"last-page"})
		# print(page_soup)
		# return Response({'hasil':keywo})
		listhalaman = []
		result = []
		page_akhir = int(halaman[0].text)
		page_ini = list(range(0,page_akhir))
		hal_jadi3 = '&search%5Bkeywords%5D='+ kata_kunci +'&search_source=omnisearch_organic&source=navbar&utf8=%E2%9C%93'   
		for hal in page_ini:
			try:
				hala = my_url1 + '/products/s?brand_badge=false&campaign_name=&from=omnisearch&page=' + str(hal) + hal_jadi3
				listhalaman.append(hala)
			except IndexError:
				print("Maaf Barang Yang Anda Cari Tidak Ada")


		# for link in listhalaman:
			#membuka koneksi, menggambil halaman html
			# uClient = uReq(link)
		uClient = uReq(listhalaman[0])
		page_html = uClient.read()
		mati = uClient.close()
		#html parsing
		# page_soup = soup(page_html, "html.parser")
		#mengambil setiap produk dari web
		detils = page_soup.findAll("li", {"class":"col-12--2"})
		detil = detils[0]
		print(detils)
		for detil in detils:
			nama = detil.div.article["data-name"]
			price = detil.find("span", {"class":"amount positive"})
			harga = price.text
			kondisi = detil.find("div", attrs={"product-meta"}).span.text
			asal = detil.find("span", {"class":"user-city__txt"})
			plp = detil.find("h5", attrs={"user__name"})
			penjual = plp.a.text + "(" + asal.text + ")"
			fdbc = detil.find("a", attrs={"user-feedback-summary"}).text
			halaman = "https://www.bukalapak.com" + detil.find("div", attrs={"product-media"}).a["href"]

			wrapedDict = {
			'kondisi' : kondisi,
			'produk' : nama,
			'harga' : harga,
			'pelapak' : penjual,
			'feedback' : fdbc,
			'link' : halaman,
			}
			result.append(wrapedDict)
		hasil = {
					'jumlah_produk':len(result),
					'page':int(listhalaman[0][91])+1,
					'result':result
				}
		return Response(hasil)
	return Response({'hasil':'gagal'}, status = status.HTTP_404_NOT_FOUND)