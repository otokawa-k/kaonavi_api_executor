from typing import Any, Dict, List, Tuple
import pytest
from kaonavi_api_executor.api.get_members_api import MembersResponse
from kaonavi_api_executor.transformers.members_member_data_flattener import (
    MembersMemberDataFlattener,
)


test_cases: List[
    Tuple[List[Dict[str, Any]], Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]]
] = [
    (
        # 入力: member_data
        [
            {
                "id": 1,
                "code": "A0002",
                "name": "カオナビ 太郎",
                "name_kana": "カオナビ タロウ",
                "mail": "taro@kaonavi.jp",
                "entered_date": "2005-09-20",
                "retired_date": "",
                "gender": "男性",
                "birthday": "1984-05-15",
                "age": 36,
                "years_of_service": "15年5ヵ月",
                "department": {
                    "code": "1000",
                    "name": "取締役会",
                    "names": ["取締役会"],
                },
                "sub_departments": [],
                "face_image": {"updated_at": "2020-10-01 01:23:45"},
                "custom_fields": [
                    {"id": 100, "name": "血液型", "values": ["A"]},
                    {
                        "id": 300,
                        "name": "電話番号",
                        "values": ["078-1234-5678", "090-1234-5678"],
                    },
                ],
            },
            {
                "id": 2,
                "code": "A0001",
                "name": "カオナビ 花子",
                "name_kana": "カオナビ ハナコ",
                "mail": "hanako@kaonavi.jp",
                "entered_date": "2013-05-07",
                "retired_date": "",
                "gender": "女性",
                "birthday": "1986-05-16",
                "age": 36,
                "years_of_service": "7年9ヵ月",
                "department": {
                    "code": "2000",
                    "name": "営業本部 第一営業部 ITグループ",
                    "names": ["営業本部", "第一営業部", "ITグループ"],
                },
                "sub_departments": [
                    {"code": "3000", "name": "企画部", "names": ["企画部"]},
                    {"code": "4000", "name": "管理部", "names": ["管理部"]},
                ],
                "face_image": None,
                "custom_fields": [
                    {"id": 100, "name": "血液型", "values": ["O"]},
                    {
                        "id": 200,
                        "name": "役職（一覧）",
                        "values": ["部長", "マネージャー"],
                    },
                    {"id": 300, "name": "電話番号", "values": ["03-1234-5678"]},
                    {
                        "id": 400,
                        "name": "変換（できるか）テスト",
                        "values": ["テスト"],
                    },
                ],
            },
            {
                "id": 3,
                "code": "A0003",
                "name": "カオナビ 次郎",
                "name_kana": "カオナビ ジロウ",
                "mail": "jiro@kaonavi.jp",
                "entered_date": "2015-01-01",
                "retired_date": "",
                "gender": "男性",
                "birthday": "1984-05-15",
                "age": 36,
                "years_of_service": "15年5ヵ月",
                "department": {
                    "code": "1000",
                    "name": "取締役会",
                    "names": ["取締役会"],
                },
                "sub_departments": [
                    {"code": "5000", "name": "営業部", "names": ["営業部"]},
                    {"code": "6000", "name": "開発部", "names": ["開発部"]},
                ],
                "face_image": {"updated_at": "2020-10-01 01:23:45"},
                "custom_fields": [
                    {"id": 100, "name": "血液型", "values": ["A"]},
                    {
                        "id": 300,
                        "name": "電話番号",
                        "values": ["078-1234-5678", "090-1234-5678"],
                    },
                ],
            },
        ],
        # 期待値: (main_df, sub_df)
        (
            [
                {
                    "社員番号": "A0002",
                    "氏名": "カオナビ 太郎",
                    "フリガナ": "カオナビ タロウ",
                    "メールアドレス": "taro@kaonavi.jp",
                    "入社日": "2005-09-20",
                    "退職日": "",
                    "性別": "男性",
                    "生年月日": "1984-05-15",
                    "年齢": 36,
                    "勤続年数": "15年5ヵ月",
                    "所属コード": "1000",
                    "所属名": "取締役会",
                    "所属名_階層別": '"取締役会"',
                    "顔写真更新日時": "2020-10-01 01:23:45",
                    "血液型": "A",
                    "役職_一覧": None,
                    "電話番号": '"078-1234-5678","090-1234-5678"',
                    "変換_できるか_テスト": None,
                },
                {
                    "社員番号": "A0001",
                    "氏名": "カオナビ 花子",
                    "フリガナ": "カオナビ ハナコ",
                    "メールアドレス": "hanako@kaonavi.jp",
                    "入社日": "2013-05-07",
                    "退職日": "",
                    "性別": "女性",
                    "生年月日": "1986-05-16",
                    "年齢": 36,
                    "勤続年数": "7年9ヵ月",
                    "所属コード": "2000",
                    "所属名": "営業本部 第一営業部 ITグループ",
                    "所属名_階層別": '"営業本部","第一営業部","ITグループ"',
                    "顔写真更新日時": None,
                    "血液型": "O",
                    "役職_一覧": '"部長","マネージャー"',
                    "電話番号": '"03-1234-5678"',
                    "変換_できるか_テスト": "テスト",
                },
                {
                    "社員番号": "A0003",
                    "氏名": "カオナビ 次郎",
                    "フリガナ": "カオナビ ジロウ",
                    "メールアドレス": "jiro@kaonavi.jp",
                    "入社日": "2015-01-01",
                    "退職日": "",
                    "性別": "男性",
                    "生年月日": "1984-05-15",
                    "年齢": 36,
                    "勤続年数": "15年5ヵ月",
                    "所属コード": "1000",
                    "所属名": "取締役会",
                    "所属名_階層別": '"取締役会"',
                    "顔写真更新日時": "2020-10-01 01:23:45",
                    "血液型": "A",
                    "役職_一覧": None,
                    "電話番号": '"078-1234-5678","090-1234-5678"',
                    "変換_できるか_テスト": None,
                },
            ],
            [
                {
                    "社員番号": "A0001",
                    "所属コード": "3000",
                    "所属名": "企画部",
                    "所属名_階層別": '"企画部"',
                },
                {
                    "社員番号": "A0001",
                    "所属コード": "4000",
                    "所属名": "管理部",
                    "所属名_階層別": '"管理部"',
                },
                {
                    "社員番号": "A0003",
                    "所属コード": "5000",
                    "所属名": "営業部",
                    "所属名_階層別": '"営業部"',
                },
                {
                    "社員番号": "A0003",
                    "所属コード": "6000",
                    "所属名": "開発部",
                    "所属名_階層別": '"開発部"',
                },
            ],
        ),
    ),
]


@pytest.mark.parametrize("member_data, expected", test_cases)
def test_members_member_data_flattener(
    member_data: List[Dict[str, Any]],
    expected: Tuple[List[Dict[str, Any]], List[Dict[str, Any]]],
) -> None:
    expected_main, expected_sub = expected

    input_data = MembersResponse(
        updated_at="2023-10-01T00:00:00Z",
        member_data=member_data,
    )
    flattener = MembersMemberDataFlattener(input_data)
    df_main, df_sub = flattener.flatten()

    actual_main = df_main.to_dict(orient="records")
    actual_sub = df_sub.to_dict(orient="records")

    assert actual_main == expected_main
    assert actual_sub == expected_sub
