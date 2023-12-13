import htmlgenerator as hg
from .scrape import base_url
from datetime import datetime

def generate_image(image_url, is_active = False):
    return hg.DIV(
        hg.IMG(
            src=base_url + image_url,
            style="object-fit: contain;",
            _class="h-100 w-100"
        ),
        _class = "carousel-item" + (" active" if is_active == True else ""),
    )

def generate_card(auction_detail):
    generated_images = hg.DIV(_class="carousel-inner")
    
    firstNotPassed = True
    for image in auction_detail["image_url"]:
        generated_images.append(generate_image(image, firstNotPassed))
        firstNotPassed = False
        
    _id = auction_detail["_id"]

    return hg.DIV(
        hg.DIV(
            generated_images,
            hg.BUTTON(
                hg.SPAN(_class="carousel-control-prev-icon"),
                _class="carousel-control-prev",
                type="button",
                data_bs_target="#demo" + str(_id),
                data_bs_slide="prev"
            ),
            hg.BUTTON(
                hg.SPAN(_class="carousel-control-next-icon"),
                _class="carousel-control-next",
                type="button",
                data_bs_target="#demo" + str(_id),
                data_bs_slide="next"
            ),
            id="demo" + str(_id),
            _class="carousel slide col-4 bg-black",
            data_bs_ride="carousel"
        ),
        hg.DIV(
            hg.H4(
                auction_detail["name"],
                _class="card-title"
            ),
            hg.H6(
                auction_detail["location"],
                _class="card-text"
            ),
            hg.P(
                "Closes on ",
                hg.STRONG(auction_detail["close_date"]),
                _class="card-text"
            ),
            hg.P(
                "Current bid: ",
                hg.STRONG("$" + str(auction_detail["current_bid"])),
                _class="card-text"
            ),
            hg.P(
                "Unit size: ",
                hg.STRONG(auction_detail["unit_size"]),
                _class="card-text"
            ),
            hg.P(
                "Unit content: ",
                hg.SMALL(auction_detail["unit_content"]),
                _class="card-text",
                style="overflow-y:auto;border-top: 3px solid lightgray;"
            ),
            _class="col-8 px-4 d-flex flex-column",
        ),
        _class="card col-12 px-4 py-4",
        style="height:350px;flex-direction:row",
    )

def generate_html(auctions) :
    generated_div = hg.DIV(_class="row")
    for auction in auctions:
        generated_div.append(generate_card(auction))
    return  hg.HTML(
        hg.HEAD(
            hg.TITLE(datetime.today().strftime('%Y-%m-%d %H:%M') + " - Report"),
            hg.LINK(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
                rel="stylesheet"
            ),
            hg.SCRIPT(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
            )
        ),
        hg.BODY(
            hg.DIV(
                generated_div,
                _class="container mt-3"
            )
        )
    )

def write_html(filename = "output.html", page = hg.HTML()): 
    # Write the HTML markup to a file
    with open(filename, "w") as file:
        file.write(hg.render(page, {}))