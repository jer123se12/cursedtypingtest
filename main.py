import curses
from curses import wrapper
import time
import string

def main(stdscr):
    RED=chr(1)+chr(1)
    GREEN=chr(1)+chr(2)
    BLUE=chr(1)+chr(3)
    WHITE=chr(1)+chr(4)
    def parser(screen,initial,tet):
        '''
        color: chr(1)+chr(colorpair) + text
        cursor: chr(2)
        '''
        maxxy=stdscr.getmaxyx()
        if tet=="":
            return
        i=0
        curi=0
        color=curses.color_pair(2)
        cur=1
        while i<len(tet):
            if tet[i]==chr(1):
                color=curses.color_pair(ord(tet[i+1]))
                stdscr.addstr(
                                initial[1]+(curi//(maxxy[1]-initial[0])),
                                initial[0]+(curi%(maxxy[1]-initial[0])),
                                tet[i+2],
                                color
                                )
                i+=3
                curi+=1
            elif tet[i]==chr(2):
                if cur==1:
                    cur=0
                    color+=curses.A_UNDERLINE
                else:
                    cur=1
                    color-=curses.A_UNDERLINE
                
                i+=1
            elif tet[i]==chr(10):
                curi=((curi//(maxxy[1]-initial[0]))+1)*(maxxy[1]-initial[0])
                i+=1
            else:
                stdscr.addstr(
                                initial[1]+(curi//(maxxy[1]-initial[0])),
                                initial[0]+(curi%(maxxy[1]-initial[0])),
                                tet[i],
                                color
                                )
                i+=1
                curi+=1
        pass
    def update(current,text):
        texttobedisplaced=[]
        for wordindex in range(len(current)-1):
            if current[wordindex]!=text[wordindex]:
                word=''
                if len(current[wordindex])>=len(text[wordindex]):
                    for i in range(len(current[wordindex])):
                        if i < len(text[wordindex]):
                            if current[wordindex][i] != text[wordindex][i]:
                                word +=RED+text[wordindex][i]#wrong
                            else:
                                word +=GREEN+text[wordindex][i]
                        else:
                            word +=RED+current[wordindex][i]#wrong
                else:
                    for i in range(len(text[wordindex])):
                        if i < len(current[wordindex]):
                            if current[wordindex][i] != text[wordindex][i]:
                                word +=RED+text[wordindex][i]#wrong
                            else:
                                word +=GREEN+text[wordindex][i]
                        else:
                            word+=WHITE+text[wordindex][i]
                texttobedisplaced.append(word)
            else:
                texttobedisplaced.append(GREEN+text[wordindex])
        if len(current)>0:
            last=len(current)-1
            if current[last]!=text[last]:
                word=''
                if len(current[last])>len(text[last]):
                    for i in range(len(current[last])):
                        if i < len(text[last]):
                            if current[last][i] != text[last][i]:
                                word +=RED+text[last][i]#wrong
                            else:
                                word +=GREEN+text[last][i]
                        else:
                            word +=RED+current[last][i]#wrong
                else:
                    for i in range(len(text[last])):
                        if i < len(current[last]):
                            if current[last][i] != text[last][i]:
                                word +=RED+text[last][i]#wrong
                            else:
                                word +=GREEN+text[last][i]
                        else:
                            word+=BLUE+text[last][i]
                texttobedisplaced.append(word)
            else:
                texttobedisplaced.append(GREEN+text[last])
        texttobedisplaced+=[BLUE+text[len(current)]]+text[len(current)+1:] if len(current)<len(text) else []
        return texttobedisplaced
    
    
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    current=[""]
    k=0
    text=""
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    
    
    
    strs=string.ascii_letters+string.digits+string.punctuation+string.whitespace
    with open("text.txt") as t:
        text=t.read().replace("\n","").split(" ")
    while True:
        prec=str(current)
        if k!=0:
            if k in [curses.KEY_BACKSPACE, ord('\b'),ord('\x7f')]:
                if len(current[-1])>0:
                    current[-1]=current[-1][:-1]
                else:
                    current=current[:-1] if len(current)>1 else current
                
            else:
                if chr(k) in strs:
                    if k==ord(" "):
                        current.append("")
                        if len(current)> len(text):
                            #end handleling here
                            exit()
                    else:
                        current[-1]+=chr(k)
        
        if prec!=current:
            tex=update(current,text)
            stdscr.clear()
            parser(stdscr,[0,0]," ".join(tex))
        stdscr.refresh()
                
                
            
        
        
        k=stdscr.getch()
        

wrapper(main)
