#!/usr/bin/env python3

#╔══════════════════════════════════════════════════════════════╗
#║           BENOWN-UNDER v2.4.1  —  FRAMEWORK CORE            ║
#║         Multi-language pentesting toolkit skeleton           ║
#║         Python | Go | Java module support                    ║
#╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import subprocess
import threading
import platform
from datetime import datetime

# ─── ANSI COLOR PALETTE ─────────────────────────────────────
class C:
    GRN   = "\033[38;5;46m"    # bright green
    DGRN  = "\033[38;5;22m"    # dark green
    RED   = "\033[38;5;196m"   # bright red
    DRED  = "\033[38;5;52m"    # dark red
    DIM   = "\033[2m"
    BOLD  = "\033[1m"
    BLINK = "\033[5m"
    RESET = "\033[0m"
    CLEAR = "\033c"

G = C.GRN
R = C.RED
D = C.DIM
X = C.RESET
B = C.BOLD

# ─── BANNER ──────────────────────────────────────────────────
BANNER = f"""
{C.GRN}
██████╗ ███████╗███╗   ██╗ ██████╗ ██╗    ██╗███╗   ██╗
{C.RED}██╔══██╗██╔════╝████╗  ██║██╔═══██╗██║    ██║████╗  ██║
{C.GRN}██████╔╝█████╗  ██╔██╗ ██║██║   ██║██║ █╗ ██║██╔██╗ ██║
{C.RED}██╔══██╗██╔══╝  ██║╚██╗██║██║   ██║██║███╗██║██║╚██╗██║
{C.GRN}██████╔╝███████╗██║ ╚████║╚██████╔╝╚███╔███╔╝██║ ╚████║
{C.DGRN}╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
{C.GRN}
██╗   ██╗███╗   ██╗██████╗ ███████╗██████╗
{C.RED}██║   ██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
{C.GRN}██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
{C.RED}██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
{C.GRN}╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║
{C.DGRN}╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝{X}
"""

SUBBANNER = f"""
{C.DGRN}╔══[{G}SYSTEM{C.DGRN}]═══════════════════════════════════════════════════════╗
║  {C.RED}[ UNAUTHORIZED ACCESS IS A FEDERAL CRIME ]{C.DGRN}                        ║
║  {G}AUTHORIZED USERS ONLY  ::  ALL ACTIVITY IS LOGGED{C.DGRN}              ║
╠══[{G}INFO{C.DGRN}]══════════════════════════════════════════════════════════╣
║  {G}AUTHOR  {C.DGRN}::  {D}BENOWN-UNDER DEV TEAM{X}{C.DGRN}                              ║
║  {G}VERSION {C.DGRN}::  {G}v2.4.1-STABLE{C.DGRN}                                       ║
║  {G}RUNTIME {C.DGRN}::  {G}Python {sys.version.split()[0]}  |  Go bridge  |  Java bridge{C.DGRN}       ║
║  {G}MODULES {C.DGRN}::  {G}SPY  {C.DGRN}|  {G}PAGES  {C.DGRN}|  {R}OSINT  {C.DGRN}|  {R}PHISHING{C.DGRN}               ║
╚══════════════════════════════════════════════════════════════╝{X}
"""

# ─── MODULE REGISTRY ─────────────────────────────────────────
MODULES = {
    "spy": {
        "lang": ["python", "go"],
        "color": C.GRN,
        "desc": "Surveillance & network monitoring",
        "icon": "[>_]",
    },
    "pages": {
        "lang": ["python", "java"],
        "color": C.GRN,
        "desc": "Web scraping & page analysis",
        "icon": "[##]",
    },
    "osint": {
        "lang": ["python", "go"],
        "color": C.RED,
        "desc": "Open-source intelligence gathering",
        "icon": "[:::]",
    },
    "phishing": {
        "lang": ["java", "go"],
        "color": C.RED,
        "desc": "Phishing detection & header forensics",
        "icon": "[><]",
    },
}

# ─── UTILITY ─────────────────────────────────────────────────
def clear():
    os.system("cls" if platform.system() == "Windows" else "clear")

def typer(text: str, speed: float = 0.012):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def line(char="─", width=66, color=C.DGRN):
    print(f"{color}{char * width}{X}")

def status_bar(label: str, pct: int, color=C.GRN, width=30):
    filled = int(width * pct / 100)
    bar = "█" * filled + "░" * (width - filled)
    print(f"  {D}{label:<12}{X} [{color}{bar}{X}] {color}{pct:3d}%{X}")

def fake_scan(label: str = "SCANNING", steps: int = 20):
    sys.stdout.write(f"  {G}{label} [{X}")
    for _ in range(steps):
        time.sleep(0.05)
        sys.stdout.write(f"{G}#{X}")
        sys.stdout.flush()
    print(f"{G}] DONE{X}")

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

# ─── DISPLAY HELPERS ─────────────────────────────────────────
def show_banner():
    clear()
    print(BANNER)
    print(SUBBANNER)

def show_modules_panel():
    line()
    print(f"  {G}{'MODULE':<12} {'LANG':<18} {'STATUS':<10} DESCRIPTION{X}")
    line()
    for name, info in MODULES.items():
        col = info["color"]
        langs = " | ".join(info["lang"])
        icon = info["icon"]
        status = f"{G}LOADED{X}" if col == C.GRN else f"{R}RESTRICTED{X}"
        print(
            f"  {col}{icon} {name.upper():<9}{X}"
            f" {D}{langs:<18}{X}"
            f" {status:<20}"
            f" {D}{info['desc']}{X}"
        )
    line()

def show_sys_info():
    cpu_usage = random.randint(10, 45)
    mem_usage = random.randint(35, 65)
    print(f"\n  {G}[SYS INFO]{X}  {timestamp()}")
    print(f"  {D}OS       {X}: {G}{platform.system()} {platform.release()}{X}")
    print(f"  {D}Python   {X}: {G}{sys.version.split()[0]}{X}")
    print(f"  {D}Session  {X}: {G}BU-{hex(int(time.time()))[-6:].upper()}{X}")
    status_bar("CPU", cpu_usage)
    status_bar("MEMORY", mem_usage)
    print()

# ─── MODULE RUNNERS ──────────────────────────────────────────
# Each module function is a stub — add your Go/Java/Python logic here.

class SpyModule:
    name = "SPY"

    def run_scan(self, args):
        typer(f"  {G}[SPY]{X} Initializing network capture...")
        fake_scan("CAPTURE", 25)
        # ── ADD YOUR Go/Python pcap logic here ──
        # Example: subprocess.run(["./spy_go_binary", "--iface", "eth0"])
        print(f"  {G}[+]{X} Packets: {random.randint(100,999)}")
        print(f"  {G}[+]{X} Protocols detected: TCP, UDP, DNS")
        print(f"  {R}[!]{X} Anomaly score: {random.uniform(0.1, 0.4):.2f}")

    def run_status(self, args):
        print(f"  {G}SPY MODULE STATUS{X}")
        status_bar("GO bridge ", random.randint(80,99))
        status_bar("PY engine ", random.randint(85,99))

    def dispatch(self, cmd, args):
        dispatch = {"scan": self.run_scan, "status": self.run_status}
        fn = dispatch.get(cmd)
        if fn:
            fn(args)
        else:
            print(f"  {R}[ERR]{X} Unknown SPY command. Commands: scan, status")


class PagesModule:
    name = "PAGES"

    def run_scrape(self, args):
        url = args[0] if args else "http://target.local"
        typer(f"  {G}[PAGES]{X} Scraping: {url}")
        fake_scan("FETCH", 20)
        # ── ADD YOUR Java Selenium / Python bs4 logic here ──
        # Example: subprocess.run(["java", "-jar", "pages.jar", "--url", url])
        print(f"  {G}[+]{X} Links found : {random.randint(20,80)}")
        print(f"  {G}[+]{X} Forms found : {random.randint(1,8)}")
        print(f"  {G}[+]{X} JS scripts  : {random.randint(5,20)}")

    def run_forms(self, args):
        url = args[0] if args else "http://target.local"
        typer(f"  {G}[PAGES]{X} Enumerating forms on: {url}")
        fake_scan("FORM ENUM", 15)
        print(f"  {G}[+]{X} Action endpoints: {random.randint(1,5)}")

    def dispatch(self, cmd, args):
        dispatch = {"scrape": self.run_scrape, "forms": self.run_forms}
        fn = dispatch.get(cmd)
        if fn:
            fn(args)
        else:
            print(f"  {R}[ERR]{X} Unknown PAGES command. Commands: scrape, forms")


class OsintModule:
    name = "OSINT"

    def run_lookup(self, args):
        username = args[0] if args else "target"
        typer(f"  {R}[OSINT]{X} Username lookup: {username}")
        fake_scan("SEARCHING", 30)
        # ── ADD YOUR Go goroutine / Python Sherlock logic here ──
        # Example: subprocess.run(["./osint_go", "--user", username])
        platforms = ["GitHub", "Twitter", "Reddit", "HackerNews", "GitLab"]
        found = random.sample(platforms, 3)
        for p in found:
            print(f"  {G}[FOUND]{X}   {p} -> https://{p.lower()}.com/{username}")
        print(f"  {R}[MISS]{X}    {random.choice([p for p in platforms if p not in found])}")

    def run_geo(self, args):
        ip = args[0] if args else "8.8.8.8"
        typer(f"  {R}[OSINT]{X} Geolocating: {ip}")
        fake_scan("GEO", 15)
        print(f"  {G}[+]{X} Country: US | Region: California | ASN: AS15169")

    def dispatch(self, cmd, args):
        dispatch = {"lookup": self.run_lookup, "geo": self.run_geo}
        fn = dispatch.get(cmd)
        if fn:
            fn(args)
        else:
            print(f"  {R}[ERR]{X} Unknown OSINT command. Commands: lookup <user>, geo <ip>")


class PhishingModule:
    name = "PHISHING"

    def run_analyze(self, args):
        fname = args[0] if args else "email.eml"
        typer(f"  {R}[PHISHING]{X} Analyzing: {fname}")
        fake_scan("PARSING", 20)
        # ── ADD YOUR Java mail parser / Go header engine here ──
        # Example: subprocess.run(["java", "-jar", "phish.jar", "--file", fname])
        score = random.uniform(0.6, 0.97)
        verdict = f"{R}HIGH RISK{X}" if score > 0.75 else f"{G}LOW RISK{X}"
        print(f"  {R}[!]{X} SPF check    : FAIL")
        print(f"  {R}[!]{X} Domain age   : 12 days")
        print(f"  {G}[+]{X} ML Score     : {score:.2f}  ->  {verdict}")

    def run_url(self, args):
        url = args[0] if args else "hxxps://evil[.]example[.]com"
        typer(f"  {R}[PHISHING]{X} Deobfuscating URL: {url}")
        fake_scan("DEOBFUSCATE", 10)
        print(f"  {G}[+]{X} Canonical: {url.replace('hxxps','https').replace('[.]','.')}")

    def dispatch(self, cmd, args):
        dispatch = {"analyze": self.run_analyze, "url": self.run_url}
        fn = dispatch.get(cmd)
        if fn:
            fn(args)
        else:
            print(f"  {R}[ERR]{X} Unknown PHISHING command. Commands: analyze <file>, url <url>")


# ─── MODULE LOADER ───────────────────────────────────────────
MODULE_INSTANCES = {
    "spy":      SpyModule(),
    "pages":    PagesModule(),
    "osint":    OsintModule(),
    "phishing": PhishingModule(),
}

def show_help(current_mod: str):
    mod_help = {
        "spy":      ["scan", "status"],
        "pages":    ["scrape <url>", "forms <url>"],
        "osint":    ["lookup <user>", "geo <ip>"],
        "phishing": ["analyze <file>", "url <url>"],
    }
    global_cmds = ["modules", "sysinfo", "clear", "exit", "help"]
    line()
    print(f"  {G}GLOBAL COMMANDS{X}  : " + "  ".join([f"{G}{c}{X}" for c in global_cmds]))
    print(f"  {G}MODULE COMMANDS{X}  : use  {G}<module_name>{X}  to switch module")
    print(f"  {G}[{current_mod.upper()}] COMMANDS{X}: " + "  ".join([f"{G}{c}{X}" for c in mod_help[current_mod]]))
    line()

# ─── MAIN REPL ───────────────────────────────────────────────
def main():
    show_banner()
    show_modules_panel()
    show_sys_info()

    current_mod = "spy"

    while True:
        try:
            prompt = (
                f"{C.DGRN}┌─[{G}benown{C.DGRN}@{R}under{C.DGRN}]─"
                f"[{G}{current_mod}{C.DGRN}]\n"
                f"└──{G}➤ {X}"
            )
            raw = input(prompt).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{R}[!]{X} Ctrl+C detected. Type {G}exit{X} to quit.")
            continue

        if not raw:
            continue

        parts = raw.split()
        cmd, args = parts[0].lower(), parts[1:]

        # ── global commands
        if cmd == "exit":
            typer(f"\n{G}[BENOWN-UNDER]{X} Session terminated. Goodbye.")
            sys.exit(0)
        elif cmd == "clear":
            show_banner()
        elif cmd == "help":
            show_help(current_mod)
        elif cmd == "modules":
            show_modules_panel()
        elif cmd == "sysinfo":
            show_sys_info()
        elif cmd in MODULE_INSTANCES:
            current_mod = cmd
            col = MODULES[cmd]["color"]
            print(f"\n  {col}[+]{X} Switched to module: {col}{cmd.upper()}{X}\n")
        else:
            # ── delegate to active module
            MODULE_INSTANCES[current_mod].dispatch(cmd, args)
            print()


if __name__ == "__main__":
    main()
