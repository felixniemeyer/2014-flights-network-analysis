import sqlite3


def sortedAirlines():
    conn = sqlite3.connect(
        '/home/sai/Documents/WiSe 2019-2020/Network Economics/Case Study/network-economics-case-study/db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT distinct airline_id FROM routes")
    rows = cursor.fetchall()
    airline_ids = []

    for row in rows:
        airline_ids.append(row)
    new_airline_list = []

    for item in airline_ids:
        cursornew = conn.cursor()
        cursornew.execute("SELECT COUNT(*) FROM routes WHERE airline_id =?", item)
        no_of_routes = cursornew.fetchall()
        listItem = list(item)
        new_airline_list.append([listItem[0], no_of_routes[0][0]])

    return sorted(new_airline_list, key=lambda x: x[1], reverse=True)
