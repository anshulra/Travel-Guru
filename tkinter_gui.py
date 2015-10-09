from tkinter import *
import tkinter.scrolledtext as scrolledtext
	
top_window = Tk()

top_window.title("TravelGuRu")

title = Label(top_window, text="TravelGuRu\n", font="Helvetica 24 bold underline")
title.pack(fill='x')

br = Label(top_window, text="" )
br.pack()

main_frame = Frame(top_window)
main_frame.pack(fill='x', padx='350')

prompt = Label(main_frame, text="Travel query:", font="Helvetica 14 bold")
prompt.pack(side="left")

search_box = Entry(main_frame, width=50)
search_box.pack(side="left")
search_box.insert(0,"Find your ideal vacation...")

search_button = Button(main_frame, text="Search", width=5, height=1, command=callSearch)
search_button.pack(side="left", padx='10')

br = Label(top_window, text="" )
br.pack()

output_frame = Frame(top_window)
output_frame.pack(fill='x', padx='50')

output_area_1 = scrolledtext.ScrolledText(output_frame, width=70, height=50, bg='#FFF0E0')

output_area_2 = scrolledtext.ScrolledText(output_frame, width=95, height=50, bg='#FFF0E0')

########
top_window.mainloop()



