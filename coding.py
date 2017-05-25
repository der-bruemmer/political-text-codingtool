from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import filedialog
import tkSimpleDialog
import csv
import os
import collections
import ntpath

root = Tk()

class CodingWindow(Frame):

    def __init__(self, master, filepath):
        root.deiconify()
        Frame.__init__(self, master)
        rater = "no_rater_name"
        filename = filepath
        self.ratingfile = filepath
        self.texts = self.readTexts(filename)
        self.cur = 0
        self.data = collections.OrderedDict()
        self.identVar = IntVar()
        self.topic = IntVar()
        self.topicNumber = IntVar()
        self.topicNumber.set(1)
        self.ratingData = collections.OrderedDict()
        
        self.grid()
        self.master = master        
        self.master.title("Text Coding")
        
        self.textField = Entry(self, width=15)
        self.textField.grid(row = 0, column = 0, sticky=W)
        if rater is None:
            rater = "no_rater_name"
        else:
            if len(rater) == 0:
                rater = "no_rater_name"
        self.textField.insert(10,rater)
        resumeButton = Button(self, text='resume',command=lambda: self.resume(),width=5)
        resumeButton.grid(row = 0, column = 1, sticky=W)
        #make this save        
        #backButton = Button(self, text='back',command=lambda: self.back())
        #backButton.grid(row = 0, column = 2, sticky=W) 

        quitButton = Button(self, text='save',command=lambda: self.printData())
        quitButton.grid(row = 0, column = 2, sticky=W)

        self.rateBox = Frame(self, height=780,width=300)
        self.rateBox.grid_propagate(True)
        self.rateBox.grid(row=1,column=5,rowspan=25,sticky=NW,padx=5)

        self.setText(True)
        if os.path.isfile("./"+rater+".csv"):
            self.resume()
        #rateButton = Button(self, text='bewerten',command=lambda: self.rateText(self.topicNumber.get()))
        #rateButton.grid(row = 4, column = 1,columnspan=3,sticky=W)

    def path_leaf(self,path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def getBaseFilename(self,filename):
        filename = self.path_leaf(filename)
        return filename[:filename.find(".")]

    def makeRatingFrame(self):
        self.resetRateBox()
        ratingLabel = Label(self.rateBox, text='Anzahl Themen im Text:',justify=LEFT)
        ratingLabel.grid(row = 0, column = 0, columnspan=2, pady=5,padx=20 , sticky = W)
        for item in [0, 1, 2, 3, 4, 5]:        
            Radiobutton(self.rateBox, text=str(item),variable=self.topicNumber,value=item).grid(row = 1+item, column = 0,columnspan=2, sticky = W)
        self.rateBox.rowconfigure(25, weight=1)
        backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(0,-1,-1,-1),width=15,pady=5)
        backButton.grid(row = 25, column = 0, sticky=SW)
        weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.updateRatingFrame(self.topicNumber.get(),self.topicNumber.get(),-1),width=15,pady=5)
        weiterButton.grid(row = 25, column = 1, sticky=SW)

    def readTexts(self, filename):
        texts = []
        with open(filename, newline='', encoding='UTF-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')
            next(reader)
            for row in reader:
                texts.append([row[0],row[1]])
        return texts

    def updateRatingFrame(self, textTopics, topicCount, topicType):
        self.resetRateBox()
        topicNo = str(textTopics-topicCount+1)
        data = self.ratingData[str(self.texts[self.cur][0])]
        #print("updateratingframe:"+topicNo)

        #setting topic value
        defaultTopic = 1
        if "topic"+topicNo in data:
            if data["topic"+topicNo] != -1:
                defaultTopic = data["topic"+topicNo]

        #persisting previous activity decision
        previousStrat = str(textTopics-topicCount)
        #print("PREVIOUS: "+str(previousStrat))
        data["topic" + previousStrat] = topicType

        self.ratingData[str(self.texts[self.cur][0])].update(data)
      #  print("saved")
      #  print(self.ratingData[str(self.texts[self.cur][0])])

        if topicCount == 0 and textTopics != 0:
            #save
            self.rateText(1)
            return
        if textTopics == 0:
            self.rateText(1)
            return
        elif textTopics > 0:
            self.topic.set(defaultTopic)
            Label(self.rateBox,text="Kategorie Thema "+topicNo).grid(row=0, column = 0,columnspan=2, sticky = W,pady=5, padx=20)
            Radiobutton(self.rateBox, text="Flüchtlinge uneindeutig",variable=self.topic,value=1).grid(row = 2, column = 0,columnspan=2,sticky = NW)
            Radiobutton(self.rateBox, text="Flüchtlinge negativ",variable=self.topic,value=2).grid(row = 3, column = 0,columnspan=2,sticky = NW)
            Radiobutton(self.rateBox, text="Flüchtlinge positiv", variable=self.topic, value=3).grid(row=4,column=0,columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="(innere) Sicherheit", variable=self.topic, value=4).grid(row=5,column=0,columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="Frieden", variable=self.topic, value=5).grid(row=6,column=0,columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="Terrorismus", variable=self.topic, value=6).grid(row=7,column=0,columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="(parteipolitische) Dysfunktionalität", variable=self.topic, value=7).grid(row=8,column=0, columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="Rechtsruck", variable=self.topic, value=8).grid(row=9,column=0,columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="Linksextremismus", variable=self.topic, value=9).grid(row=10, column=0, columnspan=2,sticky=NW)
            Radiobutton(self.rateBox, text="Umwelt", variable=self.topic, value=10).grid(row=11, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text="Wirtschaft", variable=self.topic, value=11).grid(row=12, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text="Auslandsbeziehungen", variable=self.topic, value=12).grid(row=13, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "EU", variable = self.topic, value = 13).grid(row=14, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Soziale Gerechtigkeit", variable = self.topic, value = 14).grid(row=15, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Bildung / Kinder / Familie", variable = self.topic, value = 15).grid(row=16, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Alter / Rente", variable = self.topic, value = 16).grid(row=17, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Gesundheit", variable = self.topic, value = 17).grid(row=18, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Internet und Datenschutz", variable = self.topic, value = 18).grid(row=19, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "Sonstiges", variable = self.topic, value = 19).grid(row=20, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "keine Angaben", variable = self.topic, value = 20).grid(row=21, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "zu viele Probleme", variable = self.topic, value = 21).grid(row=22, column=0, columnspan=2, sticky=NW)
            Radiobutton(self.rateBox, text = "keine Probleme", variable = self.topic, value = 22).grid(row=23, column=0, columnspan=2, sticky=NW)
            self.rateBox.rowconfigure(25, weight=1)
            backButton = Button(self.rateBox, text='zurück',command=lambda: self.back(1,self.topic.get(),textTopics, topicCount),width=15,pady=5)
            backButton.grid(row = 25, column = 0, sticky=SW)
            weiterButton = Button(self.rateBox, text='weiter',command=lambda: self.updateRatingFrame(textTopics,topicCount-1, self.topic.get()),width=15,pady=5)
            weiterButton.grid(row = 25, column = 1, sticky=SW)
    
    def resetRateBox(self):
        for widget in self.rateBox.winfo_children():
            widget.destroy()
        for i in range(0,9):
            self.rateBox.rowconfigure(i, weight=0)

    def rateText(self, value):
        data = {}
        data["ID"] = self.texts[self.cur][0]
        data["text"] = self.texts[self.cur][1]
        data["topicCount"] = self.topicNumber.get()

        self.ratingData[str(self.texts[self.cur][0])].update(data)
        #print(self.ratingData[str(data["ID"])])
 
        if self.cur+1==len(self.texts):
            showinfo('Fertig', 'Sie haben alle Texte bewertet')
            self.quit()
        else:
            self.cur += 1
        self.setText(True)
 
    def resume(self):
        ratingfilename = self.getBaseFilename(self.ratingfile)
        filename = "./"+ratingfilename+"_"+self.textField.get() + ".csv"
        fromStart = True        
        if self.cur > 0:
            fromStart = False
        if os.path.isfile(filename):
            with open(filename, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter='\t')
                next(reader, None)
                for row in reader:
                    data = {"ID":row[0],"text":row[1],"topicCount":int(row[2]),
                    "topic1":int(row[3]),
                    "topic2":int(row[4]),
                    "topic3":int(row[5]),
                    "topic4":int(row[6]),
                    "topic5":int(row[7]),}
                    self.ratingData[row[0]] = data
                    if fromStart:
                        self.cur += 1
            #check if it is the last text
            if self.cur == len(self.texts):
                showinfo('Fertig', 'Sie haben alle Texte bewertet')
                self.quit()
            else:
                self.setText(True)

    def printData(self):
        #ratingfilename = self.ratingfile[self.ratingfile.find(os.path.sep):]
        ratingfilename = self.getBaseFilename(self.ratingfile)
        filename = "./"+ratingfilename+"_"+self.textField.get() + ".csv"
        if len(self.ratingData)>0:
            with open(filename, 'w', newline='') as csvfile:
                datawriter = csv.writer(csvfile, delimiter='\t',quotechar='"',quoting=csv.QUOTE_NONNUMERIC,)
                datawriter.writerow(["ID","text","topicCount",
                    "topic1",
                    "topic2",
                    "topic3",
                    "topic4",
                    "topic5"])
               # print(self.ratingData)
                for key in self.ratingData:
                    data = self.ratingData[key]
                    #only print complete lines
                    if "topic1" in data and "topic2" in data and "topic3" in data and "topic4" in data and "topic5" in data and "topicCount" in data and "ID" in data:
                        #print("Writing:"+str(data))
                        datawriter.writerow([data["ID"],data["text"],
                                    data["topicCount"],
                                    data["topic1"],
                                    data["topic2"],
                                    data["topic3"],
                                    data["topic4"],
                                    data["topic5"],])

    def quit(self):
        self.printData()
        root.quit()

    #add previous data to buttons and fields
    def back(self, status, topic, textTopics, topicCount):
        #print(textTopics)
        data = self.ratingData[str(self.texts[self.cur][0])]
        currentTopic = textTopics - topicCount +1
        #print(status)
        #setting former activity rating
        topic = self.topic
        if "topic"+str(currentTopic-1) in data:
            if data["topic"+str(currentTopic-1)] != -1:
                topic = data["topic"+str(currentTopic-1)]

        #initial decision, no of topics
        #back: go back to last decision
        if status == 0:
            if self.cur > 0:
                self.cur-=1
                self.setText(False)
        #decision about specific topic
        #back: go to previous topic rating
        elif status == 1:
            #print("status"+str(status))
            if currentTopic > 1:
                self.updateRatingFrame(textTopics,topicCount+1,topic)
            else:
                self.setText(True)
                

    def setText(self,fromScratch):
        if fromScratch:
            self.makeRatingFrame()
        self.topicNumber.set(1)
        self.identVar.set(0)
        textlabel = Text(self, font = "Helvetica 14",wrap=WORD,height=28,width=30)
        textlabel.insert(END,self.texts[self.cur][1])
        textlabel.config(state=DISABLED)
        textlabel.grid(row=2, column=0, columnspan = 4, sticky = W)
       # textPosition = 'Text: '+str(self.texts[self.cur][0]+" von "+str(len(self.texts)))
        textPosition = 'Text: '+str(self.cur+1)+" von "+str(len(self.texts))
        textNumber = Label(self, text=textPosition, justify=LEFT)
        textNumber.grid(row = 1, column = 0, sticky=W)
        
        #key is known, data exists
        if str(self.texts[self.cur][0]) in self.ratingData:
            data = self.ratingData[str(self.texts[self.cur][0])]
            if len(data) == 12:
                self.topicNumber.set(data["topicCount"])
                if self.topicNumber.get() > 0:
                    self.topic.set(data["topic"+str(self.topicNumber.get())])
                if not fromScratch:
                    if self.topicNumber.get() == 0:
                        self.updateRatingFrame(self.topicNumber.get(),self.topicNumber.get(),-1)
                    else:
                        print(self.topicNumber.get())
            else:
                self.ratingData[str(self.texts[self.cur][0])] = {}
                data = {}
                for i in range(1,6):
                        data["topic"+str(i)]=-1
                self.ratingData[str(self.texts[self.cur][0])].update(data)
           # print("settext:")
           # print(data)
        else:
            self.ratingData[str(self.texts[self.cur][0])] = {}
            data = {}
            for i in range(1,6):
                    data["topic"+str(i)]=-1
            self.ratingData[str(self.texts[self.cur][0])].update(data)

    def onExit(self):
        self.quit()
 
def main():
    root.withdraw()
    file_path = filedialog.askopenfilename()
    ex = CodingWindow(root, file_path)
    root.protocol("WM_DELETE_WINDOW", ex.onExit)      
    root.mainloop() 


if __name__ == '__main__':
    main()  
