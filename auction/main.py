from .auctions.scrape import get_auction_detail, search_auctions, base_url
from .auctions.store import insert_data, update_data, get_specific_auction, count_table
from .auctions.gen_html import write_html, generate_html
from .auctions.email import send_email
from .auctions.utils import is_auction_equal
import webbrowser
from datetime import datetime
import os

# search_auctions(5027, 10)
# print(
#     get_auction_detail("https://storageauctions.com/auction-unit/unit-details/399452")
# )


def start_scraping(zipcode = 38060, miles = 90):
    auction_urls = search_auctions(zipcode, miles)
    # auction_urls = ["/auction-unit/unit-details/397756", "/auction-unit/unit-details/399301","/auction-unit/unit-details/403271","/auction-unit/unit-details/399302","/auction-unit/unit-details/403272"]
    new_auctions = []
    changed_count, removed_count, new_count = 0, 0, 0
    
    for detail_url in auction_urls:
        auction_detail = get_auction_detail(base_url + detail_url)
        try: 
            auction_from_db = get_specific_auction(auction_detail)
            if auction_from_db is not None : 
                if is_auction_equal(auction_from_db, auction_detail) == False:
                    update_data(auction_detail)
                    changed_count += 1
                continue
            insert_data(auction_detail)
            new_auctions.append(auction_detail)
        except:
            pass
    
    changed_count, removed_count, new_count = changed_count, count_table() - len(auction_urls), len(new_auctions)

    file_name = "reports/" + datetime.today().strftime('%Y%m%d%H%M') + "-" + str(zipcode) + "-" + str(miles) + ".html"
    write_html(file_name, generate_html(new_auctions))
    # webbrowser.open('file://' + os.path.realpath(file_name))
    
    send_email(
"""
New Auctions:\t {_new}
Changed Auctions:\t {_changed}
Removed Auctions:\t {_removed}
""".format(_new = new_count, _removed = removed_count, _changed = changed_count), 
        file_name
    )
    

if(__name__ == "__main__"):
    
    zipcode = input("Enter a zipcode: ")
    miles = 10
    while 1:
        try:
            miles = int(input("Enter a radius(mile): "))
            break
        except:
            print("Please input valid number")
            continue
   
    start_scraping(zipcode, miles)
    # print(str(3.5668786))
    # print(is_exist({"_id": 402124}))
    # insert_data({'_id': 402123, 'name': 'Halls Storage # 113049-402123', 'location': '4509 E. Emory Rd,   Knoxville,  TN,  37938', 'image_url': '/uploads/auctions_unit/402123/1440_810//HoneyCreekProperties_4 Of JulyAuction_Unit_402123_2497071.jpeg', 'close_date': '07/04/2023 05:06 PM EST', 'current_bid': 90.0, 'unit_size': '10x10', 'unit_content': 'This unit appears to contain…Unit is full to the brim with furniture, decor, clothing items, home decor, bed, mattresses, and other hidden treasures.'})