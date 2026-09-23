from src.tools.order_lookup import lookup_order


def test_existing_order():
    result = lookup_order("ORD-1001")

    assert result is not None
    assert result["order_id"] == "ORD-1001"
    assert "status" in result


def test_unknown_order():
    result = lookup_order("ORD-DOES-NOT-EXIST")

    assert result is None


def test_private_customer_data_is_not_exposed():
    result = lookup_order("ORD-1001")

    assert result is not None

    assert "customer" not in result
    assert "email" not in result
    assert "shipping_address" not in result


def test_order_id_is_case_insensitive():
    result = lookup_order("ord-1001")

    assert result is not None
    assert result["order_id"] == "ORD-1001"