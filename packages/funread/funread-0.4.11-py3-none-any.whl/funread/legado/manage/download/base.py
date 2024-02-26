import json
import os

import pandas as pd
import requests
from funfile import pickle, funos
from funread.legado.manage.utils import url_to_hostname
from funsecret import get_md5_str
from tqdm import tqdm


class DownloadSource(object):
    def __init__(self, path='./funread-hub', cate1='book', *args, **kwargs):
        self.path_bak = f'{path}/{cate1}/bak'
        self.path_pkl = f'{path}/{cate1}/pkl'
        self.path_bok = f'{path}/{cate1}/source'
        self.pkl_url = f"{self.path_pkl}/url_info.pkl.bz2"
        self.pkl_md5 = f'{self.path_pkl}/source_info.pkl.bz2'

        self.url_map = {}
        self.md5_set = {}
        self.current_id = 1

        funos.makedirs(self.path_bak)
        funos.makedirs(self.path_bok)
        funos.makedirs(self.path_pkl)

    def loads(self):
        print("loads")

        if os.path.exists(self.pkl_url):
            df = pd.read_pickle(self.pkl_url, compression='infer')
            self.url_map = {k: v for k, v in df.values}
        else:
            self.url_map = {"https://farfarfun.github.com": 100000}
        self.current_id = max(self.url_map.values())
        if os.path.exists(self.pkl_md5):
            df = pd.read_pickle(self.pkl_md5, compression='infer')
            self.md5_set = {info['md5']: info for info in df.to_dict(orient='records')}

    def dumps(self):
        print("dumps")

        df = pd.DataFrame([{"url": k, "url_id": v} for k, v in self.url_map.items()])
        df.to_pickle(self.pkl_url, compression='infer')

        df = pd.DataFrame(self.md5_set.values())
        df.to_pickle(self.pkl_md5, compression='infer')

    def url_index(self, url):
        if url in self.url_map:
            return self.url_map[url]
        else:
            self.current_id += 1
            self.url_map[url] = self.current_id
            return self.current_id

    def source_format(self, source):
        pass

    def add_sources(self, data, *args, **kwargs):
        ""
        if isinstance(data, str):
            if data.startswith("http"):
                data = requests.get(data).json()
            elif os.path.exists(data):
                data = pickle.load(data)
            elif data[0] == '[' or data[0] == '{':
                data = json.loads(data)

        for source in tqdm(data):
            md5 = get_md5_str(json.dumps(source))
            source = self.source_format(source)
            hostname = url_to_hostname(source['bookSourceUrl'])
            url_id = self.url_index(hostname)

            cate1 = (url_id // 100) * 100
            fdir = f"{self.path_bok}/book/{cate1}-{cate1 + 100}/"
            if not os.path.exists(fdir):
                os.makedirs(fdir)
            fpath = f"{fdir}/{url_id}.json"

            self.add_source_to_candidate(md5, fpath, source)
            self.md5_set[md5] = {
                "md5": md5,
                "url_id": url_id,
                "hostname": hostname,
                "cate1": cate1,
                "pkl_md5": fpath,
            }

    def add_source_to_candidate(self, md5, fpath, source):
        if os.path.exists(fpath):
            data = json.loads(open(fpath, 'r').read())
        else:
            data = {"merged": {"md5_list": [], "source": {}}, "candidate_list": {}}

        if len(data["merged"]["md5_list"]) == 0 and len(data["merged"]["source"]) == 0:
            data["merged"]["md5_list"].append(md5)
            data["merged"]["source"] = source
        elif md5 not in data["merged"]["md5_list"] and md5 not in data["candidate_list"].keys():
            data['candidate_list'][md5] = source

        with open(fpath, "w") as fw:
            fw.write(json.dumps(data, sort_keys=True, indent=4))

    def __enter__(self):
        self.loads()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dumps()
