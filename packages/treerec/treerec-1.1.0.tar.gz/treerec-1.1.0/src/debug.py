import treerec

C = treerec.TreeObj_Cursor()
C.execute('session K')
C.execute('create new Dev .')
C.execute('recroot -n T -p / treerec')
C.execute('cd $ "C:/Program Files (x86)/Steam/steamapps/common"')
C.execute('recroot -n steam .')

en = C.engine
tr = en.treedict['new']

C.mainloop()
