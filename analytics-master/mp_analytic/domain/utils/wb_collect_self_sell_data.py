from configurator.models import SelfSell


def collect_self_sell(user_id):
    queryset = SelfSell.objects.filter(user_id=user_id)
    response = {}

    for instance in queryset:
        if not response.get(instance.nm_id):
            response[instance.nm_id] = {
                "quantity": instance.total_amount,
                "rub": instance.total_sum
            }
        else:
            response[instance.nm_id]["quantity"] += instance.total_amount
            response[instance.nm_id]["rub"] += instance.total_sum
    print(response)
    return response
