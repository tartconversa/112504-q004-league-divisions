# 社区联赛分组强度与融合赛程

比分是实际比赛的入球，空比分的弃权无现场交手。资格及可用日期均按当地业务日。

## 资料

CSV 样例为合成记录，使用 UTF-8，首行为字段名。多值用竖线分隔，空单元格表示来源未填。记录日期和业务生效日期各有含义。

- teams.csv 的字段为 team、division、prev_teams、roster_size、assist_rule、state。
- scores.csv 的字段为 match、home、away、home_goals、away_goals、kind、day、received。
- roster.csv 的字段为 person、team、from_day、to_day、kind、group。
- availability.csv 的字段为 person、slot、cert、available、recorded。
- slots.csv 的字段为 slot、field、starts、stops、condition。
- fixtures.csv 的字段为 fixture、home、away、slot、state。
- old_lineups.csv 的字段为 match、team、actual_players、assistants、minutes。

## 运行资料检查

在项目根目录使用 Python 3.11 或更高版本。依赖仅为标准库。

~~~sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
~~~
