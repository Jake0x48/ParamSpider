import requests
import random
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def connector(url):
    result = False
    user_agent_list = [
        # Chrome
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        # Firefox
        "Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)",
    ]
    user_agent = random.choice(user_agent_list)
    headers = {"User-Agent": user_agent}

    try:
        # TODO control request headers in here
        response = requests.get(
            url, headers=headers, timeout=30, verify=False, stream=True
        )
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
        data2 = ""
        with open("test.dat", "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                data2 += data.decode("utf-8")
                data3 = data2.split("\n")
                file.write(data)
                result = "\n".join(data3)
        if os.path.exists("test.dat"):
            os.remove("test.dat")
        progress_bar.close()


        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")
        retry = False
        response.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        retry = False
        print(
            "\u001b[31;1mCan not connect to server. Check your internet connection.\u001b[0m"
        )
    except requests.exceptions.Timeout as e:
        retry = True
        print("\u001b[31;1mOOPS!! Timeout Error. Retrying in 2 seconds.\u001b[0m")
        time.sleep(2)
    except requests.exceptions.HTTPError as err:
        retry = True
        print(f"\u001b[31;1m {err}. Retrying in 2 seconds.\u001b[0m")
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        retry = True
        print("\u001b[31;1m {e} Can not get target information\u001b[0m")
        print(
            "\u001b[31;1mIf you think this is a bug or unintentional behaviour. Report here : https://github.com/devanshbatham/ParamSpider/issues\u001b[0m"
        )
    except KeyboardInterrupt as k:
        retry = False
        print("\u001b[31;1mInterrupted by user\u001b[0m")
        raise SystemExit(k)
    finally:
        return result, retry
