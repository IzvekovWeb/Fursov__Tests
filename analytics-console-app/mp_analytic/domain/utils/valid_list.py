def is_valid_list(nomenclatures):
    not_valid = []
    for i in range(len(nomenclatures)):
        try:
            nomenclatures[i] = int(nomenclatures[i])
        except ValueError:
            not_valid.append(i)
    for invalid in not_valid:
        nomenclatures.pop(invalid)
