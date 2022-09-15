# Google Maps Crawler
Google Maps Crawler takes Google Maps List and it scrape elements from all items such as: title, rating, reviews, location url, website,etc.

Google Maps List Example: https://www.google.com/search?q=football+stadiums+in+england&rlz=1C5CHFA_enRS980RS980&biw=1440&bih=704&tbm=lcl&ei=Dh8jY_TPEN6D9u8P3oiw-Ao&oq=football+stadiums+in+england&gs_l=psy-ab.3..0i512k1l3j0i30i22k1l7.15749.18712.0.18802.28.16.0.5.5.0.230.1711.3j9j1.13.0....0...1c.1.64.psy-ab..10.18.1724...0i67k1j0i273k1j0i512i457k1j0i402k1j0i390k1j0i30i22i10k1.0.kh43omIYycU#rlfi=hd:;si:;mv:[[54.0856624,0.9251977000000001],[50.9307963,-3.2484374]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:1

This is the list of all football stadiums in England. You can pass this URL to Crawler and it will scrape all stadiums from the list.

# How to use it?
Define crawler as crawler = GMapsCrawler()

Call function crawl_page(Provide URL to Google Maps List)

Transform your results to pandas Dataframe or JSON file by calling crawler.transform_to_dataframe() or crawler.transform_to_json() functions.
