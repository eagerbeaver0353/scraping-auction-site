from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
from .utils import extract_int, extract_float, filter_str

base_url = "https://storageauctions.com"
search_url = "/auction-unit/find-auctions?AuctionsUnitsSearch%5Bradius%5D={radius}&AuctionsUnitsSearch%5Bpage_size%5D=&AuctionsUnitsSearch%5Bzip_city_state%5D={zipcode}&item_count=${count}&page=1&per-page={count}"


def generate_url(zipcode, miles, count=12):
    return base_url + search_url.format(radius=miles, zipcode=zipcode, count=count)


def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup


def get_auction_detail(url):
    soup = get_soup(url)
    print(url)
    result = {}
    result["_id"] = extract_int(url)
    result["name"] = filter_str(
        soup.select("#web_details .col-md-3.col-sm-6 strong")[0].get_text()
    )
    result["location"] = filter_str(
        soup.select("#web_details .col-md-3.col-sm-6 small")[0].get_text()
    )
    
    images = soup.select(".auction-slider #bxslider_HRD img")
    result["image_url"] = []
    for image in images:
        result["image_url"].append(image.attrs["src"])

    result["close_date"] = filter_str(
        soup.select(".auction-slider .bid-wrap h4 strong")[0].get_text()
    )

    info_table = soup.select("#unit-details-tbl")[0]
    result["current_bid"] = extract_float(info_table.get_text())
    result["unit_size"] = filter_str(
        info_table.select("tr")[3].select("td")[0].get_text(), "\d+x\d+"
    )
    result["unit_content"] = (
        soup.select(".additional-info .col-md-6")[0].select("p")[0].get_text()
    )
    return result


def get_auction_detail_urls(url):
    soup = get_soup(url)
    print("Get auctions web content loaded")

    image_list = soup.select("ul.main-list-wrap img")
    res_urls = []
    for image in image_list:
        try:
            split_list = image.attrs["onclick"].split(" ")
            res_urls.append(split_list[2].replace('"', ""))
        except:
            pass

    return res_urls


def get_total_auctions(url):
    soup = get_soup(url)
    print("Get first auction web content loaded")

    div_totalauctions = soup.select(
        "#find_auction_units .search-wrap-content.pull-left"
    )
    total = 0
    try:
        total = extract_int(div_totalauctions[0].get_text())
    except:
        pass
    return total


def search_auctions(zipcode, miles):
    total_auctions = get_total_auctions(generate_url(zipcode, miles))
    print("Total:", total_auctions)

    return get_auction_detail_urls(generate_url(zipcode, miles, total_auctions))


# city_list = soup.find_all("td", classs_ ="city")
