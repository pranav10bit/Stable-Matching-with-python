#!/usr/bin/env python
# coding: utf-8

# In[2]:


StudentList=["S1","S2","S3","S4","S5"]  #list of students S1-S5
TeacherList=["T1","T2","T3","T4","T5"]  #list of teachers T1-T5


# In[3]:


def StudentProfile():   #function to display Student Profiles
    new=Toplevel(root)
    new.title("Student Profiles")
    Label(new,text="STUDENT PROFILES",font=("Arial",24),bg="lightblue").pack(fill=X)
    Label(new,text="").pack(fill=X)
    file=open("StudentProfile.txt","r")
    for line in file:
        if line.startswith("STUDENT"):
            Label(new,text=line,font=("Arial",10,"bold")).pack(side=TOP)
        else:
            Label(new,text=line,font=("Arial",10)).pack(side=TOP)
    Label(new,text="").pack(fill=X)
    file.close()


# In[4]:


def TeacherProfile():    #function to display Teacher Profiles
    new=Toplevel(root)
    new.title("Teacher Profiles")
    Label(new,text="TEACHER PROFILES",font=("Arial",24),bg="lightblue").pack(fill=X)
    Label(new,text="").pack(fill=X)
    file=open("TeacherProfile.txt","r")
    for line in file:
        if line.startswith("TEACHER"):
            Label(new,text=line,font=("Arial",10,"bold")).pack(side=TOP)
        else:
            Label(new,text=line,font=("Arial",10)).pack(side=TOP)
    Label(new,text="").pack(fill=X)
    file.close()


# In[5]:


TotalPreference=[]


# In[6]:


def DisplayFunction(TotalPreference):
    StudentPref=TotalPreference[0]
    TeacherPref=TotalPreference[1]
    data=StudentTeacher(StudentPref,TeacherPref)  #Student-Teacher Pairs
    data1=TeacherStudent(StudentPref,TeacherPref)   #Teacher-Student Pairs
    DisplayPairs(data,data1)  #Display pairs


# In[7]:


def InputPreference(Category,Col):  #function to input user preferences 
    Preference={}
    if Category=="Student S":
        CList=TeacherList
    else:
        CList=StudentList
    def DisplayTitle(loc,loop,ChosenList):
        if loop<=5:
            Label(new,text="Choose Preference: "+Category+str(loop),font=("Arial",10),bg="lightblue").grid(row=loc,column=Col)
            number=1
            loc=loc+1
            Preference[Category[0]+str(loop-1)]=ChosenList
            ChosenList=[]
            Display(number,loc,loop,ChosenList)
        else:
            Preference[Category[0]+"5"]=ChosenList
            if Category=="Student S":
                StudentPreference=Preference.copy()
                TotalPreference.append(StudentPreference)
                #StorePreference()
                InputPreference("Teacher T",3)  #input student preferences for each teacher
            else:
                TeacherPreference=Preference.copy()
                TotalPreference.append(TeacherPreference)
                DisplayFunction(TotalPreference) #store student/teacher preferences
                #StorePreference()
                #DisplayPairs()
    def Display(number,loc,loop,ChosenList):
        if number<=5:
            Label(new,text="Preference "+str(number)).grid(row=loc,column=Col)
            DisplayCombo(number,loc,loop,ChosenList)
        else:
            loop=loop+1
            DisplayTitle(loc,loop,ChosenList)
    def DisplayCombo(number,loc,loop,ChosenList): #print combobox
        Choices=list(set(CList)-set(ChosenList))
        cb=ttk.Combobox(new,values=Choices,state="readonly") 
        cb.bind("<<ComboboxSelected>>",lambda event:Selected(event,number,loc,loop,ChosenList))
        cb.grid(row=loc,column=Col+1)
    def Selected(event,number,loc,loop,ChosenList):  #callback function
        ChosenList.append(event.widget.get())
        number=number+1
        loc=loc+1
        Display(number,loc,loop,ChosenList)
    new=Toplevel(root)
    new.title("Preferences")
    ChosenList=[]
    number=1
    loc=1
    loop=1
    Label(new,text="Choose Preference: "+Category+str(loop),font=("Arial",10),bg="lightblue").grid(row=0,column=Col)
    Display(number,loc,loop,ChosenList) 


# In[8]:


def StudentTeacher(StudentPreference,TeacherPreference):
        # Pair students with teachers
        tempPairs={}  #dict with student(key)-teacher(value) pairs or teacher(key)-student(value) pairs
        TeachersPaired=[]  #list of teachers who have been paired
        StudentsPaired=[]  #list of students who have been paired
        while len(StudentsPaired)<len(StudentList):
            for s in StudentList:
                if s not in StudentsPaired:
                    for t in StudentPreference[s]:
                        if t not in TeachersPaired:
                            tempPairs[t]=s
                            TeachersPaired.append(t)
                            StudentsPaired.append(s)
                            break
                        else:
                            if TeacherPreference[t].index(tempPairs[t])>TeacherPreference[t].index(s):
                                StudentsPaired.remove(tempPairs[t])
                                tempPairs[t]=s
                                StudentsPaired.append(s)
                                break
        temp1=[(value,key) for key,value in tempPairs.items()]
        temp1=sorted(temp1)
        data=[("Student","Teacher")]+temp1
        return data

def TeacherStudent(StudentPreference,TeacherPreference):
        #pair teachers with students
        tempPairs={}
        TeachersPaired=[]
        StudentsPaired=[]
        while len(TeachersPaired)<len(TeacherList):
            for t in TeacherList:
                if t not in TeachersPaired:
                    for s in TeacherPreference[t]:
                        if s not in StudentsPaired:
                            tempPairs[s]=t
                            TeachersPaired.append(t)
                            StudentsPaired.append(s)
                            break
                        else:
                            if StudentPreference[s].index(tempPairs[s])>StudentPreference[s].index(t):
                                TeachersPaired.remove(tempPairs[s])
                                tempPairs[s]=t
                                TeachersPaired.append(t)
                                break
        temp1=[(value,key) for key,value in tempPairs.items()]
        temp1=sorted(temp1)
        data=[("Teacher","Student")]+temp1
        return data


# In[9]:


def DisplayPairs(data,data1):
        new=Toplevel(root)
        new.title("Pairs")
        #data=StudentTeacher()
        Label(new,text="Student-Teacher Pairs",bg="lightblue",font=('Arial',20)).grid(row=0,column=0)
        Label(new,text="").grid(row=1,column=0)
        for i in range(2,8): 
            for j in range(1,3): 
                e = Entry(new, width=20, font=('Arial',12)) 
                e.grid(row=i, column=j) 
                e.insert(END, data[i-2][j-1]) 
        Label(new,text="").grid(row=8,column=0)
        #data1=TeacherStudent()
        Label(new,text="Teacher-Student Pairs",bg="lightblue",font=('Arial',20)).grid(row=9,column=0)
        Label(new,text="").grid(row=10,column=0)
        for i in range(11,17): 
            for j in range(1,3): 
                e = Entry(new, width=20, font=('Arial',12)) 
                e.grid(row=i, column=j) 
                e.insert(END, data1[i-11][j-1])


# In[10]:


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
global StudentPreference
global TeacherPreference
StudentPreference={}
TeacherPreference={}
root = Tk()
root.title("Stable Matching")
root.geometry('500x500')
Label(root,text="Stable Matching",font=("Arial",24),bg='black',fg="white",justify="left").pack(fill=X)
Label(root,text="").pack(fill=X)
StudProf = Button(root,text="Student  Profiles",font=("Arial",12),bg="lightgrey",padx=4,pady=4,command=StudentProfile).pack()
Label(root,text="").pack(fill=X)
TeacProf = Button(root,text="Teacher  Profiles",font=("Arial",12),bg="lightgrey",padx=4,pady=4,command=TeacherProfile).pack()
Label(root,text="").pack(fill=X)
Pref = Button(root,text="Input Preferences",font=("Arial",12),bg="lightgrey",padx=4,pady=4,command=lambda:InputPreference("Student S",0)).pack()
Label(root,text="").pack(fill=X)
root.mainloop()
