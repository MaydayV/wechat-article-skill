#!/usr/bin/env python3
"""
上传封面图并创建公众号草稿。

用法:
  python3 publish_draft.py \
    --title "标题" \
    --author "作者" \
    --digest "摘要" \
    --content-file article.html \
    --cover cover.jpg \
    --appid <APPID> \
    --appsecret <APPSECRET>

也支持环境变量:
  WX_APPID, WX_APPSECRET, WX_AUTHOR
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import mimetypes
import uuid
from typing import Dict, List, Optional


def fail(msg, code=1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


SOCKS_PROXY = os.environ.get("WX_PROXY")


def get_proxy_handler():
    if SOCKS_PROXY:
        if SOCKS_PROXY.startswith("socks5h://"):
            try:
                import socks
                import socket
                # Monkey patch socket to use socks proxy
                socks.set_default_proxy(socks.SOCKS5, SOCKS_PROXY.split("://")[1].split(":")[0], int(SOCKS_PROXY.split(":")[-1]))
                socket.socket = socks.socksocket
                return urllib.request.ProxyHandler({}) # 空 ProxyHandler，因为 socket 已经被打补丁
            except ImportError:
                print("警告: WX_PROXY 配置了 socks5h，但未安装 PySocks 库。请运行 `pip install PySocks`。", file=sys.stderr)
                print("将尝试直接连接，可能导致连接失败。", file=sys.stderr)
        elif SOCKS_PROXY.startswith("http://") or SOCKS_PROXY.startswith("https://"):
            return urllib.request.ProxyHandler({"http": SOCKS_PROXY, "https": SOCKS_PROXY})
        else:
            print(f"警告: 不支持的代理协议: {SOCKS_PROXY}。将尝试直接连接。", file=sys.stderr)
    return None

_proxy_handler = get_proxy_handler()
_opener = urllib.request.build_opener(_proxy_handler) if _proxy_handler else urllib.request.build_opener()
urllib.request.install_opener(_opener)

def http_request_json(url, data=None, method="GET", timeout=30):
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            resp_data = resp.read().decode("utf-8")
            return json.loads(resp_data)
    except urllib.error.URLError as e:
        fail(f"HTTP request failed to {url}: {e}")
    except Exception as e:
        fail(f"HTTP request returned non-json or other error: {e}")

def http_get_json(url, timeout=30):
    return http_request_json(url, method="GET", timeout=timeout)

def http_post_json(url, payload, timeout=30):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return http_request_json(url, data=data, method="POST", timeout=timeout)


def get_access_token(appid, appsecret):
    q = urllib.parse.urlencode(
        {
            "grant_type": "client_credential",
            "appid": appid,
            "secret": appsecret,
        }
    )
    url = f"https://api.weixin.qq.com/cgi-bin/token?{q}"
    data = http_get_json(url)
    if "access_token" not in data:
        fail(f"get token failed: {data}")
    return data["access_token"]


def _upload_file(token, upload_url, image_path, file_type):
    """通用文件上传函数"""
    boundary = uuid.uuid4().hex
    mime_type = mimetypes.guess_type(image_path)[0] or "application/octet-stream"
    filename = os.path.basename(image_path)

    with open(image_path, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    req = urllib.request.Request(
        upload_url,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        fail(f"upload {file_type} failed: {e}")
    return data


def upload_cover(token, image_path):
    """Upload cover image (thumb_media_id)."""
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    data = _upload_file(token, url, image_path, "cover")
    if "media_id" not in data:
        fail(f"upload cover failed: {data}")
    return data["media_id"]


def upload_image_to_content(token, image_path):
    """Upload image for article content."""
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    data = _upload_file(token, url, image_path, "content image")
    if "url" not in data:
        fail(f"upload image to content failed: {data}")
    return data["url"]


def create_draft(token, title, author, digest, content, thumb_media_id, need_open_comment, only_fans_can_comment):
    payload = {
        "articles": [
            {
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": int(need_open_comment),
                "only_fans_can_comment": int(only_fans_can_comment),
            }
        ]
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    data = http_post_json(url, payload)
    if "media_id" not in data:
        fail(f"create draft failed: {data}")
    return data


def ensure_file(path, name):
    if not path:
        fail(f"{name} path is empty")
    if not os.path.exists(path):
        fail(f"{name} not found: {path}")
    if not os.path.isfile(path):
        fail(f"{name} is not a file: {path}")


def validate_inputs(args, appid, appsecret):
    if not appid or not appsecret:
        fail("AppID/AppSecret required (--appid/--appsecret or WX_APPID/WX_APPSECRET)")

    ensure_file(args.content_file, "content file")
    ensure_file(args.cover, "cover image")

    if len(args.title.strip()) == 0:
        fail("title cannot be empty")

    if len(args.digest) > 120:
        print("Warn: digest length > 120 chars, WeChat display may truncate.", file=sys.stderr)

    if args.need_open_comment not in (0, 1):
        fail("--need-open-comment must be 0 or 1")

    if args.only_fans_can_comment not in (0, 1):
        fail("--only-fans-can-comment must be 0 or 1")
    
    if args.header_img:
        ensure_file(args.header_img, "header image")
    
    for key, path in (args.content_img or {}).items():
        ensure_file(path, f"content image '{key}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建公众号草稿")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--author", default=None, help="作者（或设置 WX_AUTHOR 环境变量）")
    parser.add_argument("--digest", default="", help="文章摘要，建议 120 字以内")
    parser.add_argument("--content-file", required=True, help="HTML 内容文件路径")
    parser.add_argument("--cover", required=True, help="封面图路径")
    parser.add_argument("--header-img", default=None, help="页眉图片路径")
    parser.add_argument(
        "--content-img",
        action='append',
        nargs='*',
        metavar="KEY=PATH",
        help="文章内容图片，格式为 KEY=PATH。可指定多次，例如 --content-img image1=./img1.jpg --content-img image2=./img2.png",
        default=[],
    )
    parser.add_argument("--appid", default=None, help="AppID（或设置 WX_APPID 环境变量）")
    parser.add_argument("--appsecret", default=None, help="AppSecret（或设置 WX_APPSECRET 环境变量）")
    parser.add_argument("--need-open-comment", type=int, default=1, help="是否开启评论：1 开启，0 关闭")
    parser.add_argument("--only-fans-can-comment", type=int, default=0, help="是否仅粉丝可评论：1 是，0 否")
    args = parser.parse_args()

    # 解析 --content-img 参数为字典
    content_images_dict = {}
    for item in args.content_img:
        if isinstance(item, list): # 如果 nargs='*' 导致嵌套列表
            for sub_item in item:
                if '=' in sub_item:
                    key, path = sub_item.split('=', 1)
                    content_images_dict[key] = path
                else:
                    fail(f"Invalid --content-img format: {sub_item}. Expected KEY=PATH")
        elif '=' in item: # 直接的 KEY=PATH
            key, path = item.split('=', 1)
            content_images_dict[key] = path
        else:
            fail(f"Invalid --content-img format: {item}. Expected KEY=PATH")
    args.content_img = content_images_dict


    appid = args.appid or os.environ.get("WX_APPID")
    appsecret = args.appsecret or os.environ.get("WX_APPSECRET")
    author = args.author or os.environ.get("WX_AUTHOR", "")

    validate_inputs(args, appid, appsecret)

    with open(args.content_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    print("[1/3] Getting access token...")
    token = get_access_token(appid, appsecret)

    print("[2/3] Uploading images...")
    thumb_media_id = upload_cover(token, args.cover)

    uploaded_content_image_urls = {}
    
    if args.header_img:
        print("    Uploading header image...")
        header_url = upload_image_to_content(token, args.header_img)
        content = content.replace("<!-- IMAGE_HEADER -->", f'<p style="text-align: center;"><img src="{header_url}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" alt="页眉"/></p>')
        uploaded_content_image_urls["header"] = header_url

    for key, path in args.content_img.items():
        print(f"    Uploading content image '{key}'...")
        image_url = upload_image_to_content(token, path)
        content = content.replace(f"<!-- IMAGE_{key.upper()} -->", f'<p style="text-align: center;"><img src="{image_url}" style="max-width: 100%; height: auto; display: block; margin: 0 auto;" alt="{key}"/></p>')
        uploaded_content_image_urls[key] = image_url

    print("[3/3] Creating draft...")
    result = create_draft(
        token=token,
        title=args.title,
        author=author,
        digest=args.digest,
        content=content,
        thumb_media_id=thumb_media_id,
        need_open_comment=args.need_open_comment,
        only_fans_can_comment=args.only_fans_can_comment,
    )

    print("Done!")
    print(json.dumps({
        "ok": True,
        "media_id": result.get("media_id"),
        "need_open_comment": args.need_open_comment,
        "only_fans_can_comment": args.only_fans_can_comment,
        "uploaded_content_images": uploaded_content_image_urls,
    }, ensure_ascii=False))
