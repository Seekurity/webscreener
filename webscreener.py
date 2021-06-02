from selenium import webdriver
import os
import datetime
import sys
import argparse

__author__='Seif Elsallamy'

__version__='1.0 alpha'

__url__='https://github.com/Seekurity/webscreener'


__description__='''\
___________________________________________
webscreener mass website snapshooter
webscreener v.'''+__version__+'''
Author: '''+__author__+'''
Github: '''+__url__+'''
___________________________________________
'''


def print_banner():
    print """ _       __     __   _____                                    
| |     / /__  / /_ / ___/_____________  ___  ____  ___  _____
| | /| / / _ \/ __ \\__ \/ ___/ ___/ _ \/ _ \/ __ \/ _ \/ ___/
| |/ |/ /  __/ /_/ /__/ / /__/ /  /  __/  __/ / / /  __/ /    
|__/|__/\___/_.___/____/\___/_/   \___/\___/_/ /_/\___/_/     
                                                              """+__version__+""""""

#Program start

def runDriver(): #strat chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1366x768')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome("chromedriver", chrome_options=options)
    return driver



def main():
    os.chdir(sys.argv[0] + "/../")

    try:
        targetList=sys.argv[1] #get target list

    except:
        print "usage:>webscreener.py <targetsListFile>\n"
        print "targetsList content example:\n"
        print "domain.com\nsubdomain.com\nsub2.domain2.com\nsub.domain3.com\n..."
        exit(1)

    with open(targetList,"r") as f: # read the target file
        c=f.readlines()
        c=list(set(c))
        
    filename = "ws_"+str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')+".html" # create html file
    with open(filename, "a") as f: # put html script & css
        scripts="""
<style>
body {
  display: flex;
  flex-wrap: wrap;
}

div {
  width: 50%;
}

@media(max-width: 300px) {
  .box {
     width: 100%;
   }
}


img {
  border: 5px solid #555;
  cursor: pointer;
}
</style>
<script>
function imgSize(x){
if (x.width === 600){
x.removeAttribute("width");
x.style="z-index: 10;position: absolute;";
}
else {
x.width = 600;
x.removeAttribute("style");
}
}
</script>"""
        f.write(scripts)
    if not os.path.exists("images"): # check if images folder exists, if not create it.
        os.makedirs("images")



    
    print __description__ 
    print_banner()
    
    driver = runDriver()
    with open(filename, "a") as f: #take screenshots from the targets and save them, then put them to the html file.
        for u in range(len(c)):
            url = c[u]
            url="https://"+url
            try:
                driver.get(url)
            except:
                print url.replace("\n","") + " is down"
                continue
            link = "images/" + c[u].replace("\n","").replace("\r","")+'.png'
            screenshot = driver.save_screenshot(link)
            elm = '<div><a target="_blank" href="'+url+'">'+url+'</a>' + '<br><img onclick="imgSize(this)" width="600px" src="'+link+'"></div>'
            f.write(elm)
    driver.quit()
    print "The file is saved in " + os.path.dirname(os.path.abspath(filename))+"\\"+filename 
    


main()


