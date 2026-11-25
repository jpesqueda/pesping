# pesping

**Concurrent IPv4 ICMP scanner and network upgrade monitor** · Version 1.1.0

[Español](README.es.md) · [Publishing guide / Guía de publicación](PUBLISHING.md)

pesping checks single hosts, files of hosts, IPv4 CIDR subnets, and inclusive IP ranges. Use a one-time scan to see reachable addresses or continuous monitoring to track device outages and recoveries during network maintenance.

## Requirements
- Python 3.10 or newer.
- Windows, Linux, or macOS with the system `ping` command available.
- Optional `colorama` for colored terminal output (installed automatically on Windows).

## Installation
After the package has been published to PyPI:
```powershell
python -m pip install pesping
pesping --help
```
From source before PyPI publication:
```powershell
git clone https://github.com/jpesqueda/pesping.git
cd pesping
python -m pip install -e .
pesping --help
```

## Target options
Exactly one target source is required.

| Argument | Meaning | Example |
| --- | --- | --- |
| `-ho`, `--host` | One IP address or hostname | `-ho 192.0.2.10` |
| `-hf`, `--host_file` | UTF-8 host file | `-hf hosts.txt` |
| `-r`, `--range` | Inclusive range, full or short form | `-r 192.0.2.100-200` |
| `-s`, `--subnet` | IPv4 CIDR network | `-s 198.51.100.0/26` |

Both `-r 192.0.2.100-192.0.2.200` and `-r 192.0.2.100-200` select 101 IPs. To cross an octet boundary, use the full ending IP. CIDR enumeration excludes network/broadcast for ordinary subnets, while /31 and /32 follow Python's `ipaddress.hosts()` behavior.

## Examples
```powershell
pesping -ho 192.0.2.10
pesping -hf hosts.txt --show down
pesping -r 192.0.2.100-200 --show up
pesping -r 192.0.2.100-192.0.2.200
pesping -s 198.51.100.0/26 --workers 20
pesping -s 192.0.2.0/24 --monitor --only-changes
pesping -hf hosts.txt --monitor --interval 2 --fail-threshold 3 --recovery-threshold 2 --log upgrade.log --csv upgrade.csv
pesping -hf hosts.txt --stop-when-all-up --only-changes
```

## Host file format
```text
# One target per line, or optional friendly-name,address
switch01.example.test,192.0.2.10
switch02.example.test,192.0.2.11
192.0.2.12
```
Blank lines and lines starting with `#` are ignored; duplicate addresses are skipped.

## Monitoring behavior
A target changes to DOWN after `--fail-threshold` consecutive failed ICMP probes (default 3); it changes to UP after `--recovery-threshold` consecutive replies (default 2). `--only-changes` suppresses cycle totals while retaining events. `--wait-for-up` exits once all targets reach UP. `--stop-when-all-up` exits after a DOWN event was observed and every target has recovered. Use Ctrl+C to stop and print a summary.

`--show all|up|down` filters **one-time scan results only**. `--workers` controls concurrency (default 50), `--timeout` controls the probe timeout (default 1 second), `--interval` controls monitoring intervals (default 2 seconds), and `--max-hosts` limits scan size (default 4096). Run `pesping --help` for exact options.

## Output
- Single scans show each selected target and a summary with total/reachable/unreachable counts.
- Monitoring logs state transitions, outage counts, accumulated downtime, and final per-device states.
- `--log FILE` stores timestamped text events; `--csv FILE` writes timestamp, event, host, address, status, outage count, and downtime.

## Important limitations
A failed ICMP reply **does not prove** that a host is down: firewalls and rate limiting can block ping. An ICMP response **does not prove** that applications or routing protocols are healthy. Outages are estimates based on the monitoring process's probes, not precise device event times.

All addresses and hostnames shown here are fictional documentation examples from RFC 5737 and the reserved `.test` domain. Only scan systems you are authorized to test. Runtime logs/CSVs may contain actual host information and should be protected.

## Development
```powershell
python -m pip install -e . pytest build twine
python -m pytest -q
python -m build
python -m twine check dist/*
```

License: MIT. Maintainer: [jpesqueda](https://github.com/jpesqueda).
