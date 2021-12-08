import requests,bs4,threading
count = 0

def thread(page_range):
    for page in range(page_range-50,page_range):
        url = f'https://turbo.az/autos?page={page}'
        thread = threading.Thread(target=data_collector, args=(url,))
        thread.start()


def data_collector(url):
    global count
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    announcements = soup.find_all("a", {"class": "products-i__link"})

    for announcement in announcements:
        try:
            r = requests.get("https://turbo.az"+announcement["href"])
            soup = bs4.BeautifulSoup(r.text, 'html.parser').find_all("div", {"class": "product-properties-value"})
            with open('data.txt','a') as f:
                f.write('{},{},{},{},{},{},{},{}\n'.format(soup[1].get_text() , soup[2].get_text() , (str(int(soup[3].get_text())-2021))
                                                        ,soup[6].get_text()[:-2] , soup[8].get_text() , soup[9].get_text()[:-3] , soup[10].get_text() , soup[13].get_text()  ))
                print(f"car number {count} was added")
                count+=1
        except: print("https://turbo.az"+announcement["href"])      


def main():
    for page_range in range(50+1,1500,50):
        thread(page_range)
        print(f"Page_Range number{page_range} was completed")

main()                    


