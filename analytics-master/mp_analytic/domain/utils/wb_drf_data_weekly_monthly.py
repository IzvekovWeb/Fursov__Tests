import datetime


def get_drf_data(table):
    drf_data = {
        "dynamicOrders": {
            "dates": [],
            "ordersData": [],
            "soldData": []
        },
        "orders": {},
        "sold": {},
        "goto": {},
        "baseStat": {},
    }

    for row in table:
        try:
            datetime.datetime.strptime(row[0], "%d.%m.%y")
            drf_data["dynamicOrders"]["dates"].append(row[0])

            drf_data["dynamicOrders"]["ordersData"].append(row[1])
            drf_data["dynamicOrders"]["soldData"].append(row[3])

        except ValueError:
            pass

        if row[0] == "Итого":
            drf_data["orders"]["ordersCount"] = row[1]
            drf_data["sold"]["soldCount"] = row[3]

        elif row[0] == "Сделано":
            drf_data["orders"]["percentFact"] = round(row[2] * 100)
            drf_data["sold"]["percentFact"] = round(row[4] * 100)

        elif row[0] == "Идем на $":
            drf_data["goto"]["ordersRub"] = int(row[1])
            drf_data["goto"]["realize"] = int(row[6])
            drf_data["goto"]["logistic"] = int(row[5])
            drf_data["goto"]["sold"] = int(row[3])

    return drf_data
