import mimetypes
import os
from pathlib import Path
from typing import Iterable

import oss2


ROOT = Path(__file__).resolve().parent.parent
EXCLUDED_PATTERNS = (
    ".git/*",
    ".github/*",
    ".vercel/*",
    "scripts/*",
    "README.md",
    ".gitignore",
    "vercel.json",
)


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
      raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def normalize_prefix(prefix: str) -> str:
    prefix = prefix.strip().strip("/")
    return f"{prefix}/" if prefix else ""


def should_exclude(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    return any(path.match(pattern) or rel == pattern for pattern in EXCLUDED_PATTERNS)


def iter_site_files() -> Iterable[Path]:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if should_exclude(path):
            continue
        yield path


def content_headers(path: Path) -> dict[str, str]:
    content_type, _ = mimetypes.guess_type(path.name)
    headers: dict[str, str] = {"Cache-Control": "no-cache"}
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def upload_files(bucket: oss2.Bucket, prefix: str) -> set[str]:
    uploaded: set[str] = set()

    for path in iter_site_files():
        rel = path.relative_to(ROOT).as_posix()
        object_key = f"{prefix}{rel}"
        headers = content_headers(path)
        bucket.put_object_from_file(object_key, str(path), headers=headers)
        uploaded.add(object_key)
        print(f"uploaded: {object_key}")

    return uploaded


def delete_extra_files(bucket: oss2.Bucket, prefix: str, expected_keys: set[str]) -> None:
    delete_extra = os.getenv("ALIYUN_OSS_DELETE_EXTRA", "").strip().lower()
    if delete_extra not in {"1", "true", "yes"}:
        print("skip delete: ALIYUN_OSS_DELETE_EXTRA is not enabled")
        return

    for obj in oss2.ObjectIterator(bucket, prefix=prefix):
        if obj.key not in expected_keys:
            bucket.delete_object(obj.key)
            print(f"deleted: {obj.key}")


def main() -> None:
    access_key_id = require_env("ALIYUN_OSS_ACCESS_KEY_ID")
    access_key_secret = require_env("ALIYUN_OSS_ACCESS_KEY_SECRET")
    bucket_name = require_env("ALIYUN_OSS_BUCKET")
    endpoint = require_env("ALIYUN_OSS_ENDPOINT")
    prefix = normalize_prefix(os.getenv("ALIYUN_OSS_PREFIX", ""))

    auth = oss2.Auth(access_key_id, access_key_secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_name)

    uploaded_keys = upload_files(bucket, prefix)
    delete_extra_files(bucket, prefix, uploaded_keys)
    print(f"done: synced {len(uploaded_keys)} files to oss://{bucket_name}/{prefix}")


if __name__ == "__main__":
    main()
