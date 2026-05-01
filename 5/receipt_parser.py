import re
import json

def parse_receipt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    result = {}

    # 1. Extract all prices 
    price_pattern = r'\d{1,3}(?:\s\d{3})*,\d{2}'
    prices = re.findall(price_pattern, text)
    prices_cleaned = [
        float(p.replace(" ", "").replace(",", "."))
        for p in prices
    ]
    result["all_prices"] = prices_cleaned

    # 2. Extract product names
    product_pattern = r'\d+\.\n(.+?)\n'
    products = re.findall(product_pattern, text)
    result["products"] = [p.strip() for p in products]

    # 3. Calculate total amount
    total_match = re.search(r'ИТОГО:\n([\d\s,]+)', text)
    if total_match:
        total = float(total_match.group(1).replace(" ", "").replace(",", "."))
    else:
        total = sum(prices_cleaned)
    result["total"] = total

    # 4. Extract date and time
    datetime_match = re.search(r'Время:\s*([\d\.]+\s[\d:]+)', text)
    if datetime_match:
        result["datetime"] = datetime_match.group(1)

    # 5. Find payment method
    payment_match = re.search(r'(Банковская карта|Наличные)', text)
    if payment_match:
        result["payment_method"] = payment_match.group(1)
    return result
if __name__ == "__main__":
    data = parse_receipt("raw.txt")

    # 6. Structured JSON output
    print(json.dumps(data, indent=4, ensure_ascii=False))