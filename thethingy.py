from tkinter import ttk
import tkinter as tk
import pandas as pd
import os
import openai


'''
function taken from https://www.geeksforgeeks.org/openai-python-api/
'''
def comp(PROMPT, MaxToken=500, outputs=1):
    # using OpenAI's Completion module that helps execute 
    # any tasks involving text 
    response = openai.Completion.create(
        # model name used here is text-davinci-003
        # there are many other models available under the 
        # umbrella of GPT-3
        model="text-davinci-003",
        # passing the user input 
        prompt=PROMPT,
        # generated output can have "max_tokens" number of tokens 
        max_tokens=MaxToken,
        # number of outputs generated in one call
        n=outputs
    )
    # creating a list to store all the outputs
    output = list()
    for k in response['choices']:
        output.append(k['text'].strip())
    return output

def get_nutrition_vals():
	openai.organization = "org-amA1C7nGQio8ih1Ilh2pOsE6"
	openai.api_key = os.getenv("OPENAI_API_KEY")
	prompt = """Can you give me a rough estimate for the daily recommended nutritional values for a 70 inch male who is 170 pounds? 
		For your answer please give me a list for these nutrition values: 'Energy (kcal)', 'Protein (g)',
	   'Carbohydrate (g)', 'Sugars, total\n(g)', 'Fiber, total dietary (g)',
	   'Total Fat (g)', 'Fatty acids, total saturated (g)',
	   'Cholesterol (mg)',
	   'Retinol (mcg)', 'Vitamin A, RAE (mcg_RAE)', 'Thiamin (mg)', 'Riboflavin (mg)',
	   'Niacin (mg)', 'Vitamin B-6 (mg)', 'Folate, total (mcg)',
	   'Vitamin B-12 (mcg)', 'Vitamin C (mg)',
	   'Vitamin D (D2 + D3) (mcg)', 'Vitamin K (phylloquinone) (mcg)',
	   'Calcium (mg)', 'Phosphorus (mg)', 'Magnesium (mg)', 'Iron\n(mg)',
	   'Zinc\n(mg)', 'Copper (mg)', 'Selenium (mcg)', 'Potassium (mg)',
	   'Sodium (mg)']."""
	outputs = comp("What is the daily recommended nutrition values for a 70 inch male who is 170 pounds?")
	for output in outputs:
		print(output)
	# ['Energy (kcal)', 'Protein (g)',
	#    'Carbohydrate (g)', 'Sugars, total\n(g)', 'Fiber, total dietary (g)',
	#    'Total Fat (g)', 'Fatty acids, total saturated (g)',
	#    'Cholesterol (mg)',
	#    'Retinol (mcg)', 'Vitamin A, RAE (mcg_RAE)', 'Thiamin (mg)', 'Riboflavin (mg)',
	#    'Niacin (mg)', 'Vitamin B-6 (mg)', 'Folate, total (mcg)',
	#    'Vitamin B-12 (mcg)', 'Vitamin C (mg)',
	#    'Vitamin D (D2 + D3) (mcg)', 'Vitamin K (phylloquinone) (mcg)',
	#    'Calcium (mg)', 'Phosphorus (mg)', 'Magnesium (mg)', 'Iron\n(mg)',
	#    'Zinc\n(mg)', 'Copper (mg)', 'Selenium (mcg)', 'Potassium (mg)',
	#    'Sodium (mg)']
	return [3000, 170, 306, 36, 38,97,22, 300,900,900, 1.2, 1.3, 16, 1.7, 400, 2.4, 90, 15, 120, 1200, 700, 420, 8, 11, .9, 55, 3000, 2300]


def delete_column(buttons, cluster):
    for widget in buttons["cluster" + str(cluster)]:
        widget.grid_remove()

def inspect_column(self, buttons, cluster, fdf):
    nutrition_vals = [0] * 28
    for i in range(3, len(buttons["cluster" + str(cluster)])):
        food = buttons["cluster" + str(cluster)][i].cget('text')
        food_df = fdf.loc[fdf["Main food description"] == food]
        for j in range(len(self.nutrition_cols)):
            nutrition_vals[j] += food_df.iloc[0][self.nutrition_cols[j]]
    nutrition_vals = [nutrition_val/(len(buttons["cluster" + str(cluster)]) - 3) for nutrition_val in nutrition_vals]
    #print(nutrition_vals)
    text_str = ""
    for i in range(len(nutrition_vals)):
        text_str += self.nutrition_cols[i]
        text_str += ": "
        text_str = text_str + str(nutrition_vals[i]) + " (" + format(100 * (nutrition_vals[i]/self.nutrition_vals[i]), ".2f") + "%)\n"
    self.inspect_display.config(text = text_str)

def food_button_command(self, food, fdf):
    food_df = fdf.loc[fdf["Main food description"] == food]
    for i in range(len(self.nutrition_cols)):
        self.nutrition_bars[str(i)]["value"] += food_df.iloc[0][self.nutrition_cols[i]]
        self.nutrition_bars["progress{0}".format(i)].configure(text = "(" + str(self.nutrition_bars[str(i)]["value"]) +  "/" + str(self.nutrition_vals[i]) + ")")
    self.food_items.append(ttk.Button(self.food_items_frame, text = food))
    self.food_items[len(self.food_items) - 1].configure(command=lambda button=self.food_items[len(self.food_items) - 1]: delete_item(self, button, food_df.iloc[0]))
    self.food_items[len(self.food_items) - 1].grid(row = int((len(self.food_items) - 1) / 3), column = (len(self.food_items) - 1) % 3)

def delete_item(self, button, nut_list):
    #print(button.cget('text'))
    for i in range(len(self.nutrition_cols)):
        self.nutrition_bars[str(i)]["value"] -= nut_list[self.nutrition_cols[i]]
        self.nutrition_bars["progress{0}".format(i)].configure(text = "(" + str(self.nutrition_bars[str(i)]["value"]) +  "/" + str(self.nutrition_vals[i]) + ")")
    button.destroy()

def reset_bars(self):
    for i in range(len(self.nutrition_cols)):
        self.nutrition_bars[str(i)]["value"] = 0
    for item in self.food_items:
        item.destroy()
    

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, is_nutrition = False, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        if (not is_nutrition):
            canvas = tk.Canvas(self)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas, width = 400, height = 400)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.grid(row=0, column=0)
            scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
            canvas.configure(xscrollcommand=scrollbar2.set)
            scrollbar2.grid(row=1, column=0, sticky="ew")
            scrollbar.grid(row=0, column=1, sticky="ns")

        else:
            canvas = tk.Canvas(self, width = 400, height = 800)
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.scrollable_frame = ttk.Frame(canvas, width = 400, height = 800)

            self.scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.grid(row=0, column=0)
            scrollbar.grid(row=0, column=2, rowspan = 2, sticky="ns")


class Feedback:

    def __init__(self, master, column_name, nutrition_vals):

        df = pd.read_csv("clusters.csv")
        clusters = {}
        n = 0
        for item in df[column_name]:
            if item in clusters:
                clusters[item].append(df["Main food description"][n])
            else:
                clusters[item] = [df["Main food description"][n]]
            n +=1 
        ndf = pd.read_excel('2019-2020 FNDDS At A Glance - FNDDS Nutrient Values.xlsx', header=1)
        #food_dict = ndf.set_index('Main food description').T.to_dict('list')


        clust_row = 0
        self.clusters_frame = ttk.Frame(master)
        self.clusters_frame.grid(row = 0, column = 0)
        self.clusters_frame_scrollable = ScrollableFrame(self.clusters_frame)
        #for i in range(50):
            #ttk.Label(self.clusters_frame_scrollable.scrollable_frame, text="Sample scrolling label").pack()


        
        self.clust_frames = {}
        self.scrollbars = {}
        self.clust_buttons = {}
        # Makes a clust_buttons dictionary where each entry is a list of buttons for a cluster
        # The first entry is a delete button, second is a text and 3rd is an inspect.
        # The remaining items are the food items themselves
        for cluster, values in clusters.items():
            self.clust_buttons["cluster{0}".format(cluster)] = [ttk.Button(self.clusters_frame_scrollable.scrollable_frame, text = "X")]
            self.clust_buttons["cluster{0}".format(cluster)][0].grid(row = 0, column = cluster*2, padx = 5, pady = 5)
            self.clust_buttons["cluster{0}".format(cluster)][0].configure(command=lambda cluster=cluster: delete_column(self.clust_buttons, cluster))
            self.clust_buttons["cluster{0}".format(cluster)].append(ttk.Entry(self.clusters_frame_scrollable.scrollable_frame))
            self.clust_buttons["cluster{0}".format(cluster)][1].insert(0, "Enter Name Here")
            self.clust_buttons["cluster{0}".format(cluster)][1].grid(row = 1, column = cluster*2, padx = 5, pady = 5, columnspan = 2)
            self.clust_buttons["cluster{0}".format(cluster)].append(ttk.Button(self.clusters_frame_scrollable.scrollable_frame, text = "O"))
            self.clust_buttons["cluster{0}".format(cluster)][2].grid(row = 0, column = cluster*2 + 1, padx = 5, pady = 5)
            self.clust_buttons["cluster{0}".format(cluster)][2].configure(command=lambda cluster=cluster: inspect_column(self, self.clust_buttons, cluster, ndf))
            for n in range(len(values)):
                self.clust_buttons["cluster{0}".format(cluster)].append(ttk.Button(self.clusters_frame_scrollable.scrollable_frame, text = values[n]))
                self.clust_buttons["cluster{0}".format(cluster)][n+3].grid(row = n + 2, column = cluster*2, padx = 5, pady = 5, columnspan = 2)
                self.clust_buttons["cluster{0}".format(cluster)][n+3].configure(command=lambda food_item=values[n]: food_button_command(self, food_item, ndf))
        
        self.clusters_frame_scrollable.pack()
        self.food_items_frame = ttk.Frame(master)
        self.food_items_frame.grid(row = 1, column = 0)
        self.food_items = []

        
        self.nutrition_cols = ['Energy (kcal)', 'Protein (g)',
       'Carbohydrate (g)', 'Sugars, total\n(g)', 'Fiber, total dietary (g)',
       'Total Fat (g)', 'Fatty acids, total saturated (g)',
       'Cholesterol (mg)',
       'Retinol (mcg)', 'Vitamin A, RAE (mcg_RAE)', 'Thiamin (mg)', 'Riboflavin (mg)',
       'Niacin (mg)', 'Vitamin B-6 (mg)', 'Folate, total (mcg)',
       'Vitamin B-12 (mcg)', 'Vitamin C (mg)',
       'Vitamin D (D2 + D3) (mcg)', 'Vitamin K (phylloquinone) (mcg)',
       'Calcium (mg)', 'Phosphorus (mg)', 'Magnesium (mg)', 'Iron\n(mg)',
       'Zinc\n(mg)', 'Copper (mg)', 'Selenium (mcg)', 'Potassium (mg)',
       'Sodium (mg)']
        self.nutrition_vals = nutrition_vals
        self.nutrition_frame = ttk.Frame(master)
        self.nutrition_frame.grid(row = 0, column = 1, rowspan = 2)
        self.nutrition_frame_scrollable = ScrollableFrame(self.nutrition_frame, is_nutrition = True)

        # Add in the nutrition bars
        self.nutrition_bars = {}
        #print(len(nutrition_cols))
        #print(len(nutrition_vals))
        self.reset_button = ttk.Button(self.nutrition_frame_scrollable.scrollable_frame, text = "Reset")
        self.reset_button.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 2)
        self.reset_button.configure(command=lambda :reset_bars(self))

        s = ttk.Style()
        s.theme_use('alt')
        s.configure("red.Horizontal.TProgressbar", background='red')
        s.configure("green.Horizontal.TProgressbar", background='green')

        for i in range(len(self.nutrition_cols)):
            self.nutrition_bars["text{0}".format(i)] = ttk.Label(self.nutrition_frame_scrollable.scrollable_frame)
            self.nutrition_bars["text{0}".format(i)].configure(text = self.nutrition_cols[i])
            self.nutrition_bars["text{0}".format(i)].grid(row = i*2 + 1, column = 0, padx = 5, pady = 5)
            self.nutrition_bars["progress{0}".format(i)] = ttk.Label(self.nutrition_frame_scrollable.scrollable_frame)
            self.nutrition_bars["progress{0}".format(i)].configure(text = "(" + str(0) +  "/" + str(self.nutrition_vals[i]) + ")")
            self.nutrition_bars["progress{0}".format(i)].grid(row = i*2 + 1, column = 1, padx = 5, pady = 5)
            self.nutrition_bars["{0}".format(i)] = ttk.Progressbar(self.nutrition_frame_scrollable.scrollable_frame, maximum = self.nutrition_vals[i], length = 350, style = "green.Horizontal.TProgressbar")
            self.nutrition_bars["{0}".format(i)]['value'] = 0
            if (self.nutrition_cols[i] in ['Fatty acids, total saturated (g)', 'Cholesterol (mg)', 'Sodium (mg)']):
                self.nutrition_bars["{0}".format(i)].config(style = "red.Horizontal.TProgressbar")

            self.nutrition_bars["{0}".format(i)].grid(row = i*2 + 2, column = 0, padx = 5, pady = 5, columnspan = 2)





        self.nutrition_frame_scrollable.pack()

        self.inspect_display = ttk.Label(master, text = "Contents will display here")
        self.inspect_display.grid(row = 0, column = 2, rowspan = 2, padx = 5, pady = 5)
            
def main():

    nutrition_vals = get_nutrition_vals()          
    root = tk.Tk()
    app = Feedback(root, "100 cluster group", nutrition_vals)
    root.mainloop()
    
if __name__ == "__main__": main()