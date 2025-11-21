import sys
import json
from datetime import datetime

DATETIME_FMT = "%Y-%m-%d %H:%M"

KNOWN_AIRPORTS = {
    "LHR",
    "JFK",
    "FRA",
    "RIX",
    "OSL",
    "HEL",
    "CDG",
    "DXB",
    "AMS",
    "BRU",
    "DOH",
    "SYD",
    "LAX",
    "ARN",
}


def parse_dt(text):
    try:
        return datetime.strptime(text, DATETIME_FMT)
    except ValueError:
        return None


def validate_line(fields, raw, line_no):
    if len(fields) != 6:
        return None, f"Line {line_no}: {raw} → missing required fields"

    flight_id, origin, dest, dep_str, arr_str, price_str = [f.strip() for f in fields]
    errors = []

    if not flight_id:
        errors.append("missing flight_id field")
    else:
        if not flight_id.isalnum():
            errors.append("flight_id must be alphanumeric")
        if len(flight_id) < 2:
            errors.append("flight_id too short (less than 2 characters)")
        if len(flight_id) > 8:
            errors.append("flight_id too long (more than 8 characters)")

    def check_airport(code, label):
        if not code:
            errors.append(f"missing {label} field")
            return
        if len(code) != 3 or not code.isalpha() or not code.isupper():
            errors.append(f"invalid {label} code")
        elif code not in KNOWN_AIRPORTS:
            errors.append(f"invalid {label} code")

    check_airport(origin, "origin")
    check_airport(dest, "destination")

    dep = parse_dt(dep_str) if dep_str else None
    arr = parse_dt(arr_str) if arr_str else None

    if not dep_str:
        errors.append("missing departure datetime")
    elif not dep:
        errors.append("invalid departure datetime")

    if not arr_str:
        errors.append("missing arrival datetime")
    elif not arr:
        errors.append("invalid arrival datetime")

    if dep and arr and arr <= dep:
        errors.append("arrival before departure")

    try:
        price = float(price_str)
        if price < 0:
            errors.append("negative price value")
        elif price == 0:
            errors.append("non-positive price value")
    except ValueError:
        errors.append("invalid price value")
        price = None

    if errors:
        return None, f"Line {line_no}: {raw} → " + ", ".join(errors)

    return {
        "flight_id": flight_id,
        "origin": origin,
        "destination": dest,
        "departure_datetime": dep_str,
        "arrival_datetime": arr_str,
        "price": price,
    }, None


def main():
    if len(sys.argv) != 2:
        print("Usage: python flight_parser.py path/to/db.csv")
        sys.exit(1)

    path = sys.argv[1]
    valid = []
    errors = []

    with open(path, encoding="utf-8") as f:
        for line_no, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue

            if line_no == 1 and line.split(",")[:6] == [
                "flight_id",
                "origin",
                "destination",
                "departure_datetime",
                "arrival_datetime",
                "price",
            ]:
                continue

            if line.startswith("#"):
                errors.append(
                    f"Line {line_no}: {line} → comment line, ignored for data parsing"
                )
                continue

            fields = line.split(",")
            rec, err = validate_line(fields, line, line_no)
            if rec:
                valid.append(rec)
            if err:
                errors.append(err)

    with open("db.json", "w", encoding="utf-8") as f:
        json.dump(valid, f, indent=2)

    with open("errors.txt", "w", encoding="utf-8") as f:
        for e in errors:
            f.write(e + "\n")

    print(f"Parsed {len(valid)} valid flights. See db.json and errors.txt.")


if __name__ == "__main__":
    main()
