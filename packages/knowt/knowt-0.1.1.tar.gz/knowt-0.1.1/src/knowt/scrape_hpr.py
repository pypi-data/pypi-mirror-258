import bs4
import pandas as pd
import requests
from tqdm import tqdm
import numpy as np
from knowt.constants import DATA_DIR
import json

HPR_CSV_PATH = DATA_DIR / 'corpus_hpr' / 'hpr_podcasts.csv.gz'
BASE_URL = 'https://hackerpublicradio.org'


def scrape_index(url=f'{BASE_URL}/eps/index.html'):
    resp = requests.get(url)
    bs = bs4.BeautifulSoup(resp.text, features="html.parser")
    episodes = [
        [ep['href'], ep.text, ep.next_sibling.next_sibling['href'], ep.next_sibling.next_sibling.text]
        for ep in bs.find_all('a') if ep.get('href', '').startswith('./eps/hpr')
    ]
    df = pd.DataFrame(episodes, columns='url full_title user_url user'.split())
    df = df.sort_values('url')
    df = df.reset_index(drop=True)
    df['seq_num'] = df.index.values + 1
    df['title'] = df['full_title'].str.split('::').str[-1]
    return df['seq_num title url user user_url full_title'.split()]


def scrape_episode(url='./eps/hpr0030/', base_url=BASE_URL):
    if url.lstrip('.').lstrip('/').startswith('eps/hpr'):
        url = '/'.join([base_url, url.lstrip('.').lstrip('/')])
    resp = requests.get(url)
    s = bs4.BeautifulSoup(resp.text, features="html.parser")
    title, comments = s.find_all('h1')[1:3]
    subtitle, series = s.find_all('h3')[1:3]
    show_notes = list(series.next_siblings)[-1].next.next_sibling
    links = list(series.parent.find_all('a'))
    tags = [
        a.text for a in links
        if a.get('href', '').lstrip('.').lstrip('/').startswith('tags.html#')
    ]
    audio_urls = [a.get('href', '') for a in links if (a.text.lower().strip()[-3:] in 'ogg spx mp3')]
    row = dict(
        url=url.replace(base_url, '.'),
        full_title_4digit=title.text,
        subtitle=subtitle.text,
        series=series.text,
        audio_urls=audio_urls,
        show_notes=show_notes.text,
        tags=tags)
    series.parent.find_all('a')
    return row


def parse_urls(df, base_url=BASE_URL):
    df['seq_num'] = df['url'].str.split('/').str[-2].str[3:].astype(int)
    df['url'] = df['url'].str.replace(base_url, '.')
    return df


def coerce_to_list(obj):
    if isinstance(obj, (tuple, set, np.ndarray)):
        return list(obj)
    if not isinstance(obj, (list, str)) and not obj:
        return []
    if isinstance(obj, str):
        obj = obj.strip().lstrip('[').rstrip(']').split(',')
        return [u.strip().strip('"').strip("'").strip() for u in obj]


def json_loads(obj):
    if obj is None:
        return np.nan
    if isinstance(obj, (tuple, set, np.ndarray)):
        return list(obj)
    if not isinstance(obj, (list, str)) and not obj:
        return []
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            # FIXME: need to also deal with Python syntax dicts (single-quoted keys or values)
            if obj[0] in '[({':
                return coerce_to_list(obj)
    return str(obj)


if __name__ == '__main__':
    dfold = pd.read_csv(HPR_CSV_PATH).sort_values('url')
    dflatest = scrape_index().sort_values('url')
    scraped_urls = sorted(dfold['url'].str.strip().unique())
    episodes = []
    for i, row in tqdm(dflatest.iterrows()):
        row = row.to_dict()
        urls = row['audio_urls']
        if not isinstance(urls, list):
            urls = coerce_to_list(urls)
        url = row['url']
        if url in scraped_urls:
            continue
        row.update(scrape_episode(row['url']))
        episodes.append(row)
        scraped_urls += episodes[-1]['url'].strip()

    if len(episodes) == len(dflatest):
        dflatest = dflatest.set_index('url', drop=False).to_dict()
        for i, episode in tqdm(episodes):
            episode['url'] = episode['url'].replace(BASE_URL, '.')
            dflatest[episode['url']].update(episode)
        dflatest = pd.DataFrame(dflatest)
    else:
        dflatest = pd.concat([dfold, pd.DataFrame(episodes)], axis=0)
    dflatest = parse_urls(dflatest)
    dflatest = dflatest.sort_values('url')
    dflatest = dflatest.reset_index(drop=True)
    dflatest['url'].str.replace(BASE_URL, '.')
    # FIXME:
    # parse list of audiourls skipping "corresponents.html"
    # dropduplicates
    # e.g. newcols.append({u[-3:].lower(): u for u in urls})
    dflatest.to_csv(HPR_CSV_PATH, index=None)
