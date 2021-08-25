# Author :
# 	Xenakis Michail


from sys import argv
script, filename = argv
f = open(filename)
arrayWord=[]
reservedWords = ['if','in','var','for','and','do','else','procedure','function','print','inout'
,'not','to','step','program','or','return','while','call']
symbols = [',','[',']','{','}','(',')','*','+','-','/',':','=','<','>',';']
wordCounter=0
firstWord=""
line=1
quad_num=0
quad = []
counter=0
lists = []
helper=[]
id1=""
id2=""
oper=""
rel_op=""
pro_name=[]
false_count=0
id1_co=0
false=[]
let=""
nextq=[]
do_pos=[]
do_so=0
var_words=[]
word_state=""
forKey=False
notp=False

def backpatch(editlist,z):
	editlist[3]=z
	return editlist

def merge(list1,list2):
	mergelist = []
	mergelist.extend(list1)
	mergelist.extend(list2)
	return mergelist

def makelist(x):
	mk_list = []
	num=nextquad()
	mk_list.append(num)
	mk_list.append(x)
	return mk_list

def emptylist():
	new_list = [5]
	num=nextquad()
	new_list.append(num)
	return new_list

def newtemp():
	global counter
	k="T_"+str(counter)
	v="T_"+str(counter)
	t=globals()[k]=v
	counter+=1
	return t

def genquad(op,x,y,z):
	global quad
	quad.append(op)
	quad.append(x)
	quad.append(y)
	quad.append(z)
	return quad

def nextquad():
	global quad_num
	quad_num+=1;
	return quad_num

def lex():
	global ID,lastLetter,firstWord,wordCounter,wordCreation,line
	if not lastLetter:
		print "Error : expected '}' in line",line
		quit()
	wordCreation=""	
	while lastLetter.isalpha() or lastLetter.isdigit():	
		wordCreation=wordCreation+lastLetter
		for index in range(len(reservedWords)):
			if wordCreation==reservedWords[index]:
				ID=index+1
				break
			else:
				ID=-1
		lastLetter=f.read(1)
	if wordCreation=="":
		if (lastLetter=="" or lastLetter=="\n" or lastLetter=="\t"):
			ID=0
			if lastLetter=="\n":
				line=line+1
		for j in range(len(symbols)): 
			if lastLetter==symbols[j]:
				wordCreation=lastLetter
				ID=0
		lastLetter=f.read(1)
	if ID!=0:
		if wordCounter==0:
			firstWord = wordCreation
		wordCounter=wordCounter+1
	return wordCreation,ID

def relational_oper():
	global wordCreation,rel_op
	key = wordCreation
	rel_op=""
	if wordCreation=="<":
		rel_op=rel_op+wordCreation
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation=="=":
			rel_op=rel_op+wordCreation
			symbol=key+wordCreation
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation	
		elif wordCreation==">":
			rel_op=rel_op+wordCreation
			symbol=key+wordCreation
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation	
		else:	
			return wordCreation	
	elif wordCreation==">":	
		rel_op=rel_op+wordCreation
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation=="=":
			rel_op=rel_op+wordCreation
			symbol=key+wordCreation
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation	
		elif wordCreation==">":
			rel_op=rel_op+wordCreation
			symbol=key+wordCreation
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation	
		else:	
			return wordCreation	
	elif wordCreation=="=":
		rel_op=rel_op+wordCreation
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		return wordCreation	
	else:
		print "Error : expected relational operator in line",line
		quit()	

def boolFactor():
	global line,quad,helper,rel_op,false,nextq,ID,notp,word_state
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="" :
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=="not":
		notp=True
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="" :
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation=='[':
			wordCreation=condition()
			if wordCreation==']':
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="" :
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				return wordCreation
			else :
				print "Error : ']' expected after condition in line",line
				quit()
		else:
			print "Error : '[' before condition in line",line	
			quit()
	elif wordCreation=="[":
			wordCreation=condition()
			if wordCreation==']':
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="" :
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				return wordCreation
			else :
				print "Error : ']' expected after condition in line",line
				quit()						
	elif ID==-1 or wordCreation=="(":	
		id1=wordCreation
		helper.append(id1)
		wordCreation=expression()
		co=len(helper)
		count_help=0
		l=[]
		g=""
		ex1=""
		ex2=""
		boolean=False
		if co>=3:
			while count_help<co:
				if helper[count_help]=="(":
					boolean=True
					helper.pop(count_help)
					i=count_help
					l=[]
					for i in range(co):
						if helper[count_help]==")":
							helper.pop(count_help)
							break
						else:
							l.append(helper[count_help])
							helper.pop(count_help)
					g=num_equations(l)
					helper.insert(count_help,g)
				count_help=count_help+1
				co=len(helper)
			g=num_equations(helper)
			ex1=g
			helper=[]
		else:
			w=newtemp()
			quad=[]
			quad=genquad(":=",id1,"_",w)
			lists.append(quad)
			nextquad()
			ex1=w
			helper=[]
		expressionSymbol=wordCreation	
		wordCreation=relational_oper()
		if ID==-1:
			id2=wordCreation
			helper.append(id2)
			wordCreation=expression()
			co=len(helper)
			count_help=0
			l=[]
			g=""
			boolean=False
			#for hh in range(len(helper)):
			#	ex2=ex2+helper[hh]
			if co>=3:
				while count_help<co:
					if helper[count_help]=="(":
						boolean=True
						helper.pop(count_help)
						i=count_help
						l=[]
						for i in range(co):
							if helper[count_help]==")":
								helper.pop(count_help)
								break
							else:
								l.append(helper[count_help])
								helper.pop(count_help)
						g=num_equations(l)
						helper.insert(count_help,g)
					count_help=count_help+1
					co=len(helper)
				g=num_equations(helper)
				ex2=g
				helper=[]
			else:
				w=newtemp()
				quad=[]
				quad=genquad(":=",id2,"_",w)
				lists.append(quad)
				nextquad()
				ex2=w
				helper=[]
			if notp==True:
				if rel_op=="<":
					rel_op=">="
				elif rel_op==">":
					rel_op="<="
				elif rel_op=="=":
					rel_op="<>"
				elif rel_op=="<=":
					rel_op=">"
				elif rel_op==">=":
					rel_op="<"
				elif rel_op=="<>":
					rel_op="="
				notp=False
			quad=[]
			quad=genquad(rel_op,ex1,ex2,"_")
			lists.append(quad)
			nextq.append(nextquad())
			backpatch(quad,nextquad())
			quad=[]
			quad=genquad("jump","_","_","_",)
			lists.append(quad)
			return wordCreation
		else:
			print "Error : expected variable after '"+expressionSymbol+"' in line",line
			quit()
	else:
		print "Error : expected variable in line",line	
		quit()	

def boolTerm():
	global quad
	wordCreation=boolFactor()
	while wordCreation=="and":
		wordCreation=boolFactor()
	return wordCreation

def while_stat():
	global line,quad,nextq,false_count,lists,do_pos,do_so
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=="(":
		wordCreation=condition()
		false.append(nextq)
		nextq=[]
		false_count+=1
		if wordCreation==")":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			wordCreation=brack_or_stat()
			quad=[]
			quad=genquad("jump","_","_","_")
			lists.append(quad)
			nextquad()
			quad=[]
			quad=lists[len(lists)-1]
			backpatch(quad,do_pos[len(do_pos)-1])
			do_pos.pop(len(do_pos)-1)
			return wordCreation
		else:
			print "Error : ')' expected after while in line",line
			quit()
	else :
		print "Error : '(' expected after while in line",line
		quit()

def add_oper():
	if wordCreation=="+":
		return wordCreation
	elif wordCreation=="-":
		return wordCreation

def mul_oper():
	if wordCreation=="*":
		return wordCreation
	elif wordCreation=="/":
		return wordCreation

def optional_sign():
	global wordCreation,quad
	if wordCreation=="+" or wordCreation=="-":
		wordCreation=add_oper()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		return wordCreation	
	else:
		return wordCreation

def expression():
	global wordCreation,quad,id1,id2,oper,helper
	optional_sign()
	wordCreation=term()
	while wordCreation == "+" or wordCreation == "-":
		oper=wordCreation
		helper.append(oper)
		add_oper()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		id2=wordCreation
		helper.append(id2)
		wordCreation=term()
	return wordCreation

def actualParItem():
	global wordCreation,ID,callCount,line,quad
	if wordCreation=="in":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]	
		quad=[]
		quad=genquad("par",wordCreation,"cv","_")
		lists.append(quad)
		nextquad()
		wordCreation=expression()
		return wordCreation
	elif wordCreation=="inout":	
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		quad=[]
		quad=genquad("par",wordCreation,"ref","_")
		lists.append(quad)
		nextquad()	
		if ID==-1:
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation	
		elif ID>0:
			print "Error :",wordCreation,"is a reserved word.Use another word after 'inout' in line",line
			quit()
	else:
		print "Error : 'in' or 'inout' expected after 'call' in line",line
		quit()
		
def actualParList():
	global callCount,quad
	wordCreation=actualParItem()
	while wordCreation==",":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]			
		wordCreation=actualParItem()
	return wordCreation

def actualPars():
	global line,quad,wordCreation
	if wordCreation=="(":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation==")":
			return wordCreation
		else:		
			wordCreation=actualParList()
			return wordCreation
	else:
		return wordCreation

def idTail():
	global quad
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=='(':
		wordCreation=actualPars()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
	return wordCreation

def factor():
	global ID,wordCreation,line,helper,id1,id1_co
	key=wordCreation
	if ID==-1 :
		if id1_co==0:
			id1=wordCreation
			helper.append(id1)
			id1_co=1
		wordCreation=idTail()
		return wordCreation
	elif wordCreation=="(":
		if id1_co==0:
			helper.append(wordCreation)
			id1_co=1
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		helper.append(wordCreation)
		wordCreation=expression()
		if wordCreation==")":
			helper.append(wordCreation)
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation
		else:
			print "Error : ')' expected in line",line
			quit()
	elif ID>0 : 
		print "Error : word '",key,"' is reserved.Use another word in line",line
		quit()
	else :
		print "Error : not expected symbol '",key,"' in line",line
		quit()

def term():
	global wordCreation,quad,id1,helper
	wordCreation=factor()
	while wordCreation == "*" or wordCreation == "/":
		oper=wordCreation
		helper.append(oper)
		wordCreation=mul_oper()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		id2=wordCreation
		helper.append(id2)
		wordCreation=factor()
	return wordCreation	

def call_stat():
	global wordCreation,line,quad
	if wordCreation=="call":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		quad=[]
		quad=genquad("call",wordCreation,"_","_")
		lists.append(quad)
		nextquad()
		if ID==-1:
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			if wordCreation=='(':
				wordCreation=actualPars()
				if wordCreation==')':
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
					while wordCreation=="":
						arrayWord=lex()
						wordCreation=arrayWord[0]
						ID=arrayWord[1]
					if wordCreation==";":
						return wordCreation
					else:
						print "Error : expected ';' in line",line-1
						quit()
				else:
					print "Error : expected ')' in line",line
					quit()
			else:
				print "Error : expected '(' in line",line
				quit()
			
		elif ID>0:
			print "Error : word '",wordCreation,"' is a reserved word.Use another word in line",line
			quit()
		else :
			print "Error : expected a variable after 'call' in line",line
			quit()

def step_part():
	global line,wordCreation
	for_step=0
	if wordCreation=="step":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if ID==-1:
			for_step=wordCreation
			wordCreation=expression()
			return wordCreation,for_step
		else:
			print "Error : expected a variable after 'step' in line",line
			quit()
	else:
		return wordCreation

def for_stat():
	global ID,line,quad,wordCreation,false,false_count,nextq,quad,quad_num
	for_begin_id1=0
	for_begin_id2=0
	for_step=0
	to_go=0
	forKey=True
	if ID==-1:
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation==":":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			if wordCreation=="=" :
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="":
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				if ID==-1:
					for_begin_id1=wordCreation
					wordCreation=expression()
					if wordCreation=="to":
						arrayWord=lex()
						wordCreation=arrayWord[0]
						ID=arrayWord[1]
						while wordCreation=="":
							arrayWord=lex()
							wordCreation=arrayWord[0]
							ID=arrayWord[1]
						if ID==-1:	
							for_begin_id2=wordCreation
							wordCreation=expression()
							if wordCreation=="step":
								wordCreation,for_step=step_part()
							else:
								for_step=1
							w=newtemp()
							quad=[]
							quad=genquad(":=",for_begin_id1,"_",w)
							lists.append(quad)
							nextquad()
							w1=newtemp()
							quad=[]
							quad=genquad(":=",for_begin_id2,"_",w1)
							lists.append(quad)
							nextquad()
							to_go=quad_num
							quad=[]
							quad=genquad("<=",w,w1,nextquad())
							lists.append(quad)
							q=nextquad()
							backpatch(quad,q)
							quad=[]
							quad=genquad("jump","_","_","_")
							lists.append(quad)
							nextq.append(q-1)
							false.append(nextq)
							false_count+=1
							nextq=[]
							wordCreation=brack_or_stat()
							quad=[]
							quad=genquad("+",w,for_step,w)
							lists.append(quad)
							nextquad()
							quad=[]
							quad=genquad("jump","_","_",to_go)
							lists.append(quad)
							nextquad()
							return wordCreation
						else:
							print "Error : expected variable after 'to' in line",line
							quit()
					else:
						print "Error : expected word 'to' after expression in line",line
						quit()
				else:
					print "Error : expected variable after '=' in line",line	
					quit()	
			else:
				print "Error : expected symbol '=' after ':' in line",line
				quit()
		else:
			print "Error : symbol ':' expected after 'for' in line",line
			quit()
	elif ID>0:
		print "Error : word '"+wordCreation+"' is a reserved word.Use another word after 'for' in line",line
		quit()
	else :
		print "Error : expected word after 'for' in line",line		
		quit()

def print_stat():
	global wordCreation,line,quad
	if  wordCreation=="(":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if ID==-1:
			quad=[]
			quad=genquad("print",wordCreation,"_","_")
			lists.append(quad)
			nextquad()
			wordCreation=expression()
			if wordCreation==")":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="":
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				if wordCreation==";":
					return wordCreation
				else:
					print "Error : expected ';' in line",line-1
					quit()
			else:
				print "Error : expected ')' in line",line
				quit()
		else:
			print "Error : expected variable in 'print' in line",line
			quit()		
	else :
		print "Error : expected '(' after 'print' in line",line
		quit()

def formalParItem():
 	global wordCreation,line
 	key = wordCreation
	if wordCreation=="in" or wordCreation=="inout":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if ID==-1:
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			return wordCreation
		else:
			print "Error : expected variable after'",key,"' in line",line
			quit()
	else:
		print "Error : expected 'in','inout' or ')' in line",line
		quit()

def assignment_stat():
	global ID,wordCreation,line,id1_co,let,forKey
	key=wordCreation
	if ID==-1:
		id1_co=0
		let=wordCreation
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation==":":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			if wordCreation=="=":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="":
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				if ID==-1 or wordCreation=="(" or wordCreation=="-" or wordCreation=="+":
					wordCreation=expression()
				else: 
					print "Error : expected variable after '=' in line",line
					quit()
				if wordCreation==")":
					print "Error : expected '(' in line",line
					quit()	
				if forKey==False:
					if wordCreation!=";":
						print "Error : expected ';' in line",line-1
						quit()
				return wordCreation
			else:
				print "Error : expected '=' after ':' in line",line
				quit()
		else:
			print "Error : expected ':' after",key,"in line",line
			quit()		
	elif ID>0:
		print "Error : word '",key,"' is reserved word in line",line
		quit()
	else :
		print "Error : expected word, not symbol '",key,"' in line",line
		quit()

def condition():
	global quad
	wordCreation=boolTerm()
	while wordCreation=="or":
		wordCreation=boolTerm()
	return wordCreation

def if_stat():
	global line,quad,nextq,false,false_count
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=="(":
		wordCreation=condition()
		false.append(nextq)
		nextq=[]
		false_count+=1
		if wordCreation==")":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			wordCreation=brack_or_stat()
			wordCreation=elsepart()
			return wordCreation
		else:
			print "Error : expected symbol ')' in line",line
			quit()
	else:
		print "Error : expected symbol '(' in line",line
		quit()

def num_equations(helper):
	global lists,quad
	co=len(helper)
	h=1
	while True:
		if h+2<co:
			if (helper[h]=="+" or helper[h]=="-") and (helper[h+2]=="*" or helper[h+2]=="/"):
				id1=helper[h+1]
				oper=helper[h+2]
				id2=helper[h+3]
				w=newtemp()
				quad=[]
				quad=genquad(oper,id1,id2,w)
				lists.append(quad)
				nextquad()
				helper.pop(h+3)
				helper.pop(h+2)
				helper.pop(h+1)
				helper.insert(h+1,w)
				co=len(helper)
			elif (helper[h]=="/" or helper[h]=="*"):
				id1=helper[h-1]
				oper=helper[h]
				id2=helper[h+1]
				w=newtemp()
				quad=[]
				quad=genquad(oper,id1,id2,w)
				lists.append(quad)
				nextquad()
				helper.pop(h+1)
				helper.pop(h)
				helper.pop(h-1)
				helper.insert(h-1,w)
				co=len(helper)
			else:
				id1=helper[h-1]
				oper=helper[h]
				id2=helper[h+1]
				w=newtemp()
				quad=[]
				quad=genquad(oper,id1,id2,w)
				lists.append(quad)
				nextquad()
				helper.pop(h+1)
				helper.pop(h)
				helper.pop(h-1)
				helper.insert(h-1,w)
				co=len(helper)
		else:
			if len(helper)>2:
				id1=helper[h-1]
				oper=helper[h]
				id2=helper[h+1]
				w=newtemp()
				quad=[]
				quad=genquad(oper,id1,id2,w)
				lists.append(quad)
				nextquad()
				helper.pop(h+1)
				helper.pop(h)
				helper.pop(h-1)
				helper.insert(h-1,w)
				co=len(helper)
			f=helper[0]
			helper=[]
			return f

def statement():
	global ID,wordCreation,lastLetter,symbols,helper,quad,lists,let,quad_num,false_count,do_so,do_pos,word_state
	if ID==-1:
		word_state=wordCreation
		wordCreation=assignment_stat()
		co=len(helper)
		count_help=0
		l=[]
		g=""
		boolean=False
		if co>=3:
			while count_help<co:
				if helper[count_help]=="(":
					boolean=True
					helper.pop(count_help)
					i=count_help
					l=[]
					for i in range(co):
						if helper[count_help]==")":
							helper.pop(count_help)
							break
						else:
							l.append(helper[count_help])
							helper.pop(count_help)
					g=num_equations(l)
					helper.insert(count_help,g)
				count_help=count_help+1
				co=len(helper)
			num_equations(helper)
			quad=[]
			quad=genquad(":=",helper[0],"_",let)
			lists.append(quad)
			nextquad()
			helper=[]
		else:
			w=newtemp()
			quad=[]
			quad=genquad(":=",id1,"_",w)
			lists.append(quad)
			nextquad() 
			quad=[]
			quad=genquad(":=",w,"_",let)
			lists.append(quad)
			nextquad()
			helper=[]
	elif wordCreation=="if":
		wordCreation=if_stat()
		for i in range(len(false[false_count-1])):
			quad=[]
			quad=lists[false[false_count-1][i]] 
			backpatch(quad,quad_num)
		false.pop(false_count-1)
		false_count-=1
	elif wordCreation=="while":
		do_so+=1
		do_pos.append(quad_num)
		wordCreation=while_stat()
		for i in range(len(false[false_count-1])):
			quad=[]
			quad=lists[false[false_count-1][i]] 
			backpatch(quad,quad_num)
		false.pop(false_count-1)
		false_count-=1
	elif wordCreation=="do":
		do_so+=1
		do_pos.append(quad_num)
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=do_while_stat()
	elif wordCreation=="for":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=for_stat()
		for i in range(len(false[false_count-1])):
			quad=[]
			quad=lists[false[false_count-1][i]] 
			backpatch(quad,quad_num)
		false.pop(false_count-1)
		false_count-=1
	elif wordCreation=="call":
		call_stat()
	elif wordCreation=="return":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=return_stat()
	elif wordCreation=="print":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=print_stat()
	elif wordCreation==":" :
		print "Error : expected variable in line",line
		quit()
	return wordCreation

def sequence():
	global wordCreation,quad
	wordCreation=statement()
	while wordCreation==";":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=statement()
	return wordCreation

def bracket_seq():
	global line
	wordCreation=sequence()
	if wordCreation=="}":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		return wordCreation
	else :
		print "Error : expected '}' in line",line
		quit()
 
def brack_or_stat():
	global wordCreation
	if wordCreation=="{":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=bracket_seq()
		return wordCreation
	else:
		wordCreation=statement()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		return wordCreation
	
def return_stat():
	global wordCreation,line,quad,lists
	if wordCreation=="(":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if ID==-1:
			quad=[]
			quad=genquad("ret","_","_",wordCreation)
			lists.append(quad)
			nextquad()
			wordCreation=expression()
			if wordCreation==")":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="":
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				if wordCreation==";":
					return wordCreation
				else:
					print "Error : expected ';' after return in line",line-1
					quit()
		
			else:	
				print "Error : expected ')' in line",line
				quit()
		else:
			print "Error : expected variable in line",line
			quit()
	else:
		print "Error : expected '(' after 'return' in line",line
		quit()

def do_while_stat():
	global line,quad,do_pos,do_so,quad_num,nextq
	wordCreation=brack_or_stat()
	if wordCreation=="while":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation=="(":
			wordCreation=condition()
			if wordCreation!=")":
				print "Error, expected ')' in line",line-1
			else:
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
				while wordCreation=="":
					arrayWord=lex()
					wordCreation=arrayWord[0]
					ID=arrayWord[1]
				quad=[]
				quad=lists[len(lists)-2]
				quad.pop(3)
				quad.append(do_pos[len(do_pos)-1])
				lists.pop(len(lists)-1)
				quad_num-=1
				nextq.pop(len(nextq)-1)
				return wordCreation
		else:
			print "Error : expected '(' after 'while' in line",line
			quit()
	else:
		print "Error : expected 'while' after '}' in line",line
		quit()

def elsepart():
	global wordCreation,quad,false,nextq,false_count,lists,quad_num
	if wordCreation=="else":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		false.append(nextq)
		nextq=[]
		false_count+=1
		for i in range(len(false[false_count-2])):
			quad=[]
			quad=lists[false[false_count-2][i]] 
			backpatch(quad,quad_num+1)
		false.pop(false_count-2)
		false_count-=1
		quad=[]
		quad=genquad("jump","_","_","_")
		lists.append(quad)
		nextq=[]
		nextq.append(nextquad()-1)
		false.append(nextq)
		false_count+=1
		wordCreation=brack_or_stat()
		for i in range(len(false[false_count-1])):
			quad=[]
			quad=lists[false[false_count-1][i]] 
			backpatch(quad,quad_num)
		false.pop(false_count-1)
		false_count-=1
		nextq.pop(len(nextq)-1)
	return wordCreation
		
def formalParList():
	wordCreation=formalParItem()
	while wordCreation==",":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		wordCreation=formalParItem()
	return wordCreation

def formalPars():
	global quad,wordCreation
	key = wordCreation
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=="(":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation!=")":
			wordCreation=formalParList()
			if wordCreation==")":
				return wordCreation
			else :
				print "Error : expected ')' in line",line
				quit()
		else :
			return wordCreation	
	else:
		print "Error : expected '(' after '"+key+"' in line",line
		quit()

def funcbody():
	global quad
	wordCreation=formalPars()
	workCreation=block()
	return wordCreation

def func():
	global wordCreation,line,quad,lists,pro_name
	key = wordCreation
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="" or wordCreation=="\n" or wordCreation=="\t":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	quad=[]
	quad=genquad("begin_block",wordCreation,"_","_")
	lists.append(quad)
	nextquad()
	pro_name.append(wordCreation)
	if ID==-1:
		wordCreation=funcbody()
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="" or wordCreation=='\t' or wordCreation=="\n":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]	
		return wordCreation
	elif ID>0:
		print "Error : word '",wordCreation,"'in line",line,"is a reserved word"
	else:
		print "Error : expected word,not symbol '",wordCreation,"' in line",line 	

def subPrograms():
	global wordCreation,quad
	while wordCreation=="function" or wordCreation=="procedure":
		wordCreation=func()
	return wordCreation

def varList():
	global ID,quad,var_words
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	while ID==-1:
		var_words.append(wordCreation)
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
		while wordCreation=="":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
		if wordCreation==",":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			if ID!=-1:
				print "Error : expected variable after ',' in line",line
				quit()
		else:
			return wordCreation
	if ID!=-1:
		print "Error : expected variable in line",line
		quit()

def declarations():
	global line,ID
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if wordCreation=="var":
		wordCreation=varList()
		if wordCreation==",":
			print "Error : variable is missing in line",line
			quit()
		elif wordCreation!=";":
			print "Error : expected ';' in line",line-1
			quit()
		return True
	else:
		return False		

def block():
	global quad,pro_name
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if  wordCreation=="{":
		w=True
		while w==True:
			w=declarations()
		wordCreation=subPrograms()
		wordCreation=sequence()
		if wordCreation!="}" :
			print "Error : expected '}' in line",line-1
			quit()
		else : 
			pr=len(pro_name)-1
			quad=[]
			quad=genquad("end_block",pro_name[pr],"_","_")
			pro_name.pop(pr)
			lists.append(quad)
			nextquad()
			return wordCreation
	else:
		print "Error : expected '{' in line",line
		quit()

def sun():
	global lastLetter,wordCreation,line,quad,pro_name
	lastLetter=f.read(1)
	arrayWord=lex()
	wordCreation=arrayWord[0]
	ID=arrayWord[1]
	while wordCreation=="":
		arrayWord=lex()
		wordCreation=arrayWord[0]
		ID=arrayWord[1]
	if firstWord!="program":
			print "Error : word 'program' expected as first word in line",line
			quit()
	if ID>0 :
		if firstWord=="program":
			arrayWord=lex()
			wordCreation=arrayWord[0]
			ID=arrayWord[1]
			while wordCreation=="":
				arrayWord=lex()
				wordCreation=arrayWord[0]
				ID=arrayWord[1]
			if ID==-1:
				genquad("begin_block",wordCreation,"_","_")
				pro_name.append(wordCreation)
				lists.append(quad)
				nextquad()
				workCreation=block()
				quad=[]
				quad=genquad("halt","_","_","_")
				lists.append(quad)
				if wordCreation=="}":
					while lastLetter=="" or lastLetter=="\n" or lastLetter=="\t":
						if not lastLetter:
							print "Program has been successfully compiled"
							break	
						lastLetter=f.read(1)
					for i in range(len(symbols)):
						if lastLetter.isalpha() or lastLetter.isdigit() or lastLetter==symbols[i] :
							arrayWord=lex()
							wordCreation=arrayWord[0]
							ID=arrayWord[1]
							print "Error: words after line",line,"are invalid "	
							quit()
				else:
					print "Error : expected '}',closing program"
					quit()
			else:
				print "Error : expected program's name in line",line
				quit()
			
def int_output():
	global lists
	file = open(filename.split(".")[0]+".int", "w")
	for iu in range(len(lists)):
		file.write(str(iu)+": "+str(lists[iu])+"\n")
	file.close()

def c_output():
	global lists,quad_num,counter,var_words
	file = open(filename.split(".")[0]+".c", "w")
	file.write("#include <stdio.h>\n")
	file.write("int main() {\n")
	i=0
	file.write("\tint ")
	for i in range(counter-1):
		file.write("T_"+str(i)+",")
	file.write("T_"+str(counter-1))
	file.write(";\n")
	file.write("\tint ")
	for i in range(len(var_words)-1):
		file.write(var_words[i]+",")
	if len(var_words)>0:
		file.write(var_words[len(var_words)-1])
		file.write(";\n")
	ii=0
	for ii in range(len(lists)):
		file.write("\tL_"+str(ii)+": ")
		if lists[ii][0]==":=":
			file.write(str(lists[ii][3])+"="+str(lists[ii][1])+";"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="<=" or lists[ii][0]==">=" or lists[ii][0]=="<" or lists[ii][0]==">":
			file.write("if "+"("+str(lists[ii][1])+str(lists[ii][0])+str(lists[ii][2])+")"+" goto L_"+str(lists[ii][3])+";"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="=":
			file.write("if "+"("+str(lists[ii][1])+"=="+str(lists[ii][2])+")"+" goto L_"+str(lists[ii][3])+";"+"//"+str(lists[ii])+"\n")	
		elif lists[ii][0]=="<>":
			file.write("if "+"("+str(lists[ii][1])+"!="+str(lists[ii][2])+")"+" goto L_"+str(lists[ii][3])+";"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="+" or lists[ii][0]=="-" or lists[ii][0]=="*" or lists[ii][0]=="/":
			file.write(str(lists[ii][3])+"="+str(lists[ii][1])+str(lists[ii][0])+str(lists[ii][2])+";"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="jump":
			file.write("goto L_"+str(lists[ii][3])+";"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="print":
			file.write("printf(\"%d\\n\","+lists[ii][1]+");"+"//"+str(lists[ii])+"\n")
		elif lists[ii][0]=="halt":
			file.write("{}")
		else:
			file.write("\n")
	file.write("\n}")

sun()
int_output()
c_output()