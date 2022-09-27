def encode_token(token: str) -> str:
    listed_token = list(token)
    for idx in range(7):
        listed_token[idx + 3], listed_token[-1 - idx - 3] = \
            listed_token[-1 - idx - 3], listed_token[idx + 3]
    result = ''.join(listed_token)
    return result
