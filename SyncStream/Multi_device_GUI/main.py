
from pprint import pprint
import string
import random
import time
import random
import pickle
import math
from PIL import ImageTk, Image

import PIL
import tkinter.filedialog
from tkinter import ttk #Somehow we need this imported seperately
from tkinter import colorchooser
import numpy as np
from tkinter import *
from tkinter import font as tkFont  # for convenience
from single_stream import single_stream, vdev_stream
import animations_new
from multiprocessing import Process
import os
import animations_new  # import c_animations
import inspect

def read_animations():
    a = inspect.getmembers(animations_new.c_animations(), predicate=inspect.ismethod)
    animations = []
    blacklist = ["__init__", "cycle","set_colour","try_set_written"]
    for b in a:
        if not (b[0] in blacklist):
            animations.append(b[0])
    return animations


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
# Get packet length etc from Children instead of vdev


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
        self.sweephash=""
        self.previous_animation="blank"
        self.properties = {}
        self.text = ""
        self.line=""
        self.number_of_created_objects = number_of_created_objects
        self.properties['type'] = self.type
        self.properties['Number'] = self.number_of_created_objects + 1
        self.properties['Name'] = "Thing " + str(self.number_of_created_objects + 1)
        self.properties['IP Address'] = "1.1.1.1"
        self.properties['Port'] = "8888"
        self.properties['MAC Address'] = "FF-FF-FF-FF-FF"
        self.properties['Packet length'] = "320"
        self.properties['Invert'] = False
        self.properties['# LEDS'] = "300"
        self.properties['Group'] = "Default"
        self.properties['Vdev'] = "None"
        self.properties['Animation'] = "blank"
        self.properties['Color'] = (0,0,0)
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
        self.deleteme=0

        number_of_created_objects += 1

    def delete_me(self):
        self.deleteme=1
            #Uh I guess that it is still referenced SOMEWHERE as __del__ is apparently not called... but whatever, who is going to delete millions of objects anyway?
    def start(self):

        if self.properties['Vdev'] == "None":
            #print("Starting thread for normal beunding")
            if self.p != None:
                self.stop()
            self.fb = np.zeros((int(self.properties['# LEDS'])))  # Create frame buffer
            self.IP = self.properties["IP Address"]
            self.PORT = int(self.properties["Port"])

            self.p = Process(target=single_stream, args=(self.properties['# LEDS'],
                                                         self.properties['Animation'],
                                                         self.properties['Color'],
                                                         self.properties["Invert"],
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

    def blank(self):
        self.previous_animation=self.properties['Animation']
        self.properties['Animation'] = "blank"
        self.stop()
        self.start()
        self.properties['Animation'] = self.previous_animation



class vdev:
    def __init__(self,x, y,number_of_created_objects):
        self.type = "vdev"
        self.x = x
        self.y = y
        self.properties = {}
        self.sweephash=''
        self.number_of_created_objects=number_of_created_objects
        self.text = ""
        self.properties['type'] = self.type
        self.properties['Number'] = self.number_of_created_objects + 1
        self.properties['Name'] = "Vdev " + str(self.number_of_created_objects)
        self.properties['# LEDS'] = 0
        self.previous_animation = "blank"
        self.properties['Group'] = "Default"
        self.properties['Animation'] = "blank"
        self.properties['Color'] = (0, 0, 0)
        self.properties['Running'] = "No"
        self.PACKET_LENGTH = 320
        self.MAX_INDEX = 4095
        self.BITMULT = int(2 ** 4)
        self.Children_objects=[]
        self.deleteme=0
        self.line=""

        self.properties['Children'] = []
        self.p = None
        self.fb = []
        self.selected = False
        self.rect = ""
        number_of_created_objects += 1
    def delete_me(self):
        self.deleteme=1

    def start(self):

        #print("Starting thread Vdev")
        if len(self.Children_objects)>0:
            self.fb = {}
            if self.p != None:
                self.stop()
            child_ips=[]
            child_ports=[]
            child_leds=[]
            child_inverts=[]
            for obj in self.Children_objects:
                child_ips.append(obj.properties["IP Address"])
                child_ports.append(int(obj.properties["Port"]))
                child_leds.append(int(obj.properties['# LEDS']))
                child_inverts.append(int(obj.properties['Invert']))

            self.p = Process(target=vdev_stream, args=(self.properties["# LEDS"],
                                                       self.properties['Animation'],
                                                       self.properties['Color'],
                                                       child_ips,
                                                       child_ports,
                                                       child_leds,
                                                       child_inverts,
                                                       self.MAX_INDEX,
                                                       self.BITMULT,
                                                       self.PACKET_LENGTH))
            self.p.daemon = True
            self.p.start()


    def stop(self):
        if self.p!=None:
            self.p.terminate()
            self.p=None
    def blank(self):
        self.previous_animation=self.properties['Animation']
        self.properties['Animation'] = "blank"
        self.stop()
        self.start()
        self.properties['Animation'] = self.previous_animation




class App(Frame):
    # global adding, properties, obj_list, selected_obj, c, number_of_created_objects, tempx, tempy, master, groups, adding_type, animations, op1, op2, op3, op4, op5
    def __init__(self,master):
        self.number_of_created_objects = 0
        self.properties = []
        self.obj_list = []
        self.tempx = 0
        self.group_mode="instant"
        self.tempy = 0
        self.selected_obj = None
        self.temp_square = -1
        self.animations = read_animations()

        self.groups = ['Default']

        self.adding = 0
        self.moving = 0
        self.adding_type = "beunding"
        self.master = master
        self.menu = Menu(self.master, tearoff=0)
        self.master.config(menu=self.menu)
        self.master.title("TesLAN Beun manager")
        self.master.geometry("800x600")
        self.master.iconbitmap("Logo_Teslan_coil.ico")
        self.filemenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Save setup', command=self.save_setup)
        self.filemenu.add_command(label='Load setup', command=self.load_setup)
        self.filemenu.add_command(label='Export to legacy YAML', command=self.export_yaml)
        self.filemenu.add_command(label='---')
        self.filemenu.add_command(label='Exit', command=exit)
        self.sweeping=0;

        self.addmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Add', menu=self.addmenu)
        self.addmenu.add_command(label='Add beunding', command=self.add_beunding)
        self.addmenu.add_command(label='Add virtual device', command=self.add_vdev)

        self.helpmenu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Credits', menu=self.helpmenu)
        self.helpmenu.add_command(label='Eloy Schultz | Eloy')
        self.helpmenu.add_command(label='Max Winsemius | Hernivo')
        self.helpmenu.add_command(label='Mathijs Verhaegh | Ostheer')
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
        self.f0 = self.gframe#Frame(self.gframe)
        self.lb1 = Label(self.f0, width=15, text="Groups", anchor='center')
        self.f1 = self.gframe#Frame(self.gframe)
        self.op1 = Entry(self.f1, width=14)
        # op.insert(0, dict[field])
        self.bt1 = Button(self.f1, text="Add group", command=self.add_group)
        self.f2 = self.gframe#Frame(self.gframe)
        self.op2 = ttk.Combobox(self.f2, state="readonly", width=11, justify=LEFT)
        self.op2['values'] = self.groups
        self.bt2 = Button(self.f2, text="Delete group", command=self.remove_group)
        self.f3 = self.gframe#Frame(self.gframe)
        self.lb2 = Label(self.f3, width=10, text="With", anchor='w')
        self.op3 = ttk.Combobox(self.f3, state="readonly", width=11)
        self.op3['values'] = self.groups
        self.op3.set(value="Default")
        self.f5 = self.gframe#Frame(self.gframe)
        self.lb3 = Label(self.f5, width=10, text="Set animation", anchor='w')
        self.op4 = ttk.Combobox(self.f5, state="readonly", width=11)
        self.bt3 = Button(self.f5, text="Set animation", command=self.set_group)
        self.op4['values'] = self.animations
        self.f6 = self.gframe#Frame(self.gframe)
        self.lb4 = Label(self.f6, width=10, text="Act. direction", anchor='w')
        self.op5 = ttk.Combobox(self.f6, state="readonly", width=11)
        self.op5['values'] = ["instant","E","W","N","S","NW","SW","NE","SE"] #en miss meer
        self.op5.set(value="instant")
        self.f7 = self.gframe#Frame(self.gframe)
        self.lb5 = Label(self.f7, width=10, text="Act. speed", anchor='w')
        self.op6 = Entry(self.f7, width=14)
        self.op6.insert(0,"1")
        self.bt5 = Button(self.f7, text="Activate group", command=self.run_group)
        self.bt4 = Button(self.f7, text="Blank group", command=self.blank_group)
        self.lb1.grid(row=0,column=1)
        self.op1.grid(row=1,column=1)
        self.bt1.grid(row=1,column=2,sticky=W)
        self.op2.grid(row=2,column=1)
        self.bt2.grid(row=2,column=2,sticky=W)
        self.lb2.grid(row=3,column=0)

        self.op3.grid(row=3,column=1)
        self.lb3.grid(row=4,column=0)
        self.op4.grid(row=4, column=1) #= ttk.Combobox(self.f5, state="readonly", width=11)
        self.bt3.grid(row=4,column=2,sticky=W)
        self.lb4.grid(row=5,column=0) #= Label(self.f6, width=10, text="Activation", anchor='w')
        self.op5.grid(row=5,column=1)# = ttk.Combobox(self.f6, state="readonly", width=3)
        self.bt4.grid(row=5, column=2,sticky=W)
        self.lb5.grid(row=6,column=0)# = Label(self.f7, width=10, text="Act. speed", anchor='w')
        self.op6.grid(row=6,column=1)# = Entry(self.f7, width=2)
        self.bt5.grid(row=6,column=2,sticky=W)
        # self.lb1.pack()
        # self.f0.pack()
        # self.op1.pack(side=LEFT)
        # self.bt1.pack(side=LEFT)
        # self.f1.pack()
        # self.op2.pack(side=LEFT)
        # self.bt2.pack(side=LEFT)
        # self.f2.pack()
        # self.lb2.pack(side=LEFT)
        # self.op3.pack(side=LEFT, padx=(0,60))
        # self.f3.pack(pady=(2, 0))
        # self.lb3.pack(side=LEFT)
        # self.op4.pack(side=LEFT, padx=(0,10))
        # self.bt3.pack(side=LEFT, padx=5)
        # self.f5.pack()
        # self.lb4.pack(side=LEFT)
        # self.op5.pack(side=LEFT, padx=(0))
        # #self.bt4.pack(side=LEFT,padx=5)
        # self.f6.pack()
        # self.lb5.pack(side=LEFT)
        # self.op6.pack(side=LEFT, padx=(0, 10))
        # self.bt4.pack(side=LEFT, padx=5)
        # self.f7.pack()

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

    def choose_color(self):

        # variable to store hexadecimal code of color
        color_code = colorchooser.askcolor(title ="Choose color")
        if color_code[0]==None:
            return
        print(color_code)
        color=color_code[0]
        print(color)
        color= tuple(int(x/255*15) for x in color) #int(255/x*15)
        print(color)
        if sum(color)/3 > 10:
            messagebox.showinfo("Eyy", "That color has an average value of above 10, which will induce much current (things are more likely to catch fire lol). Maybe you want to reconsider your choice?")
        self.selected_obj.properties['Color'] = color
        self.read_properties()
        #return color


    def check_input(self,event,lst,box): #For animation autofill
        value = event.widget.get()

        if value == '':
            box['values'] = lst
        else:
            data = []
            for item in lst:
                if value.lower() in item.lower():
                    data.append(item)

            box['values'] = data

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
        j=0
        if self.selected_obj==None or len(self.properties)==0:
            pass
        else:
            for i in self.selected_obj.properties.keys():
                if (i == "# LEDS" and self.selected_obj.type=="vdev") or i == "type":
                    pass
                else:

                    if i == "Vdev" or i == "Name" or i=="Number" or i== "Running" or i == "Invert":
                        self.selected_obj.properties[i] = self.properties[j][2].get()
                    elif i == "Children":
                        self.selected_obj.properties[i] = list(self.properties[j][0].get(0,10000))

                        for obj in self.obj_list:
                            if obj.type=="beunding":
                                if obj.properties['Vdev'] == self.selected_obj.properties['Name']:
                                    self.c.coords(obj.line, obj.x, obj.y, self.selected_obj.x, self.selected_obj.y)

                        j+=1 #Skip the field that is used to add things to list
                        j+=1 #Skip the StartStop field

                    elif i != "Color":
                        try:
                            self.selected_obj.properties[i] = self.properties[j][0].get()
                        except:
                            if (len(self.properties)>0):
                                print("An exception occurred")

                j+=1
        self.read_properties()
        return True


    def find_object_by_name(self,name):
        obk = ""
        for obz in self.obj_list:
            #if obz.properties['type'] == "beunding":
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
                for nm in obj.properties['Children']:
                    objecttt= self.find_object_by_name(nm)
                    if objecttt!="":
                        ledsum += int(objecttt.properties['# LEDS'])
                obj.properties["# LEDS"] = ledsum

    def update_dragdroplist(self):
        if self.selected_obj != None:
            i="Children"
            for j in self.properties:
                if i == j[3]:
                    if isinstance(j[0],DragDropListbox):
                        j[0].delete(0,END)
                        for q in self.selected_obj.properties[i]:
                            j[0].insert(END,q)
            i = "Animation"
            for j in self.properties:
                if i == j[3]:
                    if isinstance(j[0], ttk.Combobox):
                        j[0].set(self.selected_obj.properties['Animation'])
    def read_properties(self,a=1,b=1,c=1):
        if self.selected_obj != None:
            for i in self.selected_obj.properties.keys():
                for j in self.properties:
                    if i == j[3]:
                        if i == "StartStop":
                            pass
                        if i=="Color":
                            col = tuple(int(x / 15 * 255) for x in self.selected_obj.properties['Color'])
                            col = '#%02x%02x%02x' % col
                            if sum(self.selected_obj.properties['Color'])/3<6:
                                j[0].config(text=self.selected_obj.properties[i], fg = "#FFFFFF", bg = col)
                            else:
                                j[0].config(text=self.selected_obj.properties[i], fg="#000000", bg=col)
                        elif isinstance(j[0],Label):
                            j[0].config(text=self.selected_obj.properties[i])
                            if j[-1] == "Running":
                                if self.selected_obj.properties[i]=="Yes":
                                    j[0].config(font=('Arial bold', 14), fg="green")
                                else:
                                    j[0].config(font=('Arial bold', 14), fg="red")

                        if isinstance(j[0],ttk.Combobox):
                            if i == "Child_select" or i =="Animation":
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
        if self.moving ==1:
            self.c.coords(self.selected_obj.text,event.x,event.y)
            self.moving=0
            self.selected_obj.x = event.x
            self.selected_obj.y = event.y
            if self.selected_obj.type=="beunding":
                if self.selected_obj.properties['Vdev'] != "None":
                    obj = self.find_object_by_name(self.selected_obj.properties['Vdev'])
                    self.c.coords(self.selected_obj.line,self.selected_obj.x, self.selected_obj.y, obj.x, obj.y)
            self.c.unbind('<Motion>')
            self.c.pack()
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
        self.sweeping=0
        self.deselect_all()
        for obj in self.obj_list:
            if "Vdev" in obj.properties.keys() and obj.properties["Vdev"] != "None":
                pass
            else:
                #Update Vdev so that it knows its Children
                if obj.properties['type']=="vdev":
                    obj.Children_objects = []
                    for obg in obj.properties['Children']:
                        obj.Children_objects.append(self.find_object_by_name(obg))
                obj.start()

    def blank_all(self):
        self.sweeping=0
        self.deselect_all()
        for obj in self.obj_list:
            if "Vdev" in obj.properties.keys() and obj.properties["Vdev"] != "None":
                pass
            else:
                obj.previous_animation = obj.properties['Animation']
                obj.properties['Animation'] = "blank"
                #Update Vdev so that it knows its Children
                if obj.properties['type']=="vdev":
                    obj.Children_objects = []
                    for obg in obj.properties['Children']:
                        obj.Children_objects.append(self.find_object_by_name(obg))
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

    def clear_canvas(self):
        self.c.delete("all")
        self.create_grid()
        for obj in self.obj_list:
            obj.text="" #clear this, since all text is now removed and needs to be re-generated.
            obj.rect=""
            obj.line=self.c.create_line(0,0,0,0,width= 3)


            if obj.type=="beunding":
                if obj.properties['Vdev'] != "None":
                    obj2 = self.find_object_by_name(obj.properties['Vdev'])
                    self.c.coords(obj.line,obj.x, obj.y, obj2.x, obj2.y)

    def clear_objects(self):
        self.clear_canvas()
        self.obj_list=[]
    def export_yaml(self):
        f = filedialog.asksaveasfile(mode='w', defaultextension=".yaml")

        with open(f.name, 'a') as the_file:
            the_file.write('interfaces:'+'\n')
            for obj in self.obj_list:
                if obj.type=="beunding":
                    if obj.properties['Vdev'] == "None":
                        #Save here.
                        the_file.write('  -name: virt-' + str(obj.properties['Name']) + '\n')
                        the_file.write('   interface-type: virtual' + '\n')
                        the_file.write('   children: ' + '\n')
                        the_file.write('    -name: ' + str(obj.properties['Name']) + '\n')
                        the_file.write('     interface-type: physical'+'\n')
                        the_file.write('     ip: ' + str(obj.properties['IP Address'])+'\n')
                        the_file.write('     port: ' + str(obj.properties['Port'])+'\n')
                        the_file.write('     amount-leds: ' + str(obj.properties['# LEDS'])+'\n')
                        the_file.write('     max-udp-size: ' + str(obj.properties['Packet length'])+'\n')
                        the_file.write('     max-brightness: 15'+'\n')
                else:
                    the_file.write('  -name: ' + str(obj.properties['Name'])+'\n')
                    the_file.write('   interface-type: virtual'+'\n')
                    the_file.write('   children: '+'\n')
                    parent=obj
                    for obj in parent.properties['Children']:
                        obj = a.find_object_by_name(obj)
                        the_file.write('    -name: ' + str(obj.properties['Name'])+'\n')
                        the_file.write('     interface-type: physical'+'\n')
                        the_file.write('     ip: ' + str(obj.properties['IP Address'])+'\n')
                        the_file.write('     port: ' + str(obj.properties['Port'])+'\n')
                        the_file.write('     amount-leds: ' + str(obj.properties['# LEDS'])+'\n')
                        the_file.write('     max-udp-size: ' + str(obj.properties['Packet length'])+'\n')
                        the_file.write('     max-brightness: 15'+'\n')
            the_file.write('sockets: ' + str(obj.properties['Name'])+'\n')
            the_file.write('  dir: /run/syncstream'+'\n')



    def load_setup(self):
        f = filedialog.askopenfilename(defaultextension=".pkl")
        #f= "C:\\Users\\20182653\\Desktop\\TESLAN\\2023-Beun-LANCo\\SyncStream\\Multistream\\Saved setups\\Whoah.pkl"
        if f == '':
            return
        for obj in self.obj_list:
            obj.stop()
        self.clear_objects()
        file = open(f, 'rb')
        n_objects = pickle.load(file)
        for i in range(n_objects):
            obj=pickle.load(file)
            self.obj_list.append(obj)
        self.number_of_created_objects=len(self.obj_list)
        file.close()
        self.clear_canvas()

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
                    obj.properties['Animation'] = self.op4.get()
            self.op4.set("")
        else:
            messagebox.showinfo("Eyy", "Please select an animation first.")

    def blank_group(self):
        self.sweeping=0
        self.deselect_all()
        for obj in self.obj_list:
            if obj.properties['Group'] == self.op3.get():
                obj.stop()
                if "Vdev" in obj.properties.keys():
                    if obj.properties['Vdev'] == "None":
                        obj.previous_animation=obj.properties['Animation']
                        obj.properties['Animation'] = "blank"
                        obj.start()
                        obj.properties['Animation'] = obj.previous_animation
                else:
                    if obj.properties['type'] == "vdev":
                        obj.Children_objects = []
                        for obg in obj.properties['Children']:
                            obj.Children_objects.append(self.find_object_by_name(obg))
                    obj.previous_animation = obj.properties['Animation']
                    obj.properties['Animation'] = "blank"
                    obj.start()
                    obj.properties['Animation'] = obj.previous_animation
    def run_group(self):
        self.group_mode=self.op5.get()
        if self.group_mode=="instant":
            self.write_properties()
            self.deselect_all()
            for obj in self.obj_list:
                if obj.properties['Group'] == self.op3.get():
                    obj.stop()
                    if "Vdev" in obj.properties.keys():
                        if obj.properties['Vdev'] == "None":
                            obj.start()
                    else:
                        if obj.properties['type'] == "vdev":
                            obj.Children_objects = []
                            for obg in obj.properties['Children']:
                                obj.Children_objects.append(self.find_object_by_name(obg))
                        obj.start()
        else:
            self.sweeping=1
            self.sweephash=''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.sweep_treshold=0;
            #Need to do a sweep.




    #add_grid(c) #Deze doet ook pack

    # button1.pack()

    def kill_child(self):
        new_child = ""
        for i in self.properties:
            if isinstance(i[0], OptionMenu):
                if i[3] == "Child_select":
                    new_child = i[2].get()
        if not new_child == "":
            if new_child in self.selected_obj.properties['Children']:
                self.selected_obj.properties['Children'].remove(new_child)
                chld = self.find_object_by_name(new_child)
                chld.properties["Vdev"] = "None"
                self.c.coords(chld.line,0,0,0,0)
        self.read_properties()
        self.update_vdev_leds()
        self.update_dragdroplist()
    def move(self):
        self.moving=1;
        self.c.bind('<Motion>', self.callback)
        self.c.pack()
    def adopt_child(self):

        new_child = ""
        for i in self.properties:
            if isinstance(i[0],OptionMenu):
                if i[3] == "Child_select":
                    new_child = i[2].get()
        if not new_child=="":
            if not new_child in self.selected_obj.properties['Children']:
                self.selected_obj.properties['Children'].append(new_child)
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
            obj.Children_objects = []
            for obg in obj.properties['Children']:
                obj.Children_objects.append(self.find_object_by_name(obg))
        self.selected_obj.start()
    def makeform(self, dict):




        entries = []
        i=0

        for field in list(dict.keys()):
            row = Frame(self.master)
            if field != "Children":
                lab = Label(row, width=10, text=field, anchor='w')
            sv = StringVar(value=dict[field])
            #sv.trace_add('write', write_properties())
            packed=0
            if field == "Animation":
                en = DISABLED
                if 'Vdev' in dict.keys():
                    if dict['Vdev'] == "None":
                        en = "normal"
                if dict['type'] == "vdev":
                    en = "normal"
                ent = ttk.Combobox(row,width=12)
                ent.bind('<<ComboboxSelected>>', self.write_properties)
                ent.bind('<KeyRelease>', lambda event, lst=self.animations, box=ent:  self.check_input(event,lst,box))
                ent['values'] = self.animations
                ent.configure(state=en)
            elif field == "Group":
                ent = ttk.Combobox(row,width=12, state="Readonly")
                ent.bind('<<ComboboxSelected>>',self. write_properties)
                ent['values'] = self.groups
            elif field == "Running":
                ent = Label(row, width=10, text=dict[field], anchor='w')
            elif field == "Vdev" or field=="Name" or field == "Number":
                ent = Label(row, width=10, text=dict[field], anchor='w')
            elif field == "Color":
                ent = Button(row, text="Select color", command=self.choose_color)
            elif field == "Invert":
                ent = Checkbutton(row, text='Invert',variable=sv, onvalue=1, offvalue=0, command=self.write_properties)
            elif field == "Children":

                m = Frame(self.master)
                k = Frame(m)
                sv = StringVar()
                lab = Label(k, width=10, text="Children:", anchor='w')
                ent = DragDropListbox(k, width=25)
                ent.config(width=25)
                for child in self.selected_obj.properties['Children']:
                    ent.insert(END, child)
                packed = 1
                k.pack(side=TOP, fill=X, padx=2, pady=2)
                lab.pack(side=TOP, padx=10)
                ent.pack(side=TOP, padx=0)
                entries.append((ent, k, sv,field))
                k = Frame(m)
                a = [h for h in self.obj_list if h.type == "beunding"]
                e = [n.properties['Name'] for n in list(set(a))]  # - set(self.selected_obj.properties['Children']
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
            g3 = Button(f, text="◯", command=self.selected_obj.blank, bg='#be0e55', fg='white', width=4, height=1)
            g['font']=tkFont.Font(family='Arial', size=14)
            g2['font'] = tkFont.Font(family='Arial', size=14)
            g3['font'] = tkFont.Font(family='Arial', size=14)
            g.pack(side=RIGHT, padx=4)
            g2.pack(side=RIGHT, padx=4)
            g3.pack(side=RIGHT, padx=4)
            #f.pack()
            if dict['type']=="vdev":
                f.place(x=610, y=20+445)
            else:
                f.place(x=610, y=20 + 420)
            entries.append((g2, f, None, field))
            i+=1
        # Move button
        field="StartStop" #Aka ignore this
        f = Frame(self.master)
        ent = Button(f, text="✥", command=self.move, bg='#be0e55', fg='white', width=1, height=1)
        ent['font'] = tkFont.Font(family='Arial', size=14)
        ent.pack(side=LEFT, padx=2)
        entries.append((ent, f, None, field))
        ent = Button(f, text="🗑", command=self.selected_obj.delete_me, bg='#be0e55', fg='white', width=1, height=1)
        ent['font'] = tkFont.Font(family='Arial', size=14)
        ent.pack(side=LEFT, padx=2)
        entries.append((ent, f, None, field))
        f.pack()
        f.place(x=750, y=15)
        i+=1
        return entries
    #c.place(x=10, y=10)
    # load_setup()

    #master.mainloop()



if __name__ == "__main__":
    master=Tk()
    #

    #
    a=App(master)
    #master.mainloop()


    while (a.master != "stop"):
        if a.adding == 1 or a.moving==1:
            if a.temp_square == -1:
                a.rect = a.c.create_rectangle(0, 0, 0, 0)
            a.temp_square = a.c.coords(a.rect, a.tempx - 10, a.tempy - 10, a.tempx + 10, a.tempy + 10)
        else:
            if not a.temp_square == -1:
                a.c.delete(a.temp_square)
                a.c.delete(a.rect)
                a.temp_square = -1
        for obj in a.obj_list:
            if obj.deleteme==1:
                obj.deleteme=0
                if obj.type != "vdev":
                    msg_box = messagebox.askquestion('Delete object', 'Are you sure you want to delete this object?',
                                                     icon='warning')
                    if msg_box == 'yes':
                        a.deselect_all()
                        obj.stop()
                        # Remove object from all Vdevs, from selected objects
                        for obj2 in a.obj_list:
                            if obj2.type == "vdev":
                                if obj.properties['Name'] in obj2.properties['Children']:
                                    obj2.properties['Children'].remove(obj.properties['Name'])
                        if obj in a.obj_list:
                            a.obj_list.remove(obj)
                        a.clear_canvas()

                else:
                    msg_box = messagebox.askquestion('Delete object',
                                                     'Are you sure you want to delete this Vdev? Children will become orphans.',
                                                     icon='warning')
                    if msg_box == 'yes':
                        a.deselect_all()
                        obj.stop()
                        # Remove object from all Vdevs, from selected objects
                        for obg in obj.properties['Children']:
                            obj.Children_objects.append(a.find_object_by_name(obg))
                        for obj2 in obj.Children_objects:
                            obj2.properties['Vdev'] = "None"
                        if obj in a.obj_list:
                            a.obj_list.remove(obj)
                        a.clear_canvas()

            if a.sweeping==1:
                if a.group_mode=="instant":
                    a.sweeping=0;
                    print("An exception occurred")
                z=0
                q=0
                if "N" in a.group_mode:
                    z=z+obj.y
                if "S" in a.group_mode:
                    z=z-obj.y
                    q=q-400
                if "W" in a.group_mode:
                    z=z+obj.x
                if "E" in a.group_mode:
                    z=z-obj.x
                    q=q-600
                if z<a.sweep_treshold+q:
                    if not obj.sweephash == a.sweephash:
                        obj.start()
                        obj.sweephash=a.sweephash
                if a.sweep_treshold<2000:
                    a.sweep_treshold+=float(a.op6.get())


            if obj.rect == "":
                obj.rect = a.c.create_rectangle(0, 0, 0, 0)
            if obj.text == "":
                obj.text = a.c.create_text(obj.x, obj.y, text=obj.properties['Number'], fill="black",
                                              font=('Helvetica 12 bold'))
            if obj.line=="":
                obj.line= a.c.create_line(0, 0, 0, 0,width=3)
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
                        for child in obj.properties['Children']:
                            child=a.find_object_by_name(child)
                            a.c.itemconfig(child.line, fill="red")
                    else:
                        a.c.itemconfig(obj.rect, fill='#88fca3')
                        for child in obj.properties['Children']:
                            child=a.find_object_by_name(child)
                            a.c.itemconfig(child.line, fill="green")
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
            else:
                if obj.type == "beunding":
                    a.c.itemconfig(obj.rect, fill='#FFF')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
                else:
                    a.c.itemconfig(obj.rect, fill='#FFF')
                    a.c.itemconfig(obj.text, text=obj.properties['Number'])
                    if obj.properties["Running"] == "Yes":
                        for child in obj.properties['Children']:
                            child=a.find_object_by_name(child)
                            a.c.itemconfig(child.line, fill="green")
                    else:
                        for child in obj.properties['Children']:
                            child=a.find_object_by_name(child)
                            a.c.itemconfig(child.line, fill="red")
            if obj.type == "beunding":
                a.c.coords(obj.rect, obj.x - 10, obj.y - 10, obj.x + 10, obj.y + 10)
                a.c.lift(obj.rect)
                a.c.lift(obj.text)
            else:
                a.c.coords(obj.rect, obj.x - 14, obj.y - 14, obj.x + 14, obj.y + 14)
                a.c.lift(obj.rect)
                a.c.lift(obj.text)
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