
from pprint import pprint

import random
import time
import random
import pickle
import math
from PIL import ImageTk, Image

import PIL
import tkinter.filedialog
from tkinter import ttk #Somehow we need this imported seperately
import numpy as np
from tkinter import *
from tkinter import font as tkFont  # for convenience
from single_stream import single_stream, vdev_stream
import animations_new
from multiprocessing import Process
import os
# I know this program is written....poorly. But then again I spent absolute minimum time building this. Sorry future LANCo ;)


#TODO:
# Test with actual beundingen
# Make beundingen and Vdevs movable
# Think about duration/speed
# Make Blank re-insert old animations
# Create run_all function that runs all animations
# Maybe a percentage counter for each device running an animation?
# Make animation loop toggelable
# Add invert flag to objects
# Get packet length etc from childeren instead of vdev


class DragDropListbox(Listbox):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, **kw):
        kw['selectmode'] = SINGLE
        Listbox.__init__(self, master, kw)
        self.bind('<Button-1>', self.setCurrent)
        self.bind('<B1-Motion>', self.shiftSelection)
        self.curIndex = None

    def setCurrent(self, event):
        self.curIndex = self.nearest(event.y)

    def shiftSelection(self, event):
        i = self.nearest(event.y)
        if i < self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i + 1, x)
            self.curIndex = i
        elif i > self.curIndex:
            x = self.get(i)
            self.delete(i)
            self.insert(i - 1, x)
            self.curIndex = i


def doNothing(a=1):
    pass


class beunding:
    def __init__(self, x, y,number_of_created_objects):
        self.x = x
        self.y = y
        self.type = "beunding"
        self.previous_animation="blank"
        self.properties = {}
        self.text = ""
        self.number_of_created_objects = number_of_created_objects
        self.properties['type'] = self.type
        self.properties['Number'] = self.number_of_created_objects + 1
        self.properties['Name'] = "Thing #" + str(self.number_of_created_objects + 1)
        self.properties['IP Address'] = "1.1.1.1"
        self.properties['Port'] = "8888"
        self.properties['MAC Address'] = "FF-FF-FF-FF-FF"
        self.properties['Packet length'] = "320"
        self.properties['# LEDS'] = "300"
        self.properties['Group'] = "Default"
        self.properties['Vdev'] = "None"
        self.properties['Animation'] = "blank"
        self.properties['Running'] = "No"
        self.p = None
        self.selected = False
        self.rect = ""
        self.IP = self.properties["IP Address"]
        self.PORT = self.properties["Port"]
        self.PACKET_LENGTH = 320
        self.MAX_INDEX = 4095
        self.BITMULT = int(2 ** 4)
        self.command = bytes()

        number_of_created_objects += 1

    def start(self):

        if self.properties['Vdev'] == "None":
            print("Starting thread for normal beunding")
            if self.p != None:
                self.stop()
            self.fb = np.zeros((int(self.properties['# LEDS'])))  # Create frame buffer
            self.IP = self.properties["IP Address"]
            self.PORT = int(self.properties["Port"])

            self.p = Process(target=single_stream, args=(self.properties['# LEDS'],
                                                         self.properties['Animation'],
                                                         self.IP,
                                                         self.PORT,
                                                         self.MAX_INDEX,
                                                         self.BITMULT,
                                                         self.PACKET_LENGTH))
            self.p.daemon = True
            self.p.start()

    def stop(self):
        if self.p != None:
            self.p.terminate()
            self.p = None



class vdev:
    def __init__(self, x, y,number_of_created_objects):
        self.type = "vdev"
        self.x = x
        self.y = y
        self.properties = {}
        self.number_of_created_objects=number_of_created_objects
        self.text = ""
        self.properties['type'] = self.type
        self.properties['Number'] = self.number_of_created_objects + 1
        self.properties['Name'] = "Vdev" + str(self.number_of_created_objects)
        self.properties['# LEDS'] = 0
        self.previous_animation = "blank"
        self.properties['Group'] = "Default"
        self.properties['Animation'] = "blank"
        self.properties['Running'] = "No"
        self.PACKET_LENGTH = 320
        self.MAX_INDEX = 4095
        self.BITMULT = int(2 ** 4)

        self.properties['Childeren'] = []
        self.p = None
        self.fb = []
        self.selected = False
        self.rect = ""
        number_of_created_objects += 1

    def start(self):

        print("Starting thread Vdev")
        self.fb = {}
        print("Before starting process")

        if self.p != None:
            self.stop()
        print(self.p)
        child_ips=[]
        child_ports=[]
        child_leds=[]
        for obj in self.childeren_objects:
            child_ips.append(obj.properties["IP Address"])
            child_ports.append(int(obj.properties["Port"]))
            child_leds.append(int(obj.properties['# LEDS']))


        self.p = Process(target=vdev_stream, args=(self.properties["# LEDS"],
                                                   self.properties['Animation'],
                                                   child_ips,
                                                   child_ports,
                                                   child_leds,
                                                   self.MAX_INDEX,
                                                   self.BITMULT,
                                                   self.PACKET_LENGTH))
        self.p.daemon = True
        self.p.start()
        # single_stream(self)
        # time.sleep(1)
        print("Starting Process here")

    def stop(self):
        if self.p!=None:
            self.p.terminate()
            self.p=None




class App(Frame):
    # global adding, properties, obj_list, selected_obj, c, number_of_created_objects, tempx, tempy, master, groups, adding_type, animations, op1, op2, op3, op4, op5
    def __init__(self,master):
        self.number_of_created_objects = 0
        self.properties = []
        self.obj_list = []
        self.tempx = 0
        self.tempy = 0
        self.selected_obj = None
        self.temp_square = -1
        self.animations = ["blank", "regenboog", "BBB"]

        self.groups = ['Default']

        self.adding = 0
        self.adding_type = "beunding"
        self.master = master
        self.menu = Menu(self.master, tearoff=0)
        self.master.config(menu=self.menu)
        self.master.title("TesLAN Beun manager")
        self.master.geometry("800x600")
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Save setup', command=self.save_setup)
        self.filemenu.add_command(label='Load setup', command=self.load_setup)
        self.filemenu.add_command(label='---')
        self.filemenu.add_command(label='Exit', command=exit)

        self.addmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Add', menu=self.addmenu)
        self.addmenu.add_command(label='Add beunding', command=self.add_beunding)
        self.addmenu.add_command(label='Add virtual device', command=self.add_vdev)

        self.helpmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Help', menu=self.helpmenu)
        self.helpmenu.add_command(label='About')

        self.c = Canvas(self.master, width=600, height=400, bd=2, relief='ridge')

        # if adding c.coords(rect, x - 10, y - 10, x + 10, y + 10)
        self.mframe=Frame(master, highlightbackground="#bababa", highlightthickness=1)
        self.f0 = Frame(self.mframe)
        self.lb1 = Label(self.f0, width=15, text="General", anchor='center')
        self.ggframe = Frame(self.mframe)
        self.bbutton1 = Button(self.ggframe, text="Run all", height=2, width=10, bg='#3da13f', fg='white',
                              command=self.run_all)
        self.gframe = Frame(self.mframe)
        self.button1 = Button(self.gframe, text="Blank all", height=5, width=10, bg='#be0e55', fg='white', command=self.blank_all)
        self.f0.pack()
        self.lb1.pack()
        self.bbutton1.pack(anchor=NW)
        self.ggframe.pack()
        self.button1.pack(anchor=NW)
        self.gframe.pack(pady=10,padx=4)
        self.mframe.place(x=25, y=420)

        # groups
        self.gframe = Frame(self.master, highlightbackground="#bababa", highlightthickness=1)
        self.f0 = Frame(self.gframe)
        self.lb1 = Label(self.f0, width=15, text="Groups", anchor='center')
        self.f1 = Frame(self.gframe)
        self.op1 = Entry(self.f1, width=15)
        # op.insert(0, dict[field])
        self.bt1 = Button(self.f1, text="Add group", command=self.add_group)
        self.f2 = Frame(self.gframe)
        self.op2 = ttk.Combobox(self.f2, state="readonly", width=11, justify=LEFT)
        self.op2['values'] = self.groups
        self.bt2 = Button(self.f2, text="Delete group", command=self.remove_group)
        self.f3 = Frame(self.gframe)
        self.lb2 = Label(self.f3, width=15, text="With", anchor='w')
        self.op3 = ttk.Combobox(self.f3, state="readonly", width=11)
        self.op3['values'] = self.groups
        self.f5 = Frame(self.gframe)
        self.lb3 = Label(self.f5, width=15, text="set animation", anchor='w')
        self.op4 = ttk.Combobox(self.f5, state="readonly", width=11)
        self.op4['values'] = self.animations
        self.f6 = Frame(self.gframe)
        self.bt3 = Button(self.f6, text="Apply and run", command=self.set_group)
        self.lb1.pack()
        self.f0.pack()
        self.op1.pack(side=LEFT)
        self.bt1.pack(side=LEFT)
        self.f1.pack()
        self.op2.pack(side=LEFT)
        self.bt2.pack(side=LEFT)
        self.f2.pack()
        self.lb2.pack(side=LEFT)
        self.op3.pack(side=LEFT)
        self.f3.pack(pady=(20, 0))
        self.lb3.pack(side=LEFT)
        self.op4.pack(side=LEFT)
        self.f5.pack()
        self.bt3.pack()
        self.f6.pack()

        self.gframe.pack()
        self.gframe.place(x=150, y=420)

        self.frame = Frame(self.master, width=50, height=30)
        self.frame.pack()
        # Create an object of tkinter ImageTk
        self.im = PIL.Image.open("Logo.png")
        self.im.thumbnail((80, 80), PIL.Image.LANCZOS)
        self.img = ImageTk.PhotoImage(self.im)
        self.label = Label(self.frame, image=self.img)
        self.label.pack()
        self.frame.place(x=700, y=550)

        self.c.bind("<Button-1>", self.key)
        self.c.pack(side=TOP, anchor=NW)
        self.create_grid()



    def callback(self,event):
        self.tempx, self.tempy = event.x, event.y

        #
    def create_grid(self):
        w = 600 # Get current width of canvas
        h = 400# Get current height of canvas
        self.c.delete('grid_line') # Will only remove the grid_line

        # Creates all vertical lines at intevals of 100
        for i in range(0, w, 21):
            self.c.create_line([(i, 0), (i, h)],fill="#CFCFCF",tag='grid_line')

        # Creates all horizontal lines at intevals of 100
        for i in range(0, h, 21):
            self.c.create_line([(0, i), (w, i)],fill="#CFCFCF", tag='grid_line')

    def write_properties(self,a=1,b=1,c=1):
        #print(random.randint(0,100))
        j=0
        if self.selected_obj==None or len(self.properties)==0:
            pass
        else:
            #print("KAAS")
            for i in self.selected_obj.properties.keys():
                if (i == "# LEDS" and self.selected_obj.type=="vdev") or i == "type":
                    pass
                else:
                    if i == "Vdev" or i == "Name" or i== "Running":
                        self.selected_obj.properties[i] = self.properties[j][2].get()
                    elif i == "Childeren":
                        print("Writing childeren")
                        self.selected_obj.properties[i] = list(self.properties[j][0].get(0,10000))
                        j+=1 #Skip the field that is used to add things to list
                        j+=1 #Skip the StartStop field
                    else:
                        self.selected_obj.properties[i] = self.properties[j][0].get()
                j+=1
        self.read_properties()
        return True


    def find_object_by_name(self,name):
        obk = ""
        for obz in self.obj_list:
            if obz.properties['type'] == "beunding":
                if obz.properties['Name'] == name:
                    obk=obz
        if obk == "":
            raise ValueError("Trying to find unexisting object.")
        return obk
    def deselect_all(self):
        if len(self.properties) > 0:
            self.write_properties()
            for i in self.properties:
                i[1].destroy()
            self.properties = []
        for obj in self.obj_list:
            obj.selected = False
        self.selected_obj=None
    def update_vdev_leds(self):
        for obj in self.obj_list:
            if obj.type == "vdev":
                #Read LEC Count
                ledsum = 0
                for nm in obj.properties['Childeren']:
                    objecttt= self.find_object_by_name(nm)
                    if objecttt!="":
                        ledsum += int(objecttt.properties['# LEDS'])
                obj.properties["# LEDS"] = ledsum

    def update_dragdroplist(self):
        if self.selected_obj != None:
            i="Childeren"
            for j in self.properties:
                if i == j[3]:
                    if isinstance(j[0],DragDropListbox):
                        j[0].delete(0,END)
                        for q in self.selected_obj.properties[i]:
                            j[0].insert(END,q)
    def read_properties(self,a=1,b=1,c=1):
        if self.selected_obj != None:
            for i in self.selected_obj.properties.keys():
                for j in self.properties:
                    if i == j[3]:
                        if i == "StartStop":
                            pass
                        if isinstance(j[0],Label):
                            j[0].config(text=self.selected_obj.properties[i])
                            if j[-1] == "Running":
                                if self.selected_obj.properties[i]=="Yes":
                                    j[0].config(font=('Arial bold', 14), fg="green")
                                else:
                                    j[0].config(font=('Arial bold', 14), fg="red")

                        if isinstance(j[0],ttk.Combobox):
                            if i == "Child_select":
                                pass
                            else:
                                j[0].set(self.selected_obj.properties[i])
                        #note: Dragdroplist update is seperate
        for obj in self.obj_list:
            if obj.p != None:
                try:
                    obj.p.join(timeout=0)
                except:
                    print("An exception occurred")

                if obj.p.is_alive():
                    obj.properties["Running"] = "Yes"

                else:
                    obj.properties["Running"] = "No"
            else:
                obj.properties["Running"] = "No"


                        #j[2]=selected_obj.properties[i]

    def key(self,event):

        if self.adding==1:
            self.adding=0
            if self.adding_type=="beunding":
                d=beunding(event.x,event.y,self.number_of_created_objects)
                self.number_of_created_objects+=1
            else:
                d=vdev(event.x, event.y,self.number_of_created_objects)
                self.number_of_created_objects+=1
            self.obj_list.append(d)
            self.c.unbind('<Motion>')
            self.c.pack()
        else:
            self.deselect_all()
            for obj in self.obj_list:
                if event.x > obj.x -10 and event.x < obj.x + 10 and event.y > obj.y -10 and event.y < obj.y + 10:
                    obj.selected=True
                    self.selected_obj = obj
                    self.properties=self.makeform(obj.properties)
                    self.read_properties()
                    self.update_vdev_leds()
                    self.update_dragdroplist()


    def run_all(self):
        self.deselect_all()
        for obj in self.obj_list:
            if "Vdev" in obj.properties.keys() and obj.properties["Vdev"] != "None":
                pass
            else:
                #Update Vdev so that it knows its childeren
                if obj.properties['type']=="vdev":
                    obj.childeren_objects = []
                    for obg in obj.properties['Childeren']:
                        obj.childeren_objects.append(self.find_object_by_name(obg))
                obj.start()

    def blank_all(self):
        self.deselect_all()
        for obj in self.obj_list:
            if "Vdev" in obj.properties.keys() and obj.properties["Vdev"] != "None":
                pass
            else:
                obj.previous_animation = obj.properties['Animation']
                obj.properties['Animation'] = "blank"
                #Update Vdev so that it knows its childeren
                if obj.properties['type']=="vdev":
                    obj.childeren_objects = []
                    for obg in obj.properties['Childeren']:
                        obj.childeren_objects.append(self.find_object_by_name(obg))
                obj.start()
                obj.properties['Animation']=obj.previous_animation

    def save_setup(self):

        f = filedialog .asksaveasfile(mode='w', defaultextension=".pkl")
        if f == None:
            return
        file = open(f.name, 'wb')
        pickle.dump(len(self.obj_list), file)
        for i in self.obj_list:
            i.stop()
            pickle.dump(i,file)
        file.close()

    def clear_objects(self):
        self.c.delete("all")
        self.obj_list=[]
        self.create_grid()
    def load_setup(self):
        f = filedialog.askopenfilename(defaultextension=".pkl")
        #f= "C:\\Users\\20182653\\Desktop\\TESLAN\\2023-Beun-LANCo\\SyncStream\\Multistream\\Saved setups\\Whoah.pkl"
        if f == '':
            return
        self.clear_objects()
        file = open(f, 'rb')
        n_objects = pickle.load(file)
        for i in range(n_objects):
            obj=pickle.load(file)
            self.obj_list.append(obj)
            obj.rect=""
            obj.text=""
        self.number_of_created_objects=len(self.obj_list)
        file.close()

    def exit(self):
        self.master.destroy()
        self.master="stop"
    def add_grid(self):
        self.c.bind("<Configure>", self.create_grid)
        self.c.pack(side=TOP, anchor=NW)
    def add_beunding(self):
        self.adding=1
        self.adding_type="beunding"
        self.c.bind('<Motion>', self.callback)
        self.c.pack()

    def add_vdev(self):
        self.adding = 1
        self.adding_type="vdev"
        self.c.bind('<Motion>', self.callback)
        self.c.pack()

    def set_text(self,op,text):
        op.delete(0, END)
        op.insert(0, text)
        return
    def add_group(self):
        if self.op1.get() !="":
            if not self.op1.get() in self.groups:
                self.groups.append(self.op1.get())
            else:
                messagebox.showinfo("Eyy", "That group already exists.")
            self.set_text(self.op1,"")

    def remove_group(self):
        if self.op2.get() in self.groups:
            if self.op2.get() == "Default":
                messagebox.showinfo("Eyy", "Cannot remove Default group")
            else:
                self.groups.remove(self.op2.get())
                for obj in self.obj_list:
                    if obj.properties['Group'] == self.op2.get():
                        obj.properties['Group'] = "Default"
        else:
            messagebox.showinfo("Eyy", "That group was already removed.")
        self.op2.set("")
    def set_group(self):
        self.write_properties()
        if self.op4.get()!= "":
            self.deselect_all()
            for obj in self.obj_list:
                if obj.properties['Group'] == self.op3.get():
                    obj.stop()
                    obj.properties['Animation'] = self.op4.get()
                    if "Vdev" in obj.properties.keys():
                        if obj.properties['Vdev'] == "None":
                            obj.start()
                    else:
                        if obj.properties['type'] == "vdev":
                            obj.childeren_objects = []
                            for obg in obj.properties['Childeren']:
                                obj.childeren_objects.append(self.find_object_by_name(obg))
                        obj.start()
            self.op4.set("")
        else:
            messagebox.showinfo("Eyy", "Please select an animation first.")
        #op3.set("")




    #add_grid(c) #Deze doet ook pack

    # button1.pack()

    def kill_child(self):
        new_child = ""
        for i in self.properties:
            if isinstance(i[0], OptionMenu):
                if i[3] == "Child_select":
                    new_child = i[2].get()
        if not new_child == "":
            if new_child in self.selected_obj.properties['Childeren']:
                self.selected_obj.properties['Childeren'].remove(new_child)
                chld = self.find_object_by_name(new_child)
                chld.properties["Vdev"] = "None"
        self.read_properties()
        self.update_vdev_leds()
        self.update_dragdroplist()
    def adopt_child(self):

        new_child = ""
        for i in self.properties:
            if isinstance(i[0],OptionMenu):
                if i[3] == "Child_select":
                    new_child = i[2].get()
        if not new_child=="":
            if not new_child in self.selected_obj.properties['Childeren']:
                self.selected_obj.properties['Childeren'].append(new_child)
                chld=self.find_object_by_name(new_child)
                chld.properties["Vdev"]=self.selected_obj.properties['Name']
            else:
                messagebox.showinfo("Eyy", "That object is already a child of this virtual device.")
        self.read_properties()
        self.update_vdev_leds()
        self.update_dragdroplist()
    def start_wrapper(self):
        self.write_properties()
        obj=self.selected_obj
        if obj.properties['type'] == "vdev":
            obj.childeren_objects = []
            for obg in obj.properties['Childeren']:
                obj.childeren_objects.append(self.find_object_by_name(obg))
        self.selected_obj.start()
    def makeform(self, dict):
        entries = []
        i=0

        for field in list(dict.keys()):
            row = Frame(self.master)
            if field != "Childeren":
                lab = Label(row, width=10, text=field, anchor='w')
            sv = StringVar(value=dict[field])
            #sv.trace_add('write', write_properties())
            packed=0
            if field == "Animation":
                en = DISABLED
                if 'Vdev' in dict.keys():
                    if dict['Vdev'] == "None":
                        en = "readonly"
                if dict['type'] == "vdev":
                    en = "readonly"
                ent = ttk.Combobox(row,width=12)
                ent.bind('<<ComboboxSelected>>', self.write_properties)
                ent['values'] = self.animations
                ent.configure(state=en)
            elif field == "Group":
                ent = ttk.Combobox(row,width=12, state="Readonly")
                ent.bind('<<ComboboxSelected>>',self. write_properties)
                ent['values'] = self.groups
            elif field == "Running":
                ent = Label(row, width=10, text=dict[field], anchor='w')
            elif field == "Vdev" or field=="Name":
                ent = Label(row, width=10, text=dict[field], anchor='w')

            elif field == "Childeren":

                m = Frame(self.master)
                k = Frame(m)
                sv = StringVar()
                lab = Label(k, width=10, text="Childeren:", anchor='w')
                ent = DragDropListbox(k, width=25)
                ent.config(width=25)
                for child in self.selected_obj.properties['Childeren']:
                    ent.insert(END, child)
                packed = 1
                k.pack(side=TOP, fill=X, padx=2, pady=2)
                lab.pack(side=TOP, padx=10)
                ent.pack(side=TOP, padx=0)
                entries.append((ent, k, sv,field))
                k = Frame(m)
                a = [h for h in self.obj_list if h.type == "beunding"]
                e = [n.properties['Name'] for n in list(set(a))]  # - set(self.selected_obj.properties['Childeren']
                if len(e) > 0:
                    child_select = OptionMenu(k, sv, *e)
                    child_select.config(width=10)
                    butt = Button(k, text="+", command=self.adopt_child)
                    butt2 = Button(k, text="-", command=self.kill_child)
                    k.pack(side=TOP, fill=X, padx=2, pady=2)
                    child_select.pack(side=LEFT)
                    butt.pack(side=LEFT)
                    butt2.pack(side=LEFT)
                    entries.append((child_select, k, sv,"Child_select"))
                m.place(x=610, y=20 + 210)

                packed=1
            else:
                if field == "type" or  (dict['type'] == "vdev" and field == "# LEDS"):
                    ent = Label(row, width=10, text=dict[field], anchor='w')
                else:
                    ent = Entry(row, width=15, validate="focusout",validatecommand=self.write_properties)
                    ent.insert(0, dict[field])
            if not packed:
                row.pack(side=TOP, fill=X, padx=2, pady=2)
                lab.pack(side=LEFT)
                ent.pack(side=RIGHT, expand=YES, fill=X)
                row.place(x=610, y=20+i*30)
                entries.append((ent,row,sv,field))
            i+=1
        if dict['type'] == "beunding" and dict['Vdev'] != "None":
            pass
        else:
            field="StartStop"
            f = Frame(self.master)
            g = Button(f, text="⏵", command=self.start_wrapper,bg='#be0e55', fg='white', width = 4, height=1)
            g2 = Button(f, text="⏹", command=self.selected_obj.stop,bg='#be0e55', fg='white', width = 4, height=1)
            g['font']=tkFont.Font(family='Arial', size=14)
            g2['font'] = tkFont.Font(family='Arial', size=14)
            g.pack(side=RIGHT, padx=4)
            g2.pack(side=RIGHT, padx=4)
            #f.pack()
            if dict['type']=="vdev":
                f.place(x=610, y=20+445)
            else:
                f.place(x=610, y=20 + 330)
            entries.append((g2, f, None, field))
            i+=1
        return entries
    #c.place(x=10, y=10)
    # load_setup()

    #master.mainloop()



if __name__ == "__main__":
    master=Tk()
    #
    a=App(master)
    #master.mainloop()


    while (a.master != "stop"):
        if a.adding == 1:
            if a.temp_square == -1:
                a.rect = a.c.create_rectangle(0, 0, 0, 0)
            a.temp_square = a.c.coords(a.rect, a.tempx - 10, a.tempy - 10, a.tempx + 10, a.tempy + 10)
        else:
            if not a.temp_square == -1:
                a.c.delete(a.temp_square)
                a.c.delete(a.rect)
                a.temp_square = -1
        for obj in a.obj_list:
            if obj.rect == "":
                obj.rect = a.c.create_rectangle(0, 0, 0, 0)
            if obj.text == "":
                obj.text = a.c.create_text(obj.x, obj.y, text=obj.properties['Number'], fill="black",
                                              font=('Helvetica 12 bold'))
            if obj.selected == False:
                if obj.type == "beunding":
                    if obj.properties['Vdev'] == "None":
                        if obj.properties["Running"] == "No":
                            a.c.itemconfig(obj.rect, fill='red')
                        else:
                            a.c.itemconfig(obj.rect, fill='green')
                    else:
                        if obj.properties['Running'] == "No":
                            a.c.itemconfig(obj.rect, fill='#cb8ced')
                        else:
                            a.c.itemconfig(obj.rect, fill='#8cedb1')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
                else:
                    if obj.properties["Running"] == "No":
                        a.c.itemconfig(obj.rect, fill='#fc9088')
                    else:
                        a.c.itemconfig(obj.rect, fill='#88fca3')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
            else:
                if obj.type == "beunding":

                    a.c.itemconfig(obj.rect, fill='#FFF')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
                else:
                    a.c.itemconfig(obj.rect, fill='#FFF')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
            if obj.type == "beunding":
                a.c.coords(obj.rect, obj.x - 10, obj.y - 10, obj.x + 10, obj.y + 10)
            else:
                a.c.coords(obj.rect, obj.x - 14, obj.y - 14, obj.x + 14, obj.y + 14)
        a.read_properties()
        # write_properties()
        a.op2['values'] = a.groups
        a.op3['values'] = a.groups
        master.update_idletasks()
        master.update()

#
#
#
# root = Tk()
#
# root.mainloop()