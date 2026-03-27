#!/usr/bin/env python3
"""
Keitaro Admin API Helper for Claude Code.

Usage:
    python3 keitaro_api.py test
    python3 keitaro_api.py campaigns list
    python3 keitaro_api.py campaign create --name "test" --alias "test-1"
    python3 keitaro_api.py campaign get --id 12
    python3 keitaro_api.py campaign disable --id 12
    python3 keitaro_api.py campaign enable --id 12
    python3 keitaro_api.py campaign clone --id 12
    python3 keitaro_api.py campaign delete --id 12
    python3 keitaro_api.py streams --campaign-id 12
    python3 keitaro_api.py stream create --campaign-id 12 --name "Flow" --weight 50
    python3 keitaro_api.py stream update --id 45 --weight 70
    python3 keitaro_api.py stream disable --id 45
    python3 keitaro_api.py stream enable --id 45
    python3 keitaro_api.py landings list
    python3 keitaro_api.py landing create --name "test" --url "https://..."
    python3 keitaro_api.py offers list
    python3 keitaro_api.py offer create --name "test" --url "https://..." --payout 50
    python3 keitaro_api.py domains list
    python3 keitaro_api.py domain check --id 3
    python3 keitaro_api.py networks list
    python3 keitaro_api.py sources list
    python3 keitaro_api.py report --grouping campaign_id --metrics clicks,conversions,roi --range 7d
    python3 keitaro_api.py clicks --range 7d
    python3 keitaro_api.py conversions --range 7d

Environment variables:
    KEITARO_URL     - Tracker base URL (e.g. https://tracker.example.com)
    KEITARO_API_KEY - Admin API key
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("Error: 'requests' package required. Install: pip3 install requests")
    sys.exit(1)


def get_config():
    url = os.environ.get("KEITARO_URL", "").rstrip("/")
    key = os.environ.get("KEITARO_API_KEY", "")
    if not url or not key:
        print("Error: KEITARO_URL and KEITARO_API_KEY environment variables required.")
        print("Set them:")
        print('  export KEITARO_URL="https://tracker.example.com"')
        print('  export KEITARO_API_KEY="your-api-key"')
        sys.exit(1)
    return url, key


def api_call(method, endpoint, data=None):
    url, key = get_config()
    full_url = f"{url}/admin_api/v1{endpoint}"
    headers = {"Api-Key": key, "Content-Type": "application/json"}

    try:
        if method == "GET":
            resp = requests.get(full_url, headers=headers, timeout=30)
        elif method == "POST":
            resp = requests.post(full_url, headers=headers, json=data or {}, timeout=30)
        elif method == "PUT":
            resp = requests.put(full_url, headers=headers, json=data or {}, timeout=30)
        elif method == "DELETE":
            resp = requests.delete(full_url, headers=headers, timeout=30)
        else:
            print(f"Error: Unknown method {method}")
            sys.exit(1)

        if resp.status_code in (200, 201):
            try:
                return resp.json()
            except json.JSONDecodeError:
                return {"status": "ok", "code": resp.status_code}
        else:
            print(f"API Error {resp.status_code}: {resp.text}")
            sys.exit(1)

    except requests.ConnectionError:
        print(f"Error: Cannot connect to {url}. Check KEITARO_URL.")
        sys.exit(1)
    except requests.Timeout:
        print("Error: Request timed out (30s). Tracker may be slow or unreachable.")
        sys.exit(1)


def parse_range(range_str):
    today = datetime.utcnow().date()
    if range_str == "today":
        return str(today), str(today)
    elif range_str == "yesterday":
        d = today - timedelta(days=1)
        return str(d), str(d)
    elif range_str.endswith("d"):
        days = int(range_str[:-1])
        return str(today - timedelta(days=days)), str(today)
    elif range_str.endswith("w"):
        weeks = int(range_str[:-1])
        return str(today - timedelta(weeks=weeks)), str(today)
    elif range_str.endswith("m"):
        months = int(range_str[:-1])
        return str(today - timedelta(days=months * 30)), str(today)
    else:
        # Expect "YYYY-MM-DD,YYYY-MM-DD"
        parts = range_str.split(",")
        if len(parts) == 2:
            return parts[0].strip(), parts[1].strip()
        return str(today - timedelta(days=7)), str(today)


# --- Commands ---

def cmd_test():
    url, key = get_config()
    masked_key = key[:4] + "..." + key[-4:] if len(key) > 8 else "***"
    print(f"Testing connection to {url}")
    print(f"API Key: {masked_key}")

    campaigns = api_call("GET", "/campaigns")
    active = [c for c in campaigns if c.get("state") == "active"]
    archived = [c for c in campaigns if c.get("state") != "active"]

    domains = api_call("GET", "/domains")
    active_domains = [d for d in domains if d.get("state") == "active"]

    offers = api_call("GET", "/offers")
    active_offers = [o for o in offers if o.get("state") == "active"]

    print(f"\nConnection successful!")
    print(f"Tracker: {url}")
    print(f"Campaigns: {len(active)} active, {len(archived)} archived")
    print(f"Domains: {len(active_domains)} active")
    print(f"Offers: {len(active_offers)} active")


def cmd_campaigns_list():
    campaigns = api_call("GET", "/campaigns")
    print(json.dumps(campaigns, indent=2, ensure_ascii=False))


def cmd_campaign_get(args):
    result = api_call("GET", f"/campaigns/{args.id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_campaign_create(args):
    data = {"name": args.name, "alias": args.alias}
    if args.domain_id:
        data["domain_id"] = int(args.domain_id)
    if args.traffic_source_id:
        data["traffic_source_id"] = int(args.traffic_source_id)
    if args.group_id:
        data["group_id"] = int(args.group_id)
    result = api_call("POST", "/campaigns", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_campaign_action(args, action):
    result = api_call("POST", f"/campaigns/{args.id}/{action}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_campaign_delete(args):
    result = api_call("DELETE", f"/campaigns/{args.id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_streams_list(args):
    result = api_call("GET", f"/campaigns/{args.campaign_id}/streams")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_stream_create(args):
    data = {
        "campaign_id": int(args.campaign_id),
        "name": args.name or "New Flow",
        "type": args.type or "regular",
        "weight": int(args.weight) if args.weight else 100,
        "state": "active",
    }
    if args.schema:
        data["schema"] = args.schema
    if args.landing_ids:
        data["landing_page_ids"] = [int(x) for x in args.landing_ids.split(",")]
    if args.offer_ids:
        data["offer_ids"] = [int(x) for x in args.offer_ids.split(",")]
    if args.filters:
        data["filters"] = json.loads(args.filters)
    result = api_call("POST", "/streams", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_stream_update(args):
    data = {}
    if args.weight:
        data["weight"] = int(args.weight)
    if args.name:
        data["name"] = args.name
    if args.filters:
        data["filters"] = json.loads(args.filters)
    result = api_call("PUT", f"/streams/{args.id}", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_stream_action(args, action):
    result = api_call("POST", f"/streams/{args.id}/{action}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_landings_list():
    result = api_call("GET", "/landing_pages")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_landing_create(args):
    data = {"name": args.name}
    if args.url:
        data["action_type"] = "redirect"
        data["url"] = args.url
    if args.html:
        data["action_type"] = "html"
        data["action_payload"] = args.html
    if args.group_id:
        data["group_id"] = int(args.group_id)
    result = api_call("POST", "/landing_pages", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_offers_list():
    result = api_call("GET", "/offers")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_offer_create(args):
    data = {"name": args.name, "url": args.url}
    if args.payout:
        data["payout_value"] = float(args.payout)
        data["payout_type"] = "CPA"
    if args.network_id:
        data["affiliate_network_id"] = int(args.network_id)
    if args.group_id:
        data["group_id"] = int(args.group_id)
    result = api_call("POST", "/offers", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_domains_list():
    result = api_call("GET", "/domains")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_domain_check(args):
    result = api_call("POST", f"/domains/{args.id}/check")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_networks_list():
    result = api_call("GET", "/affiliate_networks")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_sources_list():
    result = api_call("GET", "/traffic_sources")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_report(args):
    date_from, date_to = parse_range(args.range or "7d")
    metrics = (args.metrics or "clicks,campaign_unique_clicks,conversions,revenue,cost,profit,roi,cr,epc").split(",")
    grouping = (args.grouping or "campaign_id").split(",")

    data = {
        "range": {"from": date_from, "to": date_to, "timezone": args.timezone or "UTC"},
        "metrics": [m.strip() for m in metrics],
        "grouping": [g.strip() for g in grouping],
        "sort": [{"name": args.sort or "cost", "order": "desc"}],
        "summary": True,
        "limit": int(args.limit or 100),
    }

    if args.filters:
        filter_parts = args.filters.split(",")
        data["filters"] = []
        for f in filter_parts:
            key, val = f.split("=", 1)
            data["filters"].append({"name": key.strip(), "operator": "EQUALS", "expression": val.strip()})

    result = api_call("POST", "/report/build", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_clicks(args):
    date_from, date_to = parse_range(args.range or "7d")
    data = {
        "range": {"from": date_from, "to": date_to, "timezone": "UTC"},
        "columns": ["datetime", "campaign_id", "stream_id", "sub_id_1", "country", "device_type", "os", "browser"],
        "limit": int(args.limit or 50),
    }
    result = api_call("POST", "/clicks/log", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_conversions(args):
    date_from, date_to = parse_range(args.range or "7d")
    data = {
        "range": {"from": date_from, "to": date_to, "timezone": "UTC"},
        "columns": ["datetime", "campaign_id", "stream_id", "sub_id_1", "revenue", "status"],
        "order": [{"name": "datetime", "order": "desc"}],
        "limit": int(args.limit or 50),
    }
    result = api_call("POST", "/conversions/log", data)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="Keitaro Admin API Helper")
    sub = parser.add_subparsers(dest="command")

    # test
    sub.add_parser("test", help="Test API connection")

    # campaigns
    sub.add_parser("campaigns", help="List all campaigns")

    # campaign
    camp = sub.add_parser("campaign", help="Campaign operations")
    camp_sub = camp.add_subparsers(dest="action")

    camp_get = camp_sub.add_parser("get")
    camp_get.add_argument("--id", required=True)

    camp_create = camp_sub.add_parser("create")
    camp_create.add_argument("--name", required=True)
    camp_create.add_argument("--alias", required=True)
    camp_create.add_argument("--domain-id")
    camp_create.add_argument("--traffic-source-id")
    camp_create.add_argument("--group-id")

    for action in ["disable", "enable", "clone", "delete"]:
        p = camp_sub.add_parser(action)
        p.add_argument("--id", required=True)

    # streams
    streams = sub.add_parser("streams", help="List campaign streams")
    streams.add_argument("--campaign-id", required=True)

    # stream
    stream = sub.add_parser("stream", help="Stream operations")
    stream_sub = stream.add_subparsers(dest="action")

    stream_create = stream_sub.add_parser("create")
    stream_create.add_argument("--campaign-id", required=True)
    stream_create.add_argument("--name")
    stream_create.add_argument("--type", default="regular")
    stream_create.add_argument("--weight", default="100")
    stream_create.add_argument("--schema")
    stream_create.add_argument("--landing-ids")
    stream_create.add_argument("--offer-ids")
    stream_create.add_argument("--filters")

    stream_update = stream_sub.add_parser("update")
    stream_update.add_argument("--id", required=True)
    stream_update.add_argument("--weight")
    stream_update.add_argument("--name")
    stream_update.add_argument("--filters")

    for action in ["disable", "enable"]:
        p = stream_sub.add_parser(action)
        p.add_argument("--id", required=True)

    # landings
    sub.add_parser("landings", help="List landing pages")

    landing = sub.add_parser("landing", help="Landing operations")
    landing_sub = landing.add_subparsers(dest="action")
    landing_create = landing_sub.add_parser("create")
    landing_create.add_argument("--name", required=True)
    landing_create.add_argument("--url")
    landing_create.add_argument("--html")
    landing_create.add_argument("--group-id")

    # offers
    sub.add_parser("offers", help="List offers")

    offer = sub.add_parser("offer", help="Offer operations")
    offer_sub = offer.add_subparsers(dest="action")
    offer_create = offer_sub.add_parser("create")
    offer_create.add_argument("--name", required=True)
    offer_create.add_argument("--url", required=True)
    offer_create.add_argument("--payout")
    offer_create.add_argument("--network-id")
    offer_create.add_argument("--group-id")

    # domains
    sub.add_parser("domains", help="List domains")

    domain = sub.add_parser("domain", help="Domain operations")
    domain_sub = domain.add_subparsers(dest="action")
    domain_check = domain_sub.add_parser("check")
    domain_check.add_argument("--id", required=True)

    # networks & sources
    sub.add_parser("networks", help="List affiliate networks")
    sub.add_parser("sources", help="List traffic sources")

    # report
    report = sub.add_parser("report", help="Build report")
    report.add_argument("--grouping", default="campaign_id")
    report.add_argument("--metrics")
    report.add_argument("--range", default="7d")
    report.add_argument("--timezone", default="UTC")
    report.add_argument("--filters")
    report.add_argument("--sort", default="cost")
    report.add_argument("--limit", default="100")

    # clicks & conversions
    clicks = sub.add_parser("clicks", help="Click log")
    clicks.add_argument("--range", default="7d")
    clicks.add_argument("--limit", default="50")

    convs = sub.add_parser("conversions", help="Conversion log")
    convs.add_argument("--range", default="7d")
    convs.add_argument("--limit", default="50")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "test":
        cmd_test()
    elif args.command == "campaigns":
        cmd_campaigns_list()
    elif args.command == "campaign":
        if args.action == "get":
            cmd_campaign_get(args)
        elif args.action == "create":
            cmd_campaign_create(args)
        elif args.action == "delete":
            cmd_campaign_delete(args)
        elif args.action in ("disable", "enable", "clone"):
            cmd_campaign_action(args, args.action)
        else:
            print("Usage: keitaro_api.py campaign {get|create|disable|enable|clone|delete}")
    elif args.command == "streams":
        cmd_streams_list(args)
    elif args.command == "stream":
        if args.action == "create":
            cmd_stream_create(args)
        elif args.action == "update":
            cmd_stream_update(args)
        elif args.action in ("disable", "enable"):
            cmd_stream_action(args, args.action)
        else:
            print("Usage: keitaro_api.py stream {create|update|disable|enable}")
    elif args.command == "landings":
        cmd_landings_list()
    elif args.command == "landing":
        if args.action == "create":
            cmd_landing_create(args)
    elif args.command == "offers":
        cmd_offers_list()
    elif args.command == "offer":
        if args.action == "create":
            cmd_offer_create(args)
    elif args.command == "domains":
        cmd_domains_list()
    elif args.command == "domain":
        if args.action == "check":
            cmd_domain_check(args)
    elif args.command == "networks":
        cmd_networks_list()
    elif args.command == "sources":
        cmd_sources_list()
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "clicks":
        cmd_clicks(args)
    elif args.command == "conversions":
        cmd_conversions(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
