import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = "https://www.nykaa.com/search/result/?q=beauty&root=search&searchType=Manual&sourcepage=home"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

titles = soup.find_all("h2", class_="css-xrzmfa")

print("Number of products:", len(titles))

# Empty list to store product data
products = []

for product in titles[:20]:

    # Product Name
    product_name = product.get_text(strip=True)

    # Product card text
    parent = product.parent
    text = parent.get_text(" ", strip=True)

    # MRP
    mrp_match = re.search(r"Regular price ₹(\d+)", text)

    if mrp_match:
        mrp = mrp_match.group(1)
    else:
        mrp = "N/A"

    # Selling Price
    price_match = re.search(r"Discounted price ₹(\d+)", text)

    if price_match:
        price = price_match.group(1)
    else:
        price = "N/A"

    # Discount
    discount_match = re.search(r"(\d+)% Off", text)

    if discount_match:
        discount = discount_match.group(1) + "%"
    else:
        discount = "N/A"

    # Brand
    brand_match = re.match(r"(\S+)", product_name)

    if brand_match:
        brand = brand_match.group(1)
    else:
        brand = "N/A"

    # Rating
    rating = "N/A"

    current = product

    for i in range(5):

        if current:

            current_text = current.get_text(" ", strip=True)

            rating_match = re.search(r"\b[0-5]\.\d\b", current_text)

            if rating_match:
                rating = rating_match.group(0)
                break

            current = current.parent

    # Reviews
    reviews_match = re.search(r"\(\s*(\d+)\s*\)", text)

    if reviews_match:
        reviews = reviews_match.group(1)
    else:
        reviews = "N/A"

    # Product URL
    link = product.find_parent("a", href=True)

    if link:
        product_url = "https://www.nykaa.com" + link["href"]
    else:
        product_url = "N/A"

    # Category
    category = "Beauty"

    # Store product data
    products.append({
        "Product Name": product_name,
        "Brand": brand,
        "MRP": mrp,
        "Selling Price": price,
        "Discount": discount,
        "Rating": rating,
        "Reviews": reviews,
        "Product URL": product_url,
        "Category": category
    })


# Create DataFrame
df = pd.DataFrame(products)

# Display DataFrame as table
df

# Save to CSV
df.to_csv("nykaa_beauty_products.csv", index=False)

print("\nCSV file created successfully!")
print("Total products saved:", len(df))

print(df)

df