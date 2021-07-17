
# helper method, that takes 2 digits after the decimal point from float number.
def truncate_num(n):
    return float("{:.2f}".format(n))


# checks if POST request has `amount` field and check if it is valid
def is_valid_request(request_data):
    # try get 'amount' from request body
    # if there is no amount, then return -1
    amount = request_data.get('amount', -1)
    if amount > 0:
        return True, amount

    return False, None
