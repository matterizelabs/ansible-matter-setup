#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.request

RE_NDK = re.compile(r"(?i)ndk[^\n]*?(\d+\.\d+\.\d+)")
RE_NDK_SDKMANAGER = re.compile(r"ndk;([0-9.]+)")
RE_SDK_API = re.compile(r"android-([0-9]{2})")
RE_SDK_COMPILE = re.compile(r"compileSdkVersion\s*=?\s*([0-9]{2})")
RE_JDK = re.compile(r"(?i)\b(?:jdk|java)\b[^\n]*?([0-9]{1,2})")
RE_KOTLIN = re.compile(r"(?i)kotlin[^\n]*?([0-9]+\.[0-9]+\.[0-9]+)")
RE_CMDLINE = re.compile(r"cmdline-tools;([0-9.]+)")


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ansible-matter-setup"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8", errors="replace")


def first_match(text: str, patterns):
    for pat in patterns:
        m = pat.search(text)
        if m:
            return m.group(1)
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    args = ap.parse_args()

    md = fetch(args.url)

    ndk = first_match(md, [RE_NDK_SDKMANAGER, RE_NDK])
    sdk = first_match(md, [RE_SDK_COMPILE, RE_SDK_API])
    jdk = first_match(md, [RE_JDK])
    kotlin = first_match(md, [RE_KOTLIN])
    cmdline = first_match(md, [RE_CMDLINE])

    if not ndk or not sdk:
        missing = []
        if not sdk:
            missing.append("sdk_api_level")
        if not ndk:
            missing.append("ndk_version")
        sys.stderr.write("Missing required values: " + ", ".join(missing) + "\n")
        sys.exit(2)

    out = {
        "android_matter_sdk_api_level": sdk,
        "android_matter_ndk_version": ndk,
        "android_matter_jdk_version": jdk,
        "android_matter_kotlin_version": kotlin,
        "android_matter_cmdline_tools_version": cmdline,
    }

    print(json.dumps(out))


if __name__ == "__main__":
    main()
