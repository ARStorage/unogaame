from tkinter import *
from ctypes import *
"""
-1 : 종료 exit(-1)
0 : 메인메뉴 MainMenu()
1 : 로그인 Login()
2 : 회원가입 Join()
3 : 게임시작화면 StartMenu()
4 : 게임 시작 GamePlay()
5 : 게임설명 GameExplain()
6 : 게임옵션설정 GameOption()

"""

global WINDOW
WINDOW  = 0

global playername
global playerid
global playerlose
global playerwin

#프레임 만들기
def makeFrame(framename,w,h,px,py,bgcolor,r,s,f):
    framename.configure(width = w, height = h)
    framename.configure(padx = px,pady = py)
    framename.configure(bg = bgcolor)
    framename.configure(relief = r)
    framename.pack(side = s,fill = f, expand = True)

#버튼 만들기
def makeButton(buttonname,bgcolor,w,h,hgcolor,fontsize,r,c):
    buttonname.configure(bg = bgcolor)
    buttonname.configure(width = w,height = h)
    buttonname.configure(fg = hgcolor)
    buttonname.configure(font = ("맑은 고딕",fontsize))
    buttonname.grid(row = r, column = c)

#라벨 만들기
def makeLabel(labelname,bgcolor,fontsize,r,c):
    labelname.configure(bg = bgcolor)
    labelname.configure(font = ("맑은 고딕",fontsize))
    labelname.grid(row = r,column = c)

#**************************************************************************시작메뉴 UI***********************
def STARTMENU():
    def outClick():
        print("종료 버튼 누름")
        global WINDOW
        WINDOW  = -1
        GAMEMENU.destroy()

    def startClick():
        print("시작 버튼 누름")
        global WINDOW
        WINDOW = 4
        GAMEMENU.destroy()

    def explainClick():
        print("설명 버튼 누름")
        global WINDOW
        WINDOW = 5
        GAMEMENU.destroy()

    def setoptionClick():
        print("옵션 설정 버튼 누름")

    GAMEMENU = Tk()
    GAMEMENU.configure(bg = "white")
    GAMEMENU.title("게임 메뉴")

    logoframe = Frame(GAMEMENU)
    makeFrame(logoframe,500,100,160,50,"white","solid","top","both")
    logoimage = PhotoImage(file = "uonologo.gif")
    logo = Label(GAMEMENU, image = logoimage)
    logo.configure(bd = 0)
    logo.pack()

    buttonframe = Frame(GAMEMENU)
    makeFrame(buttonframe,500,100,160,50,"white","solid","top","both")

    outbuttonframe = Frame(GAMEMENU)
    makeFrame(outbuttonframe,250,50,10,10,"white","solid","left","both")

    start = Button(buttonframe,text = "게임 시작",command = startClick)
    makeButton(start,'#4f87e3',30,2,"white",10,0,0)

    explain = Button(buttonframe,text = "게임 설명",command = explainClick)
    makeButton(explain,'#4f87e3',30,2,"white",10,1,0)

    setoption = Button(buttonframe,text = "게임 설정",command = setoptionClick)
    makeButton(setoption,'#4f87e3',30,2,"white",10,2,0)

    outbutton = Button(outbuttonframe,text = "종료", command = outClick)
    makeButton(outbutton,'#4f87e3',10,0,"white",10,0,0,)

    GAMEMENU.mainloop()



#**************************************************************************로그인 UI***********************
def LOGINMENU():
    def loginOkClick():
        print("로그인 확인 버튼 누름")
        
        loginlib = cdll.LoadLibrary('loginC.dll')
        login = loginlib['logIn']
        login.argtypes = (c_wchar_p,c_wchar_p,c_wchar_p,POINTER(c_int),POINTER(c_int),)
        login.restypes = c_int#로그인 여부 -1 return시 로그인 실패, 1 return시 로그인 성공
        
        idinput = idvalue.get()
        password = passwordvalue.get()
        idinput = c_wchar_p(idinput)#c타입으로 문자열 변환
        password = c_wchar_p(password)#c타입으로 문자열 변환
        
        name ="None"#이름을 반환받을 문자열
        name = c_wchar_p(name)#c타입 문자열 변환
        
        win = 0#반환받을 승 횟수 정보
        win = c_int(win)#c타입 정수형 변환
        lose = 0#반환받을 패 횟수 정보
        lose = c_int(lose)#c타입 정수형 변환

        check = login(idinput,password,name,win,lose)#로그인
        CDLL('loginC.dll')#연결 종료
            
        #반환받은 정보 다시 유니코드로 변환
        name = name.value
        win = win.value
        lose = lose.value
        if(check==1):
            print("로그인 완료")
            global playername
            global playerid
            global playerlose
            global playerwin
            playername = name
            playerid = idinput.value
            playerwin = win
            playerlose = lose
            global WINDOW
            WINDOW = 3
            LOGIN.destroy()

            
        elif(check==-1):
            print("로그인 실패")
        else:
            print("오류")

    def loginOutClick():
        print("종료 버튼 누름")
        global WINDOW
        WINDOW = -1
        LOGIN.destroy()#종료
        
    LOGIN = Tk()
    LOGIN.configure(bg = "white")
    LOGIN.title("로그인")

    stateframe = Frame(LOGIN)
    makeFrame(stateframe,500,50,50,20,"white","solid","top","both")

    idframe = Frame(LOGIN)
    makeFrame(idframe,500,50,50,20,"white","solid","top","both")

    passwordframe = Frame(LOGIN)
    makeFrame(passwordframe,500,50,50,20,"white","solid","top","both")

    okbuttonframe = Frame(LOGIN)
    makeFrame(okbuttonframe,250,50,10,10,"white","solid","right","both")

    outbuttonframe = Frame(LOGIN)
    makeFrame(outbuttonframe,250,50,10,10,"white","solid","left","both")

    statelabel = Label(stateframe,text = "아이디와 비밀번호를 입력하세요.")
    makeLabel(statelabel,"white",10,0,0)

    idlabel = Label(idframe,text = "ID ")
    makeLabel(idlabel,"white",10,0,0)

    idvalue = StringVar()
    identry = Entry(idframe,textvariable = idvalue).grid(row = 0,column = 1)

    passwordlabel = Label(passwordframe,text = "PW")
    makeLabel(passwordlabel,"white",10,0,0)

    passwordvalue = StringVar()
    passwordentry = Entry(passwordframe,textvariable = passwordvalue,show="*").grid(row = 0,column = 1)

    okbutton = Button(okbuttonframe,text = "확인", command = loginOkClick)
    makeButton(okbutton,'#4f87e3',10,0,"white",10,0,0,)

    outbutton = Button(outbuttonframe,text = "종료", command = loginOutClick)
    makeButton(outbutton,'#4f87e3',10,0,"white",10,0,0,)

    LOGIN.mainloop()


#**************************************************************************설명 UI***********************

def EXPLAIN():
    GAMEEXPLAIN = Tk()
    GAMEEXPLAIN.configure(bg = "white")
    GAMEEXPLAIN.title("게임 설명")
    global n
    n = 0

    def okExplain():
        print("확인 버튼 누름")
        global WINDOW
        WINDOW = 3
        GAMEEXPLAIN.destroy()

    def nextClick():
        print("다음 버튼 누름")
        global n
        n = n+1
        mylist = explainframe.grid_slaves()
        for k in mylist:
            k.destroy()
        explain = ['game1.gif','game2.gif','game3.gif','game4.gif']
        explainimage = PhotoImage(file = explain[n])
        explain = Label(explainframe, image = explainimage)
        explain.configure(bd = 0)
        explain.grid()

    explainframe = Frame(GAMEEXPLAIN)
    makeFrame(explainframe,500,100,160,50,"white","solid","top","both")
    controlframe = Frame(GAMEEXPLAIN)
    makeFrame(controlframe,500,100,160,50,"white","solid","bottom","both")
    explain = ['game1.gif','game2.gif','game3.gif','game4.gif']
    explainimage = PhotoImage(file = explain[0])
    explain = Label(explainframe, image = explainimage)
    explain.configure(bd = 0)
    explain.grid()

    okeplainbutton = Button(controlframe,text = "확인", command = okExplain)
    makeButton(okeplainbutton,'#4f87e3',10,0,"white",10,0,0)

    nextplainbutton = Button(controlframe,text = "다음", command = nextClick)
    makeButton(nextplainbutton,'#4f87e3',10,0,"white",10,0,1)
    
    GAMEEXPLAIN.mainloop()
    
#**************************************************************************결과 UI***********************
    
def RESULTSHOW(result):
    RESULT = Tk()
    RESULT.configure(bg = '#c4dadb')
    RESULT.title("결과 화면")

    global playername
    global playerlose
    global playerwin

    def outClick():
        global WINDOW
        WINDOW  = -1
        RESULT.destroy()
        
    def restartClick():
        global WINDOW
        WINDOW  = 4
        RESULT.destroy()
        
    showframe = Frame(RESULT)
    makeFrame(showframe,500,100,160,5,'#c4dadb',"solid","top","both")

    buttonframe = Frame(RESULT)
    makeFrame(buttonframe,500,100,160,5,'#c4dadb',"solid","top","both")

    if (result==-1):
        string = "컴퓨터가 이겼습니다."
        playerlose = playerlose+1
    else:
        string = playername+" 플레이어가 이겼습니다."
        playerwin = playerwin+1

    SAVEDATA(playerwin,playerlose)
    
    statelabel = Label(showframe,text = string)
    makeLabel(statelabel,"white",25,1,1)
    statelabel.configure(width = 30)

    accruestring = "승 : "+str(playerwin)+"  패 : "+str(playerlose)
    perlabel = Label(buttonframe,text = accruestring)
    makeLabel(perlabel,'#c4dadb',10,0,1)
    perlabel.configure(width = 50)

    outbutton = Button(buttonframe,text = "종료",command = outClick)
    makeButton(outbutton,'#488cb0',10,0,"white",10,1,0)

    restartbutton = Button(buttonframe,text = "다시 시작",command = restartClick)
    makeButton(restartbutton,'#488cb0',10,0,"white",10,1,2)
    
#**************************************************************************게임 UI***********************
def GAMEPLAY():
    gamelib = cdll.LoadLibrary('gameC.dll')

    GAME = Tk()
    GAME.configure(bg = '#c4dadb')
    GAME.title("UNO 게임")

    upperframe = Frame(GAME)
    statelabel = Label(upperframe,text = "게임 시작합니다.")

    #카드 버튼 초기화
    buttonlist = []
    buttonvalue = []
    buttonlist2 = []
    buttonvalue2 = []
    for i in range(80):
        buttonlist.append(0)
        buttonvalue.append(0)
        buttonlist2.append(0)
        buttonvalue2.append(0)

    #플레이어가 가진 카드
    playercardindex = []
    playercardcolor = []
    playercardcategory = []
    playertop = 0#남은 카드 개수

    pci = (c_int*108)(*playercardindex)#c에서 연산가능한 배열로 변환
    pcc = (c_int*108)(*playercardcolor)
    pct = (c_int*108)(*playercardcategory)
    playertop = (c_int)(playertop)

    playercard = [pci,pcc,pct]

    #컴퓨터가 가진 카드
    comcardindex = []
    comcardcolor = []
    comcardcategory = []
    comtop = 0#남은 카드 개수

    cci = (c_int*108)(*comcardindex)#c에서 연산가능한 배열로 변환
    ccc = (c_int*108)(*comcardcolor)
    cct = (c_int*108)(*comcardcategory)
    comtop = (c_int)(comtop)
    comcard = [cci,ccc,cct]

    #카드 스택
    stackcardindex = []
    stackcardcolor = []
    stackcardcategory = []
    stacktop = 0#남은 카드 개수

    si = (c_int*108)(*stackcardindex)#c에서 연산가능한 배열로 변환
    sc = (c_int*108)(*stackcardcolor)
    st = (c_int*108)(*stackcardcategory)
    stacktop = (c_int)(stacktop)
    stackcard = [si,sc,st]

    #가장 최근에 제출한 카드
    topcardindex = -1
    topcardcolor = -1
    topcardcategory = -1

    topcardindex = (c_int)(topcardindex)
    topcardcolor = (c_int)(topcardcolor)
    topcardcategory = (c_int)(topcardcategory)
    topcardtop =(c_int)(1)

    #순서
    turn = 0
    turn = (c_int)(turn)

    #선택카드
    cardselection = 0
    cardselection = (c_int)(cardselection)

    control = gamelib['gameControl']
    control.argtypes = (POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int))
    control.restypes = (c_int,)

    reset = gamelib['gameReset']
    reset.argtypes = (POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),POINTER(c_int),POINTER(c_int),POINTER(c_int),
                       POINTER(c_int),)
    reset.restypes = (c_int,)

    def change_label(labelname,changestr):
        labelname.configure(text = changestr)
        
    #카드 배치
    def setCard():
        complayerlabel = Label(computerframe,text = "컴퓨터 플레이어")
        makeLabel(complayerlabel,'#c4dadb',10,0,0)
        
        playerlabel = Label(playerframe,text = "플레이어")
        makeLabel(playerlabel,'#c4dadb',10,0,0)

        cardfunc = ""
        cardcolor = ""
                
        #맨위 카드 보이기
        if(topcardcategory.value>=0 and topcardcategory.value<=9):
            cardfunc = topcardcategory.value
        elif(topcardcategory.value==10):
            cardfunc = "skip"
        elif (topcardcategory.value==11):
            cardfunc = "reverse"
        elif (topcardcategory.value==12):
            cardfunc = "draw two"
        elif (topcardcategory.value==13):
            cardfunc = "wild"
        elif (topcardcategory.value==14):
            cardfunc = "wile\ndraw\nfour"
        else:
            print("오류")

        if(topcardcolor.value==0):#red
            cardcolor = '#fa5656'
        elif(topcardcolor.value==1):#orange
            cardcolor = '#ff9562'
        elif(topcardcolor.value==2):#yellow
            cardcolor = '#fed558'
        elif(topcardcolor.value==3):#green
            cardcolor = '#b9d073'
        elif(topcardcolor.value==4):#black
            cardcolor = '#464646'
        else:
            print("오류")
                    
        cardbutton = Button(gamebuttonframe,text = cardfunc, command = clickButton)
        makeButton(cardbutton,cardcolor,10,5,"white",10,0,2)

        x = 1
        y = 0
        #컴퓨터 카드 보이기
        for i in range(comtop.value):
            Card(buttonlist[i],computerframe," ",'#bbe8fd',x,y,i)
            y = y+1
            if(i%8==0 and i!=0):
                x = x+1
                y = 0

        cardfunc = ""
        cardcolor = ""
        x = 1
        y = 0
        #플레이어 카드 보이기
        for i in range(playertop.value):
            if(pct[i]>=0 and pct[i]<=9):
                cardfunc = pct[i]#숫자카드
            elif(pct[i]==10):
                cardfunc = "skip"
            elif (pct[i]==11):
                cardfunc = "reverse"
            elif (pct[i]==12):
                cardfunc = "draw two"
            elif (pct[i]==13):
                cardfunc = "wild"
            elif (pct[i]==14):
                cardfunc = "wild\ndraw\nfour"
            else:
                print("오류")

            if(pcc[i]==0):#red
                cardcolor = '#fa5656'
            elif(pcc[i]==1):#orange
                cardcolor = '#ff9562'
            elif(pcc[i]==2):#yellow
                cardcolor = '#fed558'
            elif(pcc[i]==3):#green
                cardcolor = '#b9d073'
            elif(pcc[i]==4):#black
                cardcolor = '#464646'
            else:
                print("오류")
            Card2(buttonlist2[i],playerframe,cardfunc,cardcolor,x,y,i)
            y = y+1
            if(i%8==0 and i!=0):
                x = x+1
                y = 0

        if(turn.value==0):
                #print("컴퓨터 차례")
                change_label(statelabel,"컴퓨터 차례입니다.")
        else:
                #print("플레이어 차례")
                change_label(statelabel,"버튼을 누르세요.")
                    

    def resultexit(outcome):
        if(outcome==-1):
            change_label(statelabel,"컴퓨터 승입니다.")
            RESULTSHOW(-1)
            GAME.destroy()
            #결과창 띄우기
        elif(outcome==-2):
            change_label(statelabel,"플레이어 승입니다.")
            RESULTSHOW(-2)
            GAME.destroy()
            #결과창 띄우기
        
        
    class Card():#컴퓨터 카드
        def __init__(self,name,frame,texts,color,x,y,i):
            self.name = Button(frame,command = self.click)
            self.name["text"] = texts
            self.name.configure(bg = color)
            self.name.configure(width = 10,height = 5)
            self.name.configure(fg ="white")
            self.name.configure(font = ("맑은 고딕",10))
            self.name.grid(row = x, column = y)
            buttonvalue[i] = self.name

        def click(self):
            print("잘못된 버튼 클릭")
            
    class Card2():
        def __init__(self,name,frame,texts,color,x,y,i):
            self.name = Button(frame,command = self.click)
            self.name["text"] = texts
            self.name.configure(bg = color)
            self.name.configure(width = 10,height = 5)
            self.name.configure(fg ="white")
            self.name.configure(font = ("맑은 고딕",10))
            self.name.grid(row = x, column = y)
            buttonvalue2[i] = self.name

        def click(self):
            global clickedbutton
            clickedbutton = buttonvalue2.index(self.name)#플레이어가 클릭한 버튼
            print(clickedbutton)
            cardselection2 = clickedbutton
            cardselection = (c_int)(cardselection2)#cint형으로 변환
            result = control(topcardindex,topcardcolor,topcardcategory,
                                 si,sc,st,stacktop,
                                 pci,pcc,pct,playertop,
                                 cci,ccc,cct,comtop,
                                 turn,cardselection)#결과
            mylist = playerframe.grid_slaves()#카드 재설정
            for i in mylist:
                i.destroy()
            mylist = computerframe.grid_slaves()
            for i in mylist:
                i.destroy()
                
            resultexit(result)#결과 확인

            #컴퓨터 연산
            if(turn.value==0):#컴퓨터 차례이면
                result = control(topcardindex,topcardcolor,topcardcategory,
                                 si,sc,st,stacktop,
                                 pci,pcc,pct,playertop,
                                 cci,ccc,cct,comtop,
                                 turn,cardselection)
                mylist = playerframe.grid_slaves()
                for i in mylist:
                    i.destroy()
                mylist = computerframe.grid_slaves()
                for i in mylist:
                    i.destroy()
                resultexit(result)#결과 확인
                
            setCard()#카드 보이기
            
    def clickButton():
        print("button 클릭함")

    def outClick():
        print("종료 버튼 누름")
        global WINDOW
        WINDOW  = -1
        GAME.destroy()

    def clicktake():
        print("카드 가져가기 선택")
        cardselection2 = -1
        cardselection = (c_int)(cardselection2)
        result = control(topcardindex,topcardcolor,topcardcategory,
                         si,sc,st,stacktop,
                         pci,pcc,pct,playertop,
                         cci,ccc,cct,comtop,
                         turn,cardselection)
        mylist = playerframe.grid_slaves()
        for i in mylist:
            i.destroy()
        
        #컴퓨터 연산
        if(turn.value==0):#컴퓨터 차례이면
            result = control(topcardindex,topcardcolor,topcardcategory,
                             si,sc,st,stacktop,
                             pci,pcc,pct,playertop,
                             cci,ccc,cct,comtop,
                             turn,cardselection)
            mylist = playerframe.grid_slaves()
            for i in mylist:
                i.destroy()
            mylist = computerframe.grid_slaves()
            for i in mylist:
                i.destroy()
            resultexit(result)#결과 확인
        setCard()
        
    def clickUno():
        print("우노!")
        cardselection2 = -2
        cardselection = (c_int)(cardselection2)
        result = control(topcardindex,topcardcolor,topcardcategory,
                         si,sc,st,stacktop,
                         pci,pcc,pct,playertop,
                         cci,ccc,cct,comtop,
                         turn,cardselection)
        if(turn.value ==0):
            mylist = computerframe.grid_slaves()
            for i in mylist:
                i.destroy()
        else:
            mylist = playerframe.grid_slaves()
            for i in mylist:
                i.destroy()
        setCard()
    makeFrame(upperframe,50,100,160,5,'#c4dadb',"solid","top","both")

    computerframe = Frame(GAME)
    makeFrame(computerframe,500,100,160,5,'#c4dadb',"solid","top","both")

    gamebuttonframe = Frame(GAME)
    makeFrame(gamebuttonframe,500,100,160,5,'#c4dadb',"solid","top","both")

    playerframe = Frame(GAME)
    makeFrame(playerframe,500,100,160,5,'#c4dadb',"solid","bottom","both")
    global playername
    global playerlose
    global playerwin
    stringp = playername+"  승 : "+str(playerwin)+"  패 :"+str(playerlose)
    pointlabel = Label(upperframe,text = stringp)
    makeLabel(pointlabel,'#c4dadb',10,0,0)

    makeLabel(statelabel,"white",15,1,1)
    statelabel.configure(width = 50)

    outbutton = Button(upperframe,text = "종료", command = outClick)
    makeButton(outbutton,'#488cb0',10,0,"white",10,0,2)

    cardbutton = Button(computerframe,text = "", command = clickButton)
    makeButton(cardbutton,'#d5aaff',10,5,"white",10,1,0)


    stackbutton = Button(gamebuttonframe,text = "카드\n가져가기", command = clicktake)
    makeButton(stackbutton,'#488cb0',10,5,"white",10,0,0)

    unobutton = Button(gamebuttonframe,text = "UNO!", command = clickUno)
    makeButton(unobutton,'#488cb0',10,5,"white",10,0,1)



    #게임 초기화
    result = reset(topcardindex,topcardcolor,topcardcategory,
                         si,sc,st,stacktop,
                         pci,pcc,pct,playertop,
                         cci,ccc,cct,comtop,
                         turn)
    #첫 연산
    cardselection2 = 0
    cardselection = (c_int)(cardselection2)
    result = control(topcardindex,topcardcolor,topcardcategory,
                     si,sc,st,stacktop,
                     pci,pcc,pct,playertop,
                     cci,ccc,cct,comtop,
                     turn,cardselection)
    setCard()#카드 보이기
    GAME.mainloop()

def MAINMENU():
    def loginClick():
        print("로그인 버튼 누름")
        global WINDOW
        WINDOW = 1
        MAIN.destroy()
        
    def joinClick():
        print("회원가입 버튼 누름")
        global WINDOW
        WINDOW = 2
        MAIN.destroy()
        
    def outClick():
        print("종료 버튼 누름")
        global WINDOW
        WINDOW = -1
        MAIN.destroy()

    MAIN = Tk()
    MAIN.configure(bg = 'white')
    MAIN.title("우노!UNO!")

    logoframe = Frame(MAIN)
    logoframe.configure(width = 500, height = 100)
    logoframe.configure(padx = 160,pady = 50)
    logoframe.configure(bg = "white")
    logoframe.configure(relief = "solid")
    logoframe.pack(side = "top",fill = "both", expand = True)

    logoimage = PhotoImage(file = "uonologo.gif")
    logo = Label(MAIN, image = logoimage)
    logo.configure(bd = 0)
    logo.pack()
    
    buttonframe = Frame(MAIN)
    buttonframe.configure(width = 500, height = 100)
    buttonframe.configure(padx = 160,pady = 50)
    buttonframe.configure(bg = "white")
    buttonframe.pack(side = "bottom",fill = "both", expand = True)

    login = Button(buttonframe,text = "로그인",command = loginClick)
    login.configure(bg = '#4f87e3')
    login.configure(width = 30,height = 2)
    login.configure(fg = "white")
    login.configure(font = ("맑은 고딕",10))
    login.grid(row = 0, column = 0)

    join = Button(buttonframe,text = "회원가입",command = joinClick)
    join.configure(bg = '#4f87e3')
    join.configure(width = 30,height = 2)
    join.configure(fg = "white")
    join.configure(font = ("맑은 고딕",10))
    join.grid(row = 1, column = 0)

    out = Button(buttonframe,text = "종료",command = outClick)
    out.configure(bg = '#4f87e3')
    out.configure(width = 30,height = 2)
    out.configure(fg = "white")
    out.configure(font = ("맑은 고딕",10))
    out.grid(row = 2, column = 0)

    MAIN.mainloop()

def JOINMEMU():
    def joinOkClick():
        print("로그인 확인 버튼 누름")
        joinlib = cdll.LoadLibrary('joinC.dll')
        
        idinput = idvalue.get()
        name = namevalue.get()
        password = passwordvalue.get()
        password2 = password2value.get()

        name = c_wchar_p(name)
        idinput = c_wchar_p(idinput)
        password = c_wchar_p(password)
        password2 = c_wchar_p(password2)

        check = joinlib.join(idinput,password,password2,name)
        CDLL('joinC.dll')
        if(check==0):
            print("id 중복")
        elif(check==1):
            print("비밀번호 틀림")
        elif(check==2):
            print("회원가입 완료")
            global WINDOW
            WINDOW  = 0
            JOIN.destroy()
        else:
            print("오류")


    def backClick():
        print("뒤로 버튼 누름")
        global WINDOW
        WINDOW  = 0
        JOIN.destroy()
        
    JOIN = Tk()
    JOIN.configure(bg = "white")
    JOIN.title("회원가입")

    idframe = Frame(JOIN)
    makeFrame(idframe,500,50,50,20,"white","solid","top","both")

    passwordframe = Frame(JOIN)
    makeFrame(passwordframe,500,50,50,20,"white","solid","top","both")

    password2frame = Frame(JOIN)
    makeFrame(password2frame,500,50,50,20,"white","solid","top","both")

    nameframe = Frame(JOIN)
    makeFrame(nameframe,500,50,50,20,"white","solid","top","both")

    okbuttonframe = Frame(JOIN)
    makeFrame(okbuttonframe,250,50,10,10,"white","solid","right","both")

    backbuttonframe = Frame(JOIN)
    makeFrame(backbuttonframe,250,50,10,10,"white","solid","left","both")

    idlabel = Label(idframe,text = "ID ")
    makeLabel(idlabel,"white",10,0,0)

    idvalue = StringVar()
    identry = Entry(idframe,textvariable = idvalue).grid(row = 0,column = 1)

    passwordlabel = Label(passwordframe,text = "PW")
    makeLabel(passwordlabel,"white",10,0,0)

    passwordvalue = StringVar()
    passwordentry = Entry(passwordframe,textvariable = passwordvalue,show="*").grid(row = 0,column = 1)

    password2label = Label(password2frame,text = "PW 확인")
    makeLabel(password2label,"white",10,0,0)

    password2value = StringVar()
    password2entry = Entry(password2frame,textvariable = password2value,show="*").grid(row = 0,column = 1)


    namelabel = Label(nameframe,text = "닉네임")
    makeLabel(namelabel,"white",10,0,0)

    namevalue = StringVar()
    nameentry = Entry(nameframe,textvariable = namevalue).grid(row = 0,column = 1)

    okbutton = Button(okbuttonframe,text = "확인", command = joinOkClick)
    makeButton(okbutton,'#4f87e3',10,0,"white",10,0,0,)

    backbutton = Button(backbuttonframe,text = "뒤로", command = backClick)
    makeButton(backbutton,'#4f87e3',10,0,"white",10,0,0,)
    JOIN.mainloop()

def SAVEDATA(win,lose):
    global playerid
    savelib = cdll.LoadLibrary('savedataC.dll')
    save = savelib['saveData']
    save.argtypes = (c_wchar_p,c_int,c_int)
    save.restypes = c_int

    win = c_int(win)
    lose = c_int(lose)
    check = save(playerid,win,lose)

    CDLL('savedataC.dll')
    if(check==-1):
        print("해당 아이디 없음")
    else:
        print("저장완료")
        
#***********************************************메인 함수***********************************
while(True):

    if(WINDOW==-1):
        break;
    
    if(WINDOW ==0):
        MAINMENU()#1. 로그인 화면, 2. 회원가입화면 -1:종료
        
    if(WINDOW ==1):
        LOGINMENU()#3.게임시작 화면 -1:종료
        
    if(WINDOW ==2):
        JOINMEMU()#0.시작메뉴
        
    if(WINDOW ==3):
        STARTMENU()#4.게임시작 5. 게임설명 6. 게임옵션 -1:종료
        
    if(WINDOW ==4):
        GAMEPLAY()#4.다시시작 -1:종료
        
        
    if(WINDOW ==5):
        EXPLAIN()#3.게임설명화면
        
    else:
        print("오류")
