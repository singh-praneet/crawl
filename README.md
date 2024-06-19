# crawl

crawler.py contains a python3 script which will download images from a given webpage and recursively from all the links on that page depending on the arguments provided while running the script.

To run it on a simple cli, few settings need to be done on the machine where it will be run.

Basically this script should be run using python3 with the arguments passed over when `crawl` on command line is invoked.

The way this script is written, it takes two command line argument, with the following syntax.
crawl <start_url> <depth>
start_url - page where crawling starts 
depth - the crawl child pages depth where 1 is only the page given in start_url

The results are placed in a folder called images which also contains index.json, a json file shows the list of the collected image in the following format:
{
"images":[{"url":<the image url>, "page":<the url of the page the image was found>, depth:<the depth of the page>}]
}
