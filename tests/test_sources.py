"""核对业务资料的格式和交接标识。"""
import csv
import unittest
from pathlib import Path

SAMPLES = Path(__file__).resolve().parents[1] / "samples"
SCHEMAS = {'teams': ['team', 'division', 'prev_teams', 'roster_size', 'assist_rule', 'state'], 'scores': ['match', 'home', 'away', 'home_goals', 'away_goals', 'kind', 'day', 'received'], 'roster': ['person', 'team', 'from_day', 'to_day', 'kind', 'group'], 'availability': ['person', 'slot', 'cert', 'available', 'recorded'], 'slots': ['slot', 'field', 'starts', 'stops', 'condition'], 'fixtures': ['fixture', 'home', 'away', 'slot', 'state'], 'old_lineups': ['match', 'team', 'actual_players', 'assistants', 'minutes']}
REFERENCES = [('scores', 'home', 'teams', 'team'), ('scores', 'away', 'teams', 'team'), ('roster', 'team', 'teams', 'team'), ('availability', 'slot', 'slots', 'slot'), ('fixtures', 'slot', 'slots', 'slot'), ('old_lineups', 'match', 'scores', 'match'), ('old_lineups', 'team', 'teams', 'team')]
OBSERVED = [('availability', 'person', 'X1', 3), ('roster', 'person', 'U1', 2), ('scores', 'home', 'T3', 2)]

class Sources(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tables = {}
        for table, fields in SCHEMAS.items():
            with (SAMPLES / (table + ".csv")).open(encoding="utf-8", newline="") as stream:
                records = csv.DictReader(stream, strict=True)
                if records.fieldnames != fields:
                    raise ValueError(f"字段不一致：{table}")
                cls.tables[table] = list(records)

    def test_records_have_documented_columns(self):
        for table, rows in self.tables.items():
            with self.subTest(table=table):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_source_links(self):
        for left, field, right, target in REFERENCES:
            with self.subTest(table=left, field=field):
                keys = {row[field] for row in self.tables[left] if row[field]}
                self.assertTrue(keys)
                self.assertLessEqual(keys, {row[target] for row in self.tables[right]})

    def test_shared_source_records_are_available(self):
        for table, field, value, seen in OBSERVED:
            with self.subTest(table=table, field=field, value=value):
                self.assertGreaterEqual(sum(row[field] == value for row in self.tables[table]), seen)
