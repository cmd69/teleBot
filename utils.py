import decimal
import json

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)