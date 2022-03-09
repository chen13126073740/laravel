import hashlib
import json
import os
import re
import time

from lib.Mysql import Mysql
from lib.UUID import UUID
from datetime import datetime, timedelta, timezone


class Main:

    def start(self):
        self.init()
        self._article_db = Mysql('articles')
        self._tag_category_db = Mysql('tag_categories')
        self._tag_db = Mysql('tags')
        self._asset_db = Mysql('assets')
        self._asset_tag_db = Mysql('asset_tag')
        self._asset_tags_db = Mysql('asset_tags')
        self._article_tag_db = Mysql('article_tag')

        dir = './data/pages/page/'
        files = os.listdir(dir)
        files = self.sort_strings_with_emb_numbers(files)

        for file in files:
            print(file)
            time.sleep(1)
            file_type = os.path.splitext(dir + file)
            if file_type[1] == '.json':
                with open(dir + file, 'r') as f:
                    res = f.read()
                    obj = json.loads(res)
                    self.action(obj)

    def emb_numbers(self, s):
        re_digits = re.compile(r'(\d+)')
        pieces = re_digits.split(s)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    def sort_strings_with_emb_numbers(self, alist):
        return sorted(alist, key=self.emb_numbers)

    def init(self):
        self.tag_categories = [
            {
                'name': '分类',
                'id': '3cac5c9b1241721f74d6c99ec135fe3a'
            }
        ]

    def action(self, obj):
        self.article(obj)

        # self.tag_category()
        pass

    def article(self, obj):
        id = self.id(obj['name_on'])
        # print(id)
        data = {
            'id': id,
            'author': obj['name_on'],
            'title': obj['title'],
            'subtitle': obj['title'],
            'type': 'net',
            'cover': self.format_icon(obj['icon_path']),
            'description': obj['description'],
            'click_count': '0'
        }
        self._article_db.updateOrCreate({
            # 'id': id,
            'title': obj['title']
        }, data)
        self.tag(id, obj)
        self.asset(id, obj)

    def tag_category(self):
        for category in self.tag_categories:
            name = category['name']
            self._tag_category_db.updateOrCreate({
                'id': category['id']
            }, {
                'id': category['id'],
                'name': name,
                'type': '1'
            })

    def tag(self, article_id, obj):
        tags = obj['tags']['categories']

        for tag in tags:
            category_id = '3cac5c9b1241721f74d6c99ec135fe3a'
            tag_id = self.id(tag)
            self._tag_db.updateOrCreate({
                'id': tag_id
            }, {
                'id': tag_id,
                'name': tag,
                'name_en': tag,
                'category_id': category_id
            })

            self._article_tag_db.updateOrCreate({
                'article_id': article_id,
                'tag_id': tag_id
            }, {
                'article_id': article_id,
                'tag_id': tag_id
            })

    def asset(self, article_id, obj):
        images = obj['images']
        # print(images)
        for image in images:
            id = self.id(image['title'] + image['no'])
            self._asset_db.updateOrCreate({
                'id': id
            }, {
                'id': id,
                'article_id': article_id,
                'url': self.format_asset(image['src']),
                'small_url': self.format_asset_small(image['src']),
                'medium_url': self.format_asset_medium(image['src']),

                'md5': id,
                'asset_id': id,
                'name': image['title']
            })

            asset_tag = image['tags']
            for tags in asset_tag:
                for tag in tags['tags']:
                    tag_id = self.id(tag)
                    self._asset_tags_db.updateOrCreate({
                        'id': tag_id
                    }, {
                        'id': tag_id,
                        'name': tag,
                        'name_en': tag
                    })
                    self._asset_tag_db.updateOrCreate({
                        'asset_id': id,
                        'tag_id': tag_id
                    }, {
                        'asset_id': id,
                        'tag_id': tag_id
                    })

    def format_asset(self, url):
        return url.replace('images/', 'storage/images/')

    def format_asset_medium(self, url):
        return url.replace('images/', 'storage/medium_images/medium_')

    def format_asset_small(self, url):
        return url.replace('images/', 'storage/small_images/small_')

    def format_icon(self, url):
        if url == '':
            return None
        return 'storage/' + url

    def filter(self, str):
        # str = str.replace("\\u", '')
        str = str.replace("'", '\'')
        return str.strip()

    def _now(self):
        utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        cn_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
        return cn_dt.strftime('%Y-%m-%d %H:%M:%S')

    def id(self, key=None):
        if key is None:
            return UUID.id()
        else:
            hl = hashlib.md5()
            hl.update(('net_' + key).encode(encoding='utf-8'))
            return hl.hexdigest()
