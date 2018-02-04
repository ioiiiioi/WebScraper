#Import Library
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#input URL Target
keywo = input('enter here : ')
my_url1 = 'https://www.bukalapak.com'
kata_kunci = keywo.replace(" ","+")
my_url2 = '/products?utf8=%E2%9C%93&source=navbar&from=omnisearch&search_source=omnisearch_organic&search%5Bkeywords%5D='
my_url = my_url1 + my_url2  + kata_kunci

#membuka koneksi, menggambil halaman html
uClient = uReq(my_url)
page_html = uClient.read()
mati = uClient.close()

#html parsing
page_soup = soup(page_html, "html.parser")
halaman = page_soup.findAll("span", {"class":"last-page"})
#inisiasi list page
def makinglist(keywo):
    kata_kunci = keywo.replace(" ","+")
    listhalaman = []
    bukalapak = 'https://www.bukalapak.com' 
    page_akhir = int(halaman[0].text)
    page_ini = list(range(0,page_akhir))
    hal_jadi3 = '&search%5Bkeywords%5D='+ kata_kunci +'&search_source=omnisearch_organic&source=navbar&utf8=%E2%9C%93'   
    for hal in page_ini:
        try:
            hala = bukalapak + '/products/s?brand_badge=false&campaign_name=&from=omnisearch&page=' + str(hal) + hal_jadi3
            listhalaman.append(hala)
        except IndexError:
            print("Maaf Barang Yang Anda Cari Tidak Ada")
    #del listhalaman[0]
    return listhalaman

#setting table pada excell
filename = keywo + "-bukalapakv21.csv"
f = open(filename,"w")
headers = "Kondisi, Nama Produk, Harga, Pelapak, Feedback Pelapak, Link Halaman \n"
f.write(headers)



for hal in makinglist(keywo):
    #membuka koneksi, menggambil halaman html
    uClient = uReq(hal)
    page_html = uClient.read()
    mati = uClient.close()
    #html parsing
    page_soup = soup(page_html, "html.parser")
    #mengambil setiap produk dari web
    detils = page_soup.findAll("li", {"class":"col-12--2"})
    detil = detils[0]
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
        f.write(kondisi + "," + nama.replace("," , " ") + "," + harga + "," + penjual + "," + fdbc + "," + halaman + "\n")
f.close()
total = str(len(detils))
print("Iterasi selesai")
print("Total Produk = " + total)
