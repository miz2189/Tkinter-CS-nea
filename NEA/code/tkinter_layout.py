import tkinter as tk

root = tk.Tk()
root.title("Tkinter Layout")
root.geometry("800x600")

root.configure(bg="grey")

l1 = tk.Label(root, text="Quiz title", bg="#5e76d6", font=("Arial", 40))
l1.pack(side = "top", pady = 10)
l2 = tk.Label(root, text="Login", bg="#5e76d6", font=("Arial", 30))
l2.pack(side = "top", pady = 100)



root.mainloop()