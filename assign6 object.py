"""
create_players.py

Reads `basketball.csv` in the same directory, parses it without using pandas or external modules,
creates a Player object for each row, and prints a short verification.

Usage: run from the directory containing `basketball.csv`, e.g.
    python create_players.py
"""

class Player:
    def __init__(self, **fields):
        # store all fields as attributes
        for k, v in fields.items():
            setattr(self, k, v)

    def __repr__(self):
        # show a compact but informative representation
        name = getattr(self, 'Player', getattr(self, 'player', None))
        team = getattr(self, 'Team', None)
        pts = getattr(self, 'PTS', None)
        return f"Player(name={name!r}, team={team!r}, PTS={pts!r})"


def split_csv_line(line):
    """Split a CSV line into fields, handling quoted fields with commas.
    This is a minimal parser suitable for well-formed CSV with double quotes.
    """
    fields = []
    cur = []
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            # toggle in_quotes unless this is an escaped quote
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                cur.append('"')
                i += 1
            else:
                in_quotes = not in_quotes
        elif ch == ',' and not in_quotes:
            fields.append(''.join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    # append last field (strip trailing newline)
    if cur:
        fields.append(''.join(cur).rstrip('\n').rstrip('\r'))
    return fields


def convert_value(val):
    """Attempt to convert to int or float, or return stripped string. Empty -> None."""
    if val is None:
        return None
    s = val.strip()
    if s == '':
        return None
    # try int
    try:
        if '.' not in s:
            return int(s)
    except Exception:
        pass
    # try float
    try:
        return float(s)
    except Exception:
        pass
    # remove surrounding quotes if any
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1]
    return s


def read_players(csv_path):
    players = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        header_line = f.readline()
        if not header_line:
            return players
        headers = [h.strip() for h in split_csv_line(header_line)]
        for line in f:
            # skip empty lines
            if not line.strip():
                continue
            cols = split_csv_line(line)
            # if number of columns mismatches header, keep as-is and pad with None
            if len(cols) < len(headers):
                cols += [None] * (len(headers) - len(cols))
            elif len(cols) > len(headers):
                # join extra columns into the last header (rare) or truncate
                cols = cols[:len(headers)]
            row = {}
            for h, v in zip(headers, cols):
                row[h] = convert_value(v)
            players.append(Player(**row))
    return players


if __name__ == '__main__':
    csv_file = 'basketball.csv'
    print(f"Reading '{csv_file}' and creating Player objects (no pandas, no modules)...")
    players = read_players(csv_file)
    print(f"Total players created: {len(players)}")
    # print first 10 players as verification
    to_show = min(10, len(players))
    print(f"Showing first {to_show} players:")
    for p in players[:to_show]:
        print(p)

    # optional: demonstrate access to fields of first player
    if players:
        first = players[0]
        print('\nExample of full attribute set for first player:')
        attrs = sorted([a for a in dir(first) if not a.startswith('_') and not callable(getattr(first, a))])
        # print name: value pairs
        for a in attrs:
            print(f"{a}: {getattr(first, a)}")
