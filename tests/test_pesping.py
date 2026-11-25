"""Offline tests for pesping address expansion and CLI arguments."""

import unittest
import pesping


class TargetTests(unittest.TestCase):
    def test_short_and_full_ranges(self):
        short = pesping.parse_range("192.0.2.100-200")
        full = pesping.parse_range("192.0.2.100-192.0.2.200")
        self.assertEqual(short, full)
        self.assertEqual(short[1] - short[0] + 1, 101)

    def test_cross_subnet_range(self):
        start, end = pesping.parse_range("192.0.2.254-192.0.3.2")
        self.assertEqual(end - start + 1, 5)

    def test_reverse_range_rejected(self):
        with self.assertRaises(ValueError):
            pesping.parse_range("192.0.2.200-100")

    def test_cidr_26(self):
        args, parser = pesping.parse_args(["-s", "198.51.100.0/26"])
        hosts = pesping.load_targets(args, parser)
        self.assertEqual(len(hosts), 62)
        self.assertEqual(hosts[0]["address"], "198.51.100.1")
        self.assertEqual(hosts[-1]["address"], "198.51.100.62")

    def test_cidr_22(self):
        args, parser = pesping.parse_args(["-s", "192.0.2.0/22"])
        self.assertEqual(len(pesping.load_targets(args, parser)), 1022)

    def test_host_limit(self):
        args, parser = pesping.parse_args(["-s", "198.51.100.0/24", "--max-hosts", "20"])
        with self.assertRaises(SystemExit):
            pesping.load_targets(args, parser)


if __name__ == "__main__":
    unittest.main()
