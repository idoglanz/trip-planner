import re
import requests
import gzip
from datetime import datetime
import glob

def fetch_todays_price_list():
    req = requests.get('http://prices.shufersal.co.il/FileObject/UpdateCategory?storeId=413')
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', str(req.content))
    full_list_url = [url for url in urls if 'PriceFull' in url]

    if full_list_url:
        full_url_req = full_list_url[0].replace('amp;','')
    else:
        return False

    full_price_ = requests.get(full_url_req, allow_redirects=True)

    # save the file
    filename = f'./data/price_lists/PriceFull-{datetime.now().strftime("%Y%m%d")}.gzip'

    open(filename, 'wb').write(full_price_.content)
    # unzip the file
    with gzip.open(filename, 'rb') as f_in:
        file_content = f_in.read()

    filename = filename.replace('.gzip', '.xml')
    with open(filename, 'wb') as f_out:
        f_out.write(file_content)
    
    return filename


def get_latest_price_list_from_dir(dir):

    def extract_timestamp_from_filename(filename):
        return datetime.strptime(filename.split('-')[-1].split('.')[0], '%Y%m%d')
    
    list_of_files = glob.glob(dir + '/*.xml') # * means all if need specific format then *.csv
    if not list_of_files:
        return None, None
    latest_file = max(list_of_files, key=lambda x: extract_timestamp_from_filename(x))
    return latest_file, extract_timestamp_from_filename(latest_file)


def get_price_list_filename():
    filename, ts = get_latest_price_list_from_dir('./data/price_lists')

    if filename is None or ts.date() < datetime.now().date():
        print(f'Price list is not up to date ({ts}) or none available, fetching new list')
        filename = fetch_todays_price_list()
    
    return filename


if __name__ == "__main__":
    filename = get_price_list_filename()
    print(f'filename: {filename}')