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
import subprocess
import sys
import urllib.parse
import urllib.request


def fail(msg, code=1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def http_get_json(url, timeout=20):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        fail(f"HTTP GET failed: {e}")


def http_post_json(url, payload, timeout=20):
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        fail(f"HTTP POST failed: {e}")


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


def upload_cover(token, image_path):
    if not shutil_which("curl"):
        fail("curl not found. Please install curl first.")

    cmd = [
        "curl",
        "-sS",
        "-X",
        "POST",
        f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
        "-F",
        f"media=@{image_path}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        fail(f"upload cover failed: {result.stderr.strip() or result.stdout.strip()}")

    try:
        data = json.loads(result.stdout)
    except Exception:
        fail(f"upload cover returned non-json: {result.stdout[:300]}")

    if "media_id" not in data:
        fail(f"upload cover failed: {data}")
    return data["media_id"]


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


def shutil_which(cmd):
    # avoid importing shutil for tiny dependency surface
    for p in os.environ.get("PATH", "").split(os.pathsep):
        full = os.path.join(p, cmd)
        if os.path.isfile(full) and os.access(full, os.X_OK):
            return full
    return None


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="创建公众号草稿")
    parser.add_argument("--title", required=True, help="文章标题")
    parser.add_argument("--author", default=None, help="作者（或设置 WX_AUTHOR 环境变量）")
    parser.add_argument("--digest", default="", help="文章摘要，建议 120 字以内")
    parser.add_argument("--content-file", required=True, help="HTML 内容文件路径")
    parser.add_argument("--cover", required=True, help="封面图路径")
    parser.add_argument("--appid", default=None, help="AppID（或设置 WX_APPID 环境变量）")
    parser.add_argument("--appsecret", default=None, help="AppSecret（或设置 WX_APPSECRET 环境变量）")
    parser.add_argument("--need-open-comment", type=int, default=1, help="是否开启评论：1 开启，0 关闭")
    parser.add_argument("--only-fans-can-comment", type=int, default=0, help="是否仅粉丝可评论：1 是，0 否")
    args = parser.parse_args()

    appid = args.appid or os.environ.get("WX_APPID")
    appsecret = args.appsecret or os.environ.get("WX_APPSECRET")
    author = args.author or os.environ.get("WX_AUTHOR", "")

    validate_inputs(args, appid, appsecret)

    with open(args.content_file, "r", encoding="utf-8") as f:
        content = f.read().strip()

    print("[1/3] Getting access token...")
    token = get_access_token(appid, appsecret)

    print("[2/3] Uploading cover image...")
    thumb_media_id = upload_cover(token, args.cover)

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
    }, ensure_ascii=False))
