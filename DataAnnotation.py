# $ pip install requests lxml pandas


import requests
from lxml import html
import pandas as pd


def decode_secret_message(doc_url: str) -> None:
    """
    Fetches a published Google Doc containing character coordinates,
    parses the data, and prints the decoded character grid.

    Args:
        doc_url (str): URL of the published Google Doc.
    """
    try:
        # Fetch and parse the HTML content
        response = requests.get(doc_url)
        response.raise_for_status()
        tree = html.fromstring(response.text)

        # Extract the first table
        table = tree.xpath('//table')[0]
        rows = table.xpath('.//tr')
        data = [
            [cell.text_content().strip() for cell in row.xpath('.//td | .//th')]
            for row in rows
        ]

        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])

        # Convert coordinates to integers
        df["x-coordinate"] = pd.to_numeric(df["x-coordinate"], errors="coerce")
        df["y-coordinate"] = pd.to_numeric(df["y-coordinate"], errors="coerce")
        df.dropna(subset=["x-coordinate", "y-coordinate"], inplace=True)
        df["x-coordinate"] = df["x-coordinate"].astype(int)
        df["y-coordinate"] = df["y-coordinate"].astype(int)

        # Create pivot table
        grid = df.pivot_table(
            index="y-coordinate",
            columns="x-coordinate",
            values="Character",
            aggfunc="first",
            fill_value=" "
        )

        # Sort y-axis from top to bottom
        grid = grid.sort_index(ascending=False)

        # Print the decoded grid
        for row in grid.values:
            print(''.join(cell if cell else ' ' for cell in row))

    except Exception as e:
        print(f"Error decoding message: {e}")


decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub")
