#!/usr/bin/env python3
"""
上传封面图并创建公众号草稿。
用法: python3 publish_draft.py --title "标题" --author "作者" --digest "摘要" --content-file article.html --cover cover.jpg
需要环境变量: WX_APPID, WX_APPSECRET
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request


def get_access_token(appid, appsecret):
    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={appsecret}"
    resp = urllib.request.urlopen(url)
    data = json.loads(resp.read().decode('utf-8'))
    if 'access_token' not in data:
        print(f"Error getting token: {data}", file=sys.stderr)
        sys.exit(1)
    return data['access_token']


def upload_image(token, image_path):
    result = subprocess.run([
        'curl', '-s', '-X', 'POST',
        f'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image',
        '-F', f'media=@{image_path}'
    ], capture_output=True, text=True)
    data = json.loads(result.stdout)
    if 'media_id' not in data:
        print(f"Error uploading image: {data}", file=sys.stderr)
        sys.exit(1)
    return data['media_id']


def create_draft(token, title, author, digest, content, thumb_media_id):
    data = {
        "articles": [{
            "title": title,
            "author": author,
            "digest": digest,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0
        }]
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    req = urllib.request.Request(
        url,
        data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode('utf-8'))
    if 'media_id' not in result:
        print(f"Error creating draft: {result}", file=sys.stderr)
        sys.exit(1)
    print(f"Draft created! media_id: {result['media_id']}")
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='创建公众号草稿')
    parser.add_argument('--title', required=True, help='文章标题')
    parser.add_argument('--author', default='', help='作者')
    parser.add_argument('--digest', default='', help='文章摘要')
    parser.add_argument('--content-file', required=True, help='HTML内容文件路径')
    parser.add_argument('--cover', required=True, help='封面图路径')
    parser.add_argument('--appid', default=None, help='AppID（或设置 WX_APPID 环境变量）')
    parser.add_argument('--appsecret', default=None, help='AppSecret（或设置 WX_APPSECRET 环境变量）')
    args = parser.parse_args()

    appid = args.appid or os.environ.get('WX_APPID')
    appsecret = args.appsecret or os.environ.get('WX_APPSECRET')
    if not appid or not appsecret:
        print("Error: AppID and AppSecret required (--appid/--appsecret or WX_APPID/WX_APPSECRET)", file=sys.stderr)
        sys.exit(1)

    with open(args.content_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    print("Getting access token...")
    token = get_access_token(appid, appsecret)

    print("Uploading cover image...")
    thumb_id = upload_image(token, args.cover)

    print("Creating draft...")
    create_draft(token, args.title, args.author, args.digest, content, thumb_id)
    print("Done!")
