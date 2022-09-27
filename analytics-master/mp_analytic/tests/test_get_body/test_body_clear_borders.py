import pytest

from data.google.get_body_methods.get_body import get_body_clear_borders

constructor = {
        "style": "SOLID",
        "width": 2,
        "color": {
            "red": 255,
            "green": 0,
            "blue": 100
        },
        "colorStyle": {
            "rgbColor": {
                "red": 255,
                "green": 0,
                "blue": 100
            },
        }
    }


def test_get_body_clear_borders():
    expected_body_clear_borders_1 = {"requests":[{"repeatCell":{'range':{'sheetId':12345678},"cell":{"userEnteredFormat":{"borders":{"left":{"style":"SOLID","width":2,"color":{"red":255,"green":0,"blue":100},"colorStyle":{"rgbColor":{"red":255,"green":0,"blue":100},}},"right":{"style":"SOLID","width":2,"color":{"red":255,"green":0,"blue":100},"colorStyle":{"rgbColor":{"red":255,"green":0,"blue":100},}},"top":{"style":"SOLID","width":2,"color":{"red":255,"green":0,"blue":100},"colorStyle":{"rgbColor":{"red":255,"green":0,"blue":100},}},"bottom":{"style":"SOLID","width":2,"color":{"red":255,"green":0,"blue":100},"colorStyle":{"rgbColor":{"red":255,"green":0,"blue":100},}}}}},"fields":"userEnteredFormat.borders"}}]}

    assert get_body_clear_borders(12345678, constructor) == expected_body_clear_borders_1

    expected_body_clear_borders_2 = {'requests': [{'repeatCell':{'cell':{'userEnteredFormat':{'borders':{'bottom':{'color':{'blue':100,'green':0,'red':255},'colorStyle':{'rgbColor':{'blue':100,'green':0,'red':255}},'style':'SOLID','width':2},'left':{'color':{'blue':100,'green':0,'red':255},'colorStyle':{'rgbColor':{'blue':100,'green':0,'red':255}},'style':'SOLID','width':2},'right':{'color':{'blue':100,'green':0,'red':255},'colorStyle':{'rgbColor':{'blue':100,'green':0,'red':255}},'style':'SOLID','width':2},'top':{'color':{'blue':100,'green':0,'red':255},'colorStyle':{'rgbColor':{'blue':100,'green':0,'red':255}},'style':'SOLID','width':2}}}},'fields':'userEnteredFormat.borders','range':{'sheetId':12345678}}}]}

    assert get_body_clear_borders(12345678, constructor) == expected_body_clear_borders_2


def test_get_body_clear_borders_exceptions():
    with pytest.raises(TypeError):
        get_body_clear_borders([], constructor)

    with pytest.raises(ValueError):
        get_body_clear_borders(-1, constructor)
    with pytest.raises(ValueError):
        get_body_clear_borders('-1234', constructor)
    with pytest.raises(ValueError):
        get_body_clear_borders('some_id', constructor)
