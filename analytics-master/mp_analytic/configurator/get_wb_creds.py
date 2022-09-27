from .models import *
from data.marketplaces.wildberries.wb_auth import WBAuth


def get_creds(token_v3, user_id):
    user = User.objects.filter(pk=user_id)
    user = user.first()
    user.token_v3 = token_v3
    user.save()

    try:
        wb_auth_object = WBAuth("")
        wb_token, suppliers = wb_auth_object.get_wb_token(token_v3)

        old_instances = UserCredentials.objects.filter(user=user_id)
        if old_instances:
            old_instances.delete()

        new_instance = UserCredentials
        for supplier in suppliers:
            print(supplier.get("name"))
            x64key, access_token = wb_auth_object.get_external_keys(wb_token, supplier.get("id"))
            new_instance = UserCredentials(
                user=user,
                wb_token=wb_token,
                name=supplier.get("name"),
                organization=supplier.get("fullName"),
                token=access_token,
                x64key=x64key,
                supplier_id=supplier.get("id")
            )
            new_instance.save()
    except Exception as error:
        print(f"---------------------- {error}")
        return False
    return True
