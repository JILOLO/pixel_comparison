import sqlite3
from PIL import Image
import numpy as np
import time
import datetime
import os
import shutil

# 32bit PC import Image
# 64bit PC import pillow
# Python 3+ only
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import time
from statistics import mean, median

import sqlite3
from PIL import Image
import numpy as np
from collections import Counter
from matplotlib import style
style.use("ggplot")


def createExamples():
    '''
    Create a database with all hand written samples  

    Args:
        subfolder structure:
            image/numbers/
            0.1.png, 0.2.png, ...,0.9.png, 1.1.png, 1.2.png, ..., 1.9.png, ..., 9.9.png
    
    Returns:
        void
        generated an img.db with format of:
            name    TEXT
            content TEXT
    '''
    ##generate unique timestamp for db file name
    #unix = int(time.time())
    #date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H-%M-%S'))
    ##print(date)

    ##generate unique version for db
    #version = 0 

    #conn = sqlite3.connect('img' + date + '.db')
    conn = sqlite3.connect('img.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS imgTable(name TEXT, content TEXT)")


    '''
    To open each file:
    Option1: Manually create file names.
    Option2: recursively walk thru files and obtain file names.
    '''
    
    # Option1
    numbers = range(1,10)
    for eachNum in numbers:
        for furtherNum in numbers:
            fileName = str(eachNum) + '.' + str(furtherNum) 
            imgFilePath = 'images/numbers/' + fileName + '.PNG'
            ei = Image.open(imgFilePath)
            eiar = np.array(ei)
            eiarl = str(eiar.tolist())
            c.execute("INSERT INTO imgTable(name, content) VALUES(?,?)", (fileName, eiarl))
            conn.commit()
    
    '''
    # Option2
    # It didn't work well becuse of the recursive sequence doesn't follow numerical sequance
    root = 'images/numbers/'  
    for item in os.listdir(root):
        imgFilePath = os.path.join(root, item)
        ei = Image.open(imgFilePath)
        eiar = np.array(ei)
        eiarl = str(eiar.tolist())
        c.execute("INSERT INTO imgTable(name, content) VALUES(?,?)", (item, eiarl))
        conn.commit()
    '''
            
    c.close()
    conn.close()    



def threshold(imagArray):
    '''
    Adjust pixel value to filter out certain feathre as needed
    
    Args:
        an image array  

    Returns:
        adjusted images array in the same dimension
    '''
    balanceAr = []
    newAr = imagArray

    for eachRow in imagArray:
        for eachPix in eachRow:
            avgNum = mean(eachPix[:2])
            balanceAr.append(avgNum)

    balance = mean(balanceAr)
    for eachRow in newAr:
        for eachPix in eachRow:
            if mean(eachPix[:2]):
                eachPix[0] = 255
                eachPix[1] = 255
                eachPix[2] = 255
            else:
                eachPix[0] = 0
                eachPix[1] = 0
                eachPix[2] = 0
    return newAr

##test a picture
#i = Image.open('images/animals/lion.png')
#iar = np.array(i)
#iar.flags.writeable = True
#iar = threshold(iar)
#plt.imshow(iar)
#plt.show()


def whatNumIsThis(filePath):
    '''
    Go pixel by pixel, count how many identical pixel values.

    Args:
        the test file's path

    Returns:
        void
        plot test.png & probability bar chart 

    Raises:
        Exception: print str(e)

    '''

    matchdAr = []
    conn = sqlite3.connect('img.db')
    c = conn.cursor()
    c.execute('SELECT * FROM imgTable')
    loadExamps  = c.fetchall()

    i = Image.open(filePath)
    iar = np.array(i)
    iarl = iar.tolist()
    inQuestion = str(iarl)

    #print(loadExamps)
    
    for eachExample in loadExamps:
        #print(eachExample)
        try:
            currentNum = eachExample[0]
            currentAr = eachExample[1]

            x = 0
            while x < min(len(currentAr), len(inQuestion)):
                if inQuestion[x] == currentAr[x]:
                    matchdAr.append(currentNum)
                x += 1

        except Exception as e:
            print(str(e))

    #print(matchdAr)
    x = Counter(matchdAr)
    print(x)
    # x is like Counter({'a': qty1, 'b': qty,....})

    graphX = []
    graphY = []

    #ylimi = 0

    for item in x:
        graphX.append(item)
        graphY.append(x[item])
        #ylimi = [x[item]]

    fig = plt.figure()
    ax1 = plt.subplot2grid((4,4),(0,0), rowspan=1, colspan=4)
    ax2 = plt.subplot2grid((4,4),(1,0), rowspan=3, colspan=4)

    ax1.imshow(iar)
    ax2.bar(graphX, graphY, align='center')
    plt.ylim(600)

    xloc = plt.MaxNLocator(12)
    ax2.xaxis.set_major_locator(xloc)

    plt.show()


#createExamples()
whatNumIsThis('images/numbers/test.png')