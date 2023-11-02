from tkinter import ttk
import tkinter as tk
import pandas as pd

def delete_column(scrollableframe, cluster):
    print(cluster)
    

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar2 = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas, width = 500, height = 500)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar2.set)

        canvas.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky="ns")
        scrollbar2.grid(row=1, column=0, sticky="ew")


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
        self.clusters_frame = ttk.Frame(master)
        self.clusters_frame.pack()
        self.clusters_frame_scrollable = ScrollableFrame(self.clusters_frame)
        #for i in range(50):
            #ttk.Label(self.clusters_frame_scrollable.scrollable_frame, text="Sample scrolling label").pack()


        
        self.clust_frames = {}
        self.scrollbars = {}
        self.clust_buttons = {}
        for cluster, values in clusters.items():
            #self.clust_frames["cluster{0}".format(cluster)] = ttk.Frame(self.scrollable_frame)
            #self.clust_frames["cluster{0}".format(cluster)].grid(row = clust_row, column = 0)
            #self.scrollbars["scrollbar{0}".format(cluster)] = ttk.Scrollbar(self.clust_frames["cluster{0}".format(cluster)], orient = 'horizontal', command = ) 
            #self.scrollbars["scrollbar{0}".format(cluster)].grid(row = 0, column = 0, sticky = 'ns')
            self.clust_buttons["cluster{0}_delete".format(cluster)] = ttk.Button(self.clusters_frame_scrollable.scrollable_frame, text = "X")
            self.clust_buttons["cluster{0}_delete".format(cluster)].grid(row = 0, column = cluster, padx = 5, pady = 5)
            self.clust_buttons["cluster{0}_delete".format(cluster)].configure(command=lambda: delete_column(self.clusters_frame_scrollable.scrollable_frame, this.grid_info()['column']))
            for n in range(len(values)):
                self.clust_buttons["cluster{0}_{1}".format(cluster, n)] = ttk.Button(self.clusters_frame_scrollable.scrollable_frame, text = values[n])
                self.clust_buttons["cluster{0}_{1}".format(cluster, n)].grid(row = n + 1, column = cluster, padx = 5, pady = 5)
            #clust_row += 1
        
        self.clusters_frame_scrollable.pack()
            
def main():

               
    root = tk.Tk()
    app = Feedback(root, "100 cluster group")
    root.mainloop()
    
if __name__ == "__main__": main()