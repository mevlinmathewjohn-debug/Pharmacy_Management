def calculate_total(items):

    total = 0

    for item in items:

        total += (
            float(item["unit_price"])
            * item["quantity"]
        )

    return total