from tkinter import Tk, Label, Entry, Button, StringVar
from tkinter.filedialog  import askdirectory 
from tkinter.ttk import Combobox
import download
import text

print('Welcome to Pic finder\n')
input('Press Enter to continue...')

def method():
    gui()
    if data['method'] == 'Download pictures':
        download.search(data)
        again()
    elif data['method'] == 'Store links in a .txt file':
        text.search(data)
        again()

def exit_func():
    print('Exiting program...')
    exit()

def gui():
    global window, data

    data = None
    
    window = Tk()
    window.title('Options')
    window.geometry('600x400')
    window.resizable(height=False, width=False)

    def Search():
        global search_entry
        Label(window, text='Search:', font=('tahoma', 15)).place(relx=0.05, rely=0.03)
        search_entry = Entry(window, font=80, width=60)
        search_entry.place(relx=0.05, rely=0.1)
    
    def choose_path():
        chosen_save_path = askdirectory(initialdir="/", title="Select file")
        save_path.config(state='normal')
        save_path.insert(0, chosen_save_path)
        save_path.config(state="readonly")

    def path():
        global save_path        

        Label(window, text='Select a folder to save the files to:', font=('tahoma', 15)).place(relx=0.05, rely=0.20)
        
        save_path = Entry(window, font=80, width=45, state="readonly")
        save_path.place(relx=0.05, rely=0.27)

        Button(window, text='Select folder', bd=1, font=('tahoma', 12), command=choose_path).place(relx=0.79, rely=0.255)
        
    def Combo():
        global method_combo, time_combo, sizes_combo, colors_combo, types_combo, layouts_combo
        Label(window, text='Options:', font=('tahoma', 15)).place(relx=0.05, rely=0.4)

        method_list = ['Download pictures', 'Store links in a .txt file']
        time_list = ['Any time', 'Past day', 'Past week', 'Past month']
        sizes_list = ['All sizes', 'Small', 'Medium', 'Large', 'Wallpaper']
        colors_list = ['All colors', 'Color only', 'Black and white', 'Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Pink', 'Brown', 'Black', 'Gray', 'Teal', 'White']
        types_list = ['All types', 'Photograph', 'Clipart', 'Animated GIF', 'Transparent', 'Line Drawing']
        layouts_list = ['All layouts', 'Square', 'Tall', 'Wide']

        method_combo = Combobox(window, values=method_list, state="readonly")
        time_combo = Combobox(window, values=time_list, state="readonly")
        sizes_combo = Combobox(window, values=sizes_list, state="readonly")
        colors_combo = Combobox(window, values=colors_list, state="readonly")
        types_combo = Combobox(window, values=types_list, state="readonly")
        layouts_combo = Combobox(window, values=layouts_list, state="readonly")

        method_combo.set('Download pictures')
        method_combo.place(relx=0.05, rely=0.5)
        time_combo.set('Any time')
        time_combo.place(relx=0.38, rely=0.5)
        sizes_combo.set('All sizes')
        sizes_combo.place(relx=0.72, rely=0.5)
        colors_combo.set('All colors')
        colors_combo.place(relx=0.05, rely=0.6)
        types_combo.set('All types')
        types_combo.place(relx=0.38, rely=0.6)
        layouts_combo.set('All layouts')
        layouts_combo.place(relx=0.72, rely=0.6)

    def resolution():
        global height, width

        def validate_input(new_value):
            valid = new_value.isdigit() and len(new_value) <= 8
            return valid
        validate = window.register(validate_input)

        Label(window, text='Height:', font=('tahoma', 15)).place(relx=0.05, rely=0.75)
        Label(window, text='Width:', font=('tahoma', 15)).place(relx=0.05, rely=0.85)
        height = StringVar()
        width = StringVar()
        Entry(window, textvariable=height, validate="key", validatecommand=(validate, "%P")).place(relx=0.2, rely=0.77)
        Entry(window, textvariable=width, validate="key", validatecommand=(validate, "%P")).place(relx=0.2, rely=0.87)
        
    def check():
        if search_entry.get() != '' and save_path.get() != '' and (height.get() != '' or width.get() != ''):
            return_data()
        elif search_entry.get() == '' or save_path.get() == '':
            if search_entry.get() == '':
                Label(window, text='This field cannot be empty', font=('tahoma', 10), fg='red').place(relx=0.7, rely=0.16)
                Search()
            if save_path.get() == '':
                Label(window, text='This field cannot be empty', font=('tahoma', 10), fg='red').place(relx=0.478, rely=0.33)
                path()

        if height.get() == '' and width.get() == '':
            Label(window, text='At least fill in one of these fields', font=('tahoma', 10), fg='red').place(relx=0.05, rely=0.7)
            resolution()
        
    def return_data():
        global data
        data = {}
        data['search word'] = search_entry.get()
        data['save path'] = save_path.get()
        data['method'] = method_combo.get()
        data['time'] = time_combo.get()
        data['size'] = sizes_combo.get()
        data['color'] = colors_combo.get()
        data['type'] = types_combo.get()
        data['layout'] = layouts_combo.get()
        data['height'] = height.get()
        data['width'] = width.get()

        window.destroy()
    
    Search()
    path()
    Combo()
    resolution()

    Button(window, text='Search', bd=1, font=('tahoma', 20), command=check).place(relx=0.8, rely=0.85, anchor='center')

    window.mainloop()
    
    make_link(data)

def make_link(data):
    if data == None:
        exit_func()

    url = 'https://duckduckgo.com/?q={}&iax=images&ia=images'.format(data['search word'].replace(' ', '+'))

    # time
    if data['time'] != 'Any time':
        if data['time'] == 'Past day':
            url += '&iaf=time%3ADay'
        elif data['time'] == 'Past week':
            url += '&iaf=time%3AWeek'
        elif data['time'] == 'Past month':
            url += '&iaf=time%3AMonth'

    # size 
    if data['size'] != 'All sizes':
        if data['size'] == 'Small':
            url += '&iaf=size%3ASmall'
        elif data['size'] == 'Medium':
            url += '&iaf=size%3AMedium'
        elif data['size'] == 'Large':
            url += '&iaf=size%3ALarge'
        elif data['size'] == 'Wallpaper':
            url += '&iaf=size%3AWallpaper'

    # color
    if data['color'] != 'All colors':
        if data['color'] == 'Color only':
            url += '&iaf=color%3Acolor'
        elif data['color'] == 'Black and white':
            url += '&iaf=color%3AMonochrome'
        elif data['color'] == 'Red':
            url += '&iaf=color%3ARed'
        elif data['color'] == 'Orange':
            url += '&iaf=color%3AOrange'
        elif data['color'] == 'Yellow':
            url += '&iaf=color%3AYellow'
        elif data['color'] == 'Green':
            url += '&iaf=color%3AGreen'
        elif data['color'] == 'Blue':
            url += '&iaf=color%3ABlue'
        elif data['color'] == 'Purple':
            url += '&iaf=color%3APurple'
        elif data['color'] == 'Pink':
            url += '&iaf=color%3APink'
        elif data['color'] == 'Brown':
            url += '&iaf=color%3ABrown'
        elif data['color'] == 'Black':
            url += '&iaf=color%3ABlack'
        elif data['color'] == 'Gray':
            url += '&iaf=color%3AGray'
        elif data['color'] == 'Teal':
            url += '&iaf=color%3ATeal'
        elif data['color'] == 'White':
            url += '&iaf=color%3AWhite'

    # types
    if data['type'] != 'All types':
        if data['type'] == 'Photograph':
            url += '&iaf=type%3Aphoto'
        elif data['type'] == 'Clipart':
            url += '&iaf=type%3Aclipart'
        elif data['type'] == 'Animated GIF':
            url += '&iaf=type%3Agif'
        elif data['type'] == 'Transparent':
            url += '&iaf=type%3Atransparent'
        elif data['type'] == 'Line Drawing':
            url += '&iaf=type%3Aline'

    # layout
    if data['layout'] != 'All layouts':
        if data['layout'] == 'Square':
            url += '&iaf=layout%3ASquare'
        elif data['layout'] == 'Tall':
            url += '&iaf=layout%3ATall'
        elif data['layout'] == 'Wide':
            url += '&iaf=layout%3AWide'


    url = url[::-1]
    amount = url.count('=fai&')
    url = url.replace('=fai&', 'C2%', amount-1)
    url = url[::-1]

    data['url'] = url
    return data

def again():
    print('Do you want search again?')
    print('1 - Search')
    print('2 - search for current searched title')
    print('0 - Exit')
    act = input('--> ')
    if act.lower() in ['1', 'search']:
        gui()
        if data['method'] == 'Download pictures':
            download.search(data)
        elif data['method'] == 'Store links in a .txt file':
            text.search(data)
    elif act == '2':
        if data['method'] == 'Download pictures':
            download.check_to_download(data)
        elif data['method'] == 'Store links in a .txt file':
            text.check_to_store(data)
    elif act.lower() in ['0', 'exit']:
        exit_func()    
    else:
        print('Input is incorrect. Try again. ')
        again()
    again()

method()