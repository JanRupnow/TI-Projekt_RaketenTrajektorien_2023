from Methods.JsonMethods import update_key_in_json


def test_update_key():
    # Sample JSON data
    json_data = {
        "category1": {
            "item1": {"text": "apple", "key": "A"},
            "item2": {"text": "banana", "key": "B"}
        },
        "category2": {
            "item1": {"text": "cat", "key": "C"},
            "item2": {"text": "dog", "key": "D"}
        }
    }

    # The hotkey to update "banana" to "orange"
    hotkey = ("O", "banana")

    # Call the function to update the key in JSON
    updated_json = update_key_in_json(json_data, hotkey)

    # Assert that the "text" value is updated correctly
    assert updated_json["category1"]["item2"]["text"] == "banana"
    # Assert that the "key" value is updated correctly
    assert updated_json["category1"]["item2"]["key"] == "O"

    # Ensure that other values remain unchanged
    assert updated_json["category1"]["item1"]["text"] == "apple"
    assert updated_json["category1"]["item1"]["key"] == "A"

    # Ensure that the second category is not affected
    assert updated_json["category2"]["item2"]["text"] == "dog"
    assert updated_json["category2"]["item2"]["key"] == "D"