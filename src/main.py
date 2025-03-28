#!./.venv/bin/python
from os import remove
from pandas import DataFrame as df
import re
import time

ignore_lines = 15
with open("FINAL BUDGET PROPOSAL.md", "r") as file:
    text = file.read()


text = text.split("\n")
text = text[ignore_lines:]

brackets = r"\[(.*?)\]"
parens = r"\((.*?)\)"


def remove_md(data):
    data = data.replace("~", "")
    data = data.replace("*", "")
    data = data.replace(")", "")
    return data


# data = df
category = None
items = []
item = {}
for line in text:
    # print("\n" * 1)
    # section header
    if line.startswith("* "):
        category = line.strip(" *")

    # item header
    elif line.startswith("  * "):
        if category and item != {}:
            items.append(item)
            item = {}
        # getting name, url, cost
        # print(f"line: {line}")
        line = line.strip(" *")
        try:
            splitter = line.index("$") + 1
            # print(f"{splitter}")
            name_url = line[:splitter]
            prices = line[splitter:]
            # print(f"name_url: {name_url}")
            # print(f"prices: {prices}")
            # name_url, prices = line.split(" ", 1)
        except Exception as e:
            # print(line)
            print(e)
            print("INVALID LINE, IGNORING")
            continue
        name = re.findall(brackets, name_url)[0]

        link = re.findall(parens, name_url)[0]
        if "~" in name:
            item["ordered"] = "True"
        else:
            item["ordered"] = "False"
        name = remove_md(name)
        item["name"] = name
        # print(f"name {name}")
        item["category"] = category
        # print(f"category {category}")
        item["link"] = link
        try:
            # works if theres parenthesis
            parenthesized_index = prices.index("(")
            total_price = prices[:parenthesized_index]
            item["header_note"] = prices[prices.index(")")]
            unit_price = re.findall(parens, prices)[0]
            total_price = remove_md(total_price)
            item["total_price"] = total_price
            item["unit_price"] = unit_price
            # print(f"total_price: {total_price}")
            # print(f"unit_price: {unit_price}")
            # print(f"header_note {item['header_note']}")
        except:
            # no parenthesis
            prices = remove_md(prices)
            item["total_price"] = prices
            item["unit_price"] = "NA"
            # print(f"total_price: {prices}")
            # print(f"unit_price: {'NA'}")

        # print(item)
        # time.sleep(1)

        item_name = line
    # subsection
    if line.startswith("    * "):
        line = line.replace("!", "")
        line = line.replace("*", "")
        # line = line.replace(" ", "")
        if "Orders" in line:
            item["orders"] = line.split(":")[-1]
        elif "Dimensions" in line:
            item["dimensions"] = line.split(":")[-1]
        elif "Per\_Order" in line:
            print(line)
            item["per_order"] = line.split(":")[-1]
        else:
            try:
                item["note"].append(line)
            except:
                item["note"] = [line]
        # print(line)

# category	item	quantity	ordered	total_cost	unit_cost	link notes

columns = []
for item in items:
    # print(item["quantity"])
    try:
        if not "orders" in item.keys():
            item["orders"] = "NA"
        if not "per_order" in item.keys():
            item["per_order"] = "NA"
        if not "dimensions" in item.keys():
            item["dimensions"] = "NA"

        if not "note" in item.keys():
            item["note"] = []
        try:
            item["note"].append(item["top_note"])
        except:
            pass
        item["note"] = ", ".join(item["note"])
        row = [
            item["category"],
            item["ordered"],
            item["name"],
            item["total_price"],
            item["unit_price"],
            item["link"],
            item["orders"],
            item["per_order"],
            item["dimensions"],
            item["note"],
        ]

        columns.append(row)
    except Exception as e:
        print(e)
        # print(item)

data = df(
    columns,
    columns=[
        "category",
        "ordered(crossed out)",
        "name",
        "total_price",
        "unit_price",
        "link",
        "orders",
        "per_order",
        "dimensions",
        "note",
    ],
)

data.to_csv("data.csv", index=False)
