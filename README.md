# youtube_subscriptions
STA260 final project: YouTubers' weekly subscriptions and video views since the Covid19 pandemic

## Setup
Steps for collecting url and name of the Youtuber of interest:
* Find the account name of the Youtuber as shown in their channel
* Search for this Youtuber in https://socialblade.com/youtube/
* In the homepage, click on "See full monthly statistics" to go to the detailed statistics page. 
* Now the url should end with "/monthly". Copy this url and got to https://web.archive.org/.
* In the "save page now" section, enter the url you just copied and save the page. 
* After the page is saved, you will see on the screen "visit page: [url]". Copy that link and put it into the 'url' column of the google sheet.
* The 'name' column on the google sheet is the account name as shown in the url, right before '/monthly'. NOT the youtube channel's name.
  *  E.g. url: https://web.archive.org/web/20220521004032/https://socialblade.com/youtube/user/pamelarf1/monthly, name: pamelarf1.

## Web scraping
Under code, there is a scraper_batch.py file which could be used to batch scraping the websites after we collected the urls and names and compile them into the library.csv file under data. If you want to try scraping a single website, you can use the scraper_revised.py file. It will ask you to input the url and name of a single website you want to scrape. To avoid any conflicts, please do not push any scraped data to this repo until we finalized the list of urls. 
