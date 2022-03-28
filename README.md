## ParamSpider: fork by Jake0x48

### key changes:

 - cleaner output
 - much faster
 - removed some options i wasnt using
 - improved logging
 - progress bar :)

  

### usage instructions:


Note : Use python 3.7+

```
git clone https://github.com/Jake0x48/ParamSpider
```
```
cd ParamSpider
```
```
pip3 install -r requirements.txt
```
```
python3 paramspider.py --domain hackerone.com
```


  

### usage options:

```
usage: paramspider.py [-h] -d DOMAIN [-s SUBS] [-e EXCLUDE] [-o OUTPUT] [-q] [-r RETRIES]

ParamSpider a parameter discovery suite

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain name of the taget [ex : hackerone.com]
  -s SUBS, --subs SUBS  Set False for no subs [ex : --subs False ]
  -e EXCLUDE, --exclude EXCLUDE
                        extensions to exclude [ex --exclude php,aspx]
  -o OUTPUT, --output OUTPUT
                        Output file name [by default it is 'domain.txt']
  -q, --quiet           Do not print the results to the screen
  -r RETRIES, --retries RETRIES
                        Specify number of retries for 4xx and 5xx errors
```

## example (quiet):

```
$ python3 paramspider.py -d bugcrowd.com -e swf,gif,jpg,js,css,png,jpeg,woff,ttf,svg,eot -q
```

  ![example](https://user-images.githubusercontent.com/22352400/160432470-99e5eb14-94d5-46fd-a1c4-129a31d0eaa3.PNG) 
  

### support the riginal creator here:

twitter: [0xAsm0d3us](https://twitter.com/0xAsm0d3us)
donate: [Buy me a Coffee here](https://www.buymeacoffee.com/Asm0d3us)
