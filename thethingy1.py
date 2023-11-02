from tkinter import ttk
import tkinter as tk
import pandas as pd

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, scrollbar_orient = "vertical", scrollbar_side = "right", scrollbar_fill = "y", *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        if (scrollbar_orient == "vertical"):
            scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        else:
            scrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        if (scrollbar_orient == "vertical"):
            canvas.configure(yscrollcommand=scrollbar.set)
        else:
            canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side=scrollbar_side, fill=scrollbar_fill)

class Feedback:

    def __init__(self, master, column_name):

        df = pd.read_csv("clusters.csv")
        clusters = {}
        n = 0
        for item in df[column_name]:
            if item in clusters:
                clusters[item].append(df["Main food description"][n])
            else:
                clusters[item] = [df["Main food description"][n]]
            n +=1 


        clust_row = 0
        self.clusters_frame = ScrollableFrame(master)


        
        self.clust_frames = {}
        self.clust_buttons = {}
        for cluster, values in clusters.items():
            self.clust_frames["cluster{0}".format(cluster)] = ScrollableFrame(self.clusters_frame.scrollable_frame, scrollbar_orient = "horizontal", scrollbar_side="top", scrollbar_fill="x")
            self.clust_frames["cluster{0}".format(cluster)].pack()
            self.clust_buttons["cluster{0}_{1}".format(cluster, 0)] = ttk.Button(self.clust_frames["cluster{0}".format(cluster)].scrollable_frame, text = values[0]).pack()
            clust_row += 1
        self.clusters_frame.pack()
        

        

            
def main():

               
    root = tk.Tk()
    app = Feedback(root, "100 cluster group")
    root.mainloop()
    
if __name__ == "__main__": main()