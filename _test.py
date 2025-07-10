import pytest, csv
from main import values_is_integer, values_is_float, get_data, match_value_column_types, get_condition_result, get_aggregate_result, get_order_by_result


@pytest.mark.parametrize("input, expected", [
    (["123", "432", "4", "22"], True),
    (["12", "23", "-345432", "0"], True),
    (["123", "432", "word"], False),
    (["432", "654", "12.54", "1"], False)
])
def test_values_is_integer(input, expected):
    assert values_is_integer(input) == expected


@pytest.mark.parametrize("input, expected", [
    (["1.23", "43.2", "4.0", "2.2"], True),
    (["12", "0.0", "-34.5432", "85300.13"], True),
    (["123", "432", "word"], False),
    (["432", "654s", "12.54", "1"], False)
])
def test_values_is_float(input, expected):
    assert values_is_float(input) == expected


@pytest.mark.parametrize("input, expected", [
    ([
        ["Name", "Age", "Height"],
        ["Alice", "25", "165.5"],
        ["Bob", "30", "180.0"]
    ], [
        ["Name", "Age", "Height"],
        ["Alice", 25, 165.5],
        ["Bob", 30, 180.0]
    ]),
    ([
        ["Name", "Weight", "Height"],
        ["Jack", "75.3", "170.0"],
        ["Zack", "73", "160.0"]
    ], [
        ["Name", "Weight", "Height"],
        ["Jack", 75.3, 170],
        ["Zack", 73.0, 160]
    ]),
    ([
        ["Name", "Weight", "Height"]
    ], [
        ["Name", "Weight", "Height"]
    ])
])
def test_get_data_success(tmp_path, input, expected):
    file_path = tmp_path / "test.csv"
    with open(file_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(input)

    result = get_data(str(file_path))
    
    assert result == expected


@pytest.mark.parametrize("data, column_index, value, expected", [
    ([
        ["Name", "Weight", "Height"],
        ["Jack", 65.0, 164.7],
        ["Bob", 77.2, 183.2]
    ], 1, "66.4", 66.4),
    ([
        ["Name", "Weight", "Height"],
        ["Jack", 65.0, 164.7],
        ["Bob", 77.2, 183.2]
    ], 2, "170", 170.0),
    ([
        ["Name", "Weight", "Height"],
        ["Jack", 65.0, 164.7],
        ["Bob", 77.2, 183.2]
    ], 0, "Alice", "Alice"),
    ([
        ["Name", "Weight", "Height"],
        ["Jack", 65.0, 164.7],
        ["Bob", 77.2, 183.2]
    ], 1, "23.0s", None)
])
def test_match_value_column_types(data, column_index, value, expected):
    result = match_value_column_types(data, column_index, value)

    assert result == expected


@pytest.mark.parametrize("data, condition, expected", [
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "price<500", [
        ["name", "brand", "price", "rating"],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "rating>4.5", [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "brand=xiaomi", [
        ["name", "brand", "price", "rating"],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "brandxiaomi", None)
])
def test_get_condition_result(data, condition, expected):
    result = get_condition_result(data, condition)
    assert result == expected


@pytest.mark.parametrize("data, aggregate, expected", [
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "price=max", [
        ["max"],
        [1199]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "rating=avg", [
        ["avg"],
        [4.67]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "rating=min", [
        ["min"],
        [4.4]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "ratingmin", None)
])
def test_get_aggregate_result(data, aggregate, expected):
    result = get_aggregate_result(data, aggregate)
    assert result == expected


@pytest.mark.parametrize("data, order_rule, expected", [
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "price=desc", [
        ["name", "brand", "price", "rating"],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["iphone 15 pro", "apple", 999,4.9],
        ["poco x5 pro", "xiaomi", 299, 4.4],
        ["redmi note 12", "xiaomi", 199, 4.6]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "rating=asc", [
        ["name", "brand", "price", "rating"],
        ["poco x5 pro", "xiaomi", 299, 4.4],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["iphone 15 pro", "apple", 999, 4.9]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "brand=asc", [
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ]),
    ([
        ["name", "brand", "price", "rating"],
        ["iphone 15 pro", "apple", 999,4.9],
        ["galaxy s23 ultra", "samsung", 1199, 4.8],
        ["redmi note 12", "xiaomi", 199, 4.6],
        ["poco x5 pro", "xiaomi", 299, 4.4]
    ], "brandasc", None)
])
def test_get_order_by_result(data, order_rule, expected):
    result = get_order_by_result(data, order_rule)
    assert result == expected

