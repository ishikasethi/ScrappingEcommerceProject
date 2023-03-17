import os
import time
import PySimpleGUI as pg
import functions


if not os.path.exists("product_data.csv"):
    with open("product_data.csv", 'w') as file:
        pass

pg.theme("LightGreen5")

clock = pg.Text('', key='clock')
label = pg.Text("Type keywords")
input_box = pg.InputText(tooltip="Enter keywords", key='keyword')
add_button = pg.Button("Search")
exit_button = pg.Button("Stop")
label2 = pg.Text("Total products found:")
output_label = pg.Text(key="totalProducts", text_color='green')
box = ""
boxLabel1 = pg.Text("Top 3 positions products")
list_box1 = pg.Listbox(values=box, key='position',
                      enable_events=True, size=(100, 5))
boxLabel2 = pg.Text("Top 3 Lowest Price Products")
list_box2 = pg.Listbox(values=box, key='lowPrice',
                      enable_events=True, size=(100, 5))
boxLabel3 = pg.Text("Top 3 Highest Average Rating products")
list_box3 = pg.Listbox(values=box, key='avgRating',
                      enable_events=True, size=(100, 5))
layout = [[clock],
          [label],
          [input_box, add_button, exit_button, output_label],
          [boxLabel1],
          [list_box1],
          [boxLabel2],
          [list_box2],
          [boxLabel3],
          [list_box3]]

window = pg.Window('Product Search engine App',
                   layout=layout,
                   font=('Helvetica', 10))

data = functions.extract_data()
while True:
    event, values = window.read(timeout=200)
    window["clock"].update(value=time.strftime("%b %d, %Y %H:%M:%S"))

    match event:
        case "Search":
            keywords = values['keyword']
            if keywords == "":
                pg.popup("Please enter keywords to search for a product!", font=('Helvetica', 15))
            else:
                products = functions.get_products()
                filtered_product = functions.filtered_products(products, keywords)
                if filtered_product:
                    top_products = functions.top_positions(filtered_product)
                    lowest_price = functions.lowest_price_products(filtered_product)
                    highest_avg_rating = functions.highest_avg_rating(filtered_product)
                    window["totalProducts"].update(value=f"Total {len(filtered_product)} Products found with similar specification")
                    window['position'].update(values=top_products)
                    window['lowPrice'].update(values=lowest_price)
                    window['avgRating'].update(values=highest_avg_rating)
                else:
                    window["totalProducts"].update(value="No Product Found")
                    window['position'].update(values="")
                    window['lowPrice'].update(values="")
                    window['avgRating'].update(values="")
        case "Stop":
            break

window.close()
