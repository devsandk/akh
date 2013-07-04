# -*- coding:utf-8 -*-
#!/usr/bin/env python 
""" Ahtung!!! Говнокод"""
import sqlite3 as db
import os
import sys
import time
from subprocess import Popen, PIPE
c=db.connect('base.db')
cur=c.cursor()
inp=0
try:
    cur.execute(""" CREATE TABLE users (
                            usercard INTEGER,
                            userid INTEGER );""")
except db.DatabaseError, x:
    print "Error: ",x
try:
    cur.execute(""" CREATE TABLE clientreg (
                bullshit INTEGER,
                secnum INTEGER);""")
except db.DatabaseError, x:
    print "Error: ",x
try:
    cur.execute("""CREATE TABLE cells (
                row VARCHAR(150),
                secnum INTEGER,
                rowindex VARCHAR(30))""")
except db.DatabaseError, x:
    print 'Error: ',x
c.commit()
class Menu:
    def __init__(self, pathdb=''):
        self.pathdb=pathdb
    
    def addcell(self, row=None, snum=None):
        if row==None:
            row=raw_input('Введите порядковый номер стойки \n или q для выход в основное меню: \n')
            self.addcell(row)
        elif row=='q':
            self.printMenu(None)
        else:
            try:
                snum=int(raw_input('Введите номер блока управления:\n'))
                cur.execute(""" UPDATE cells set rowindex=%s where secnum=%d"""%(row, snum))
                c.commit()
                self.addcell()
            except:
                snum=None
                row=None
                self.printMenu(None)

    def addadmin(self, usercard=None, userid=None):
        if usercard==None:
            usercard=raw_input('Введите номер карты:\n')
            self.addadmin(usercard)
        else:
            try:
                userid=int(raw_input('Введите номер пользователя от 9-12:\n'))
            except:
                userid=None
            if userid in [9,10,11,12]:
               cur.execute(""" UPDATE users set usercard=%s where userid=%d"""% (usercard, userid))
               c.commit()
               self.printMenu(None)
            else:
                self.addadmin()

    def clearcardbase(self):
        cur.execute(""" DELETE FROM clientreg""")
        c.commit()
        self.printMenu()
    
    def clearallcell(self):
        cur.execute(""" DELETE FROM cells""")
        c.commit()
        self.printMenu()
    
    def clearonecell(self):
        snum=int(raw_input('Введите номер блока управления: \n'))
        cur.execute(""" DELETE FROM cells WHERE secnum=%d""" % snum)
        c.commit()
        self.printMenu()

    def reboot(self):
        p=Popen(["sudo","reboot"])
        p.communicate()

    def baseback(self):
        p=Popen(['cp','base.db','base.backup'])
        p.communicate()
        self.printMenu()

    def killavkars(self):
        p=Popen(["sudo","killall","-TERM","avkars"])
        p.communicate()
        self.printMenu()

    def initsells(self, num=None, size=None, cellpos=None):
        if num==None:
            num=int(raw_input('Порядковый номер ячейки:\n'))
            size=int(raw_input('Размер ячейки:\n'))
            cellpos=int(raw_input('Прзиция в стойке:\n'))
            cur.execute("""UPDATE cells set num=%d, size=%d WHERE rowindex=1 and cellpos=%d """%(num,size,cellpos))
            c.commit() 
            self.initsells()
        elif num=='q':
            self.printMenu(None)


    def printMenu(self, data=None):
        items=('0)Сделать бекап базы','1)Прописывание админимтративных карт:','2)Очистка базы использованых карт:','3)Очистка всей базы о стойках','4)Очистка одной стойки из базы', '5)Установка и регистрация новых стоек', '6)Нумерация ячеек','8)Перезагрузка сервера','9)Убить АКХ','q)Выход')
        print("Выбрите необходимое действие или введите 'q' для выхода:")
        for val in items:
            print val
        data=raw_input()
# Attention!!! Говнокод :))
        if data=='1':
          self.addadmin()
        elif data=='0':
            self.baseback()
        elif data=='2':
            self.clearcardbase()
        elif data=='3':
            self.clearallcell()
        elif data=='4':
            self.clearonecell()
        elif data=='5':
            self.addcell()
        elif data=='6':
            self.initsells()
        elif data=='9':
            self.killavkars()
        elif data=='q':
            print 'Коней сеанса'
        elif data=='8':
            self.reboot()
        else:
            self.printMenu()
print(""" 
**************************************************************************
*                                                                        *
**************************************************************************""")
obj=Menu()
obj.printMenu()
