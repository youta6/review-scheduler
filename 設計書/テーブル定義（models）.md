# USER
<table style="border-collapse: collapse;">
    <tr>
        <th colspan="2" style="border: 3px solid white; background-color: gray;">テーブル論理名：</th>
        <th colspan="2" style="border: 3px solid white;">ユーザー情報</th>
        <th colspan="3" style="border: 3px solid white; background-color: gray;">テーブル物理名：</th>
        <th colspan="3" style="border: 3px solid white;">USER</th>
    </tr>
    <tr>
        <th style="border: 3px solid white; background-color: gray;">論理名</th>
        <th style="border: 3px solid white; background-color: gray;">物理名</th>
        <th style="border: 3px solid white; background-color: gray;">型</th>
        <th style="border: 3px solid white; background-color: gray;">必須</th>
        <th style="border: 3px solid white; background-color: gray;">最小桁</th>
        <th style="border: 3px solid white; background-color: gray;">最大桁</th>
        <th style="border: 3px solid white; background-color: gray;">主キー</th>
        <th style="border: 3px solid white; background-color: gray;">一意</th>
        <th style="border: 3px solid white; background-color: gray;">外部キー</th>
        <th style="border: 3px solid white; background-color: gray;">備考</th>
    </tr>
    <tr>
        <td style="border: 1px solid white;">ユーザーID</td>
        <td style="border: 1px solid white;">id</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">2</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">ユーザー名</td>
        <td style="border: 1px solid white;">user_name</td>
        <td style="border: 1px solid white;">VARCHAR</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">50</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">ハッシュ済みパスワード</td>
        <td style="border: 1px solid white;">hashed_password</td>
        <td style="border: 1px solid white;">VARCHAR</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">255</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">削除済みフラグ</td>
        <td style="border: 1px solid white;">delete_flag</td>
        <td style="border: 1px solid white;">BOOLEAN</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">管理者フラグ</td>
        <td style="border: 1px solid white;">admin_flag</td>
        <td style="border: 1px solid white;">BOOLEAN</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">作成日</td>
        <td style="border: 1px solid white;">created_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">更新日</td>
        <td style="border: 1px solid white;">updated_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">更新しない限り作成日と同じ値</td>
    </tr>
</table>

---

# REVIEW
<table style="border-collapse: collapse;">
    <tr>
        <th colspan="2" style="border: 3px solid white; background-color: gray;">テーブル論理名：</th>
        <th colspan="2" style="border: 3px solid white;">復習情報</th>
        <th colspan="3" style="border: 3px solid white; background-color: gray;">テーブル物理名：</th>
        <th colspan="3" style="border: 3px solid white;">REVIEW</th>
    </tr>
    <tr>
        <th style="border: 3px solid white; background-color: gray;">論理名</th>
        <th style="border: 3px solid white; background-color: gray;">物理名</th>
        <th style="border: 3px solid white; background-color: gray;">型</th>
        <th style="border: 3px solid white; background-color: gray;">必須</th>
        <th style="border: 3px solid white; background-color: gray;">最小桁</th>
        <th style="border: 3px solid white; background-color: gray;">最大桁</th>
        <th style="border: 3px solid white; background-color: gray;">主キー</th>
        <th style="border: 3px solid white; background-color: gray;">一意</th>
        <th style="border: 3px solid white; background-color: gray;">外部キー</th>
        <th style="border: 3px solid white; background-color: gray;">備考</th>
    </tr>
    <tr>
        <td style="border: 1px solid white;">ユーザーID</td>
        <td style="border: 1px solid white;">user_id</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">2</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">USER.id</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習項目ID</td>
        <td style="border: 1px solid white;">review_id</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">3</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">ユーザーごとにIDを割り振る<br>1人当たり999件まで</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習項目</td>
        <td style="border: 1px solid white;">review_item</td>
        <td style="border: 1px solid white;">VARCHAR</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">200</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習内容詳細</td>
        <td style="border: 1px solid white;">description</td>
        <td style="border: 1px solid white;">VARCHAR</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1000</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">学習日</td>
        <td style="border: 1px solid white;">study_date</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">作成日</td>
        <td style="border: 1px solid white;">created_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">更新日</td>
        <td style="border: 1px solid white;">updated_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">更新しない限り作成日と同じ値</td>
    </tr>
</table>

---

# REVIEW_MANAGEMENT
<table style="border-collapse: collapse;">
    <tr>
        <th colspan="2" style="border: 3px solid white; background-color: gray;">テーブル論理名：</th>
        <th colspan="2" style="border: 3px solid white;">復習管理情報</th>
        <th colspan="3" style="border: 3px solid white; background-color: gray;">テーブル物理名：</th>
        <th colspan="3" style="border: 3px solid white;">REVIEW_MANAGEMENT</th>
    </tr>
    <tr>
        <th style="border: 3px solid white; background-color: gray;">論理名</th>
        <th style="border: 3px solid white; background-color: gray;">物理名</th>
        <th style="border: 3px solid white; background-color: gray;">型</th>
        <th style="border: 3px solid white; background-color: gray;">必須</th>
        <th style="border: 3px solid white; background-color: gray;">最小桁</th>
        <th style="border: 3px solid white; background-color: gray;">最大桁</th>
        <th style="border: 3px solid white; background-color: gray;">主キー</th>
        <th style="border: 3px solid white; background-color: gray;">一意</th>
        <th style="border: 3px solid white; background-color: gray;">外部キー</th>
        <th style="border: 3px solid white; background-color: gray;">備考</th>
    </tr>
    <tr>
        <td style="border: 1px solid white;">ユーザーID</td>
        <td style="border: 1px solid white;">user_id</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">2</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">USER.id</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習項目ID</td>
        <td style="border: 1px solid white;">review_id</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">3</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">REVIEW.review_id</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習回</td>
        <td style="border: 1px solid white;">review_time</td>
        <td style="border: 1px solid white;">INTEGER</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">1</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">1つのreview_id毎に1～5</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">復習予定日</td>
        <td style="border: 1px solid white;">review_date</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">学習日+1,+3,+7,+15,+31日</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">対応済みフラグ</td>
        <td style="border: 1px solid white;">done_flag</td>
        <td style="border: 1px solid white;">BOOLEAN</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">作成日</td>
        <td style="border: 1px solid white;">created_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
    </tr>
    <tr>
        <td style="border: 1px solid white;">更新日</td>
        <td style="border: 1px solid white;">updated_at</td>
        <td style="border: 1px solid white;">DATETIME</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">○</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="text-align: center; vertical-align: middle; border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">-</td>
        <td style="border: 1px solid white;">更新しない限り作成日と同じ値</td>
    </tr>
</table>
