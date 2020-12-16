
class Record:
	def __init__(self, PtrComp, Discr, EnumComp, IntComp, StringComp):
		self.PtrComp = PtrComp
		self.Discr = Discr
		self.EnumComp = EnumComp
		self.IntComp = IntComp
		self.StringComp = StringComp

	def copy(self):
		return Record(self.PtrComp, self.Discr, self.EnumComp, self.IntComp, self.StringComp)

TRUE = 1
FALSE = 0
IntGlob = 0
BoolGlob = FALSE
Char1Glob = ''
Char2Glob = ''
PtrGlb = None
PtrGlbNext = None

Ident1 = 1
Ident2 = 2 
Ident3 = 3
Ident4 = 4
Ident5 = 5

Array1Glob = [0]*51

def create_array2glob(n):
	r = []
	for i in range(n):
		r.append( list(Array1Glob) )
	return r

Array2Glob = create_array2glob(51)

def Func3(EnumParIn):
	EnumLoc = EnumParIn
	if EnumLoc == Ident3: return TRUE
	return FALSE

def Proc6(EnumParIn):
	EnumParOut = EnumParIn
	if not Func3(EnumParIn):
		EnumParOut = Ident4
	if EnumParIn == Ident1:
		EnumParOut = Ident1
	elif EnumParIn == Ident2:
		if IntGlob > 100:
			EnumParOut = Ident1
		else:
			EnumParOut = Ident4
	elif EnumParIn == Ident3:
		EnumParOut = Ident2
	elif EnumParIn == Ident4:
		pass
	elif EnumParIn == Ident5:
		EnumParOut = Ident3
	return EnumParOut

def Proc7(IntParI1, IntParI2):
	IntLoc = IntParI1 + 2
	IntParOut = IntParI2 + IntLoc
	return IntParOut

def Proc2(IntParIO):
	IntLoc = IntParIO + 10
	while True:
		if Char1Glob == 'A':
			IntLoc = IntLoc - 1
			IntParIO = IntLoc - IntGlob
			EnumLoc = Ident1
		if EnumLoc == Ident1:
			break
	return IntParIO

def Proc3(PtrParOut):
	global IntGlob
	if PtrGlb is not None:
		PtrParOut = PtrGlb.PtrComp
	else:
		IntGlob = 100
	PtrGlb.IntComp = Proc7(10, IntGlob)
	return PtrParOut

def Proc4():
	global Char2Glob
	BoolLoc = Char1Glob == 'A'
	BoolLoc = BoolLoc or BoolGlob
	Char2Glob = 'B'

def Proc5():
	global Char1Glob
	global BoolGlob
	Char1Glob = 'A'
	BoolGlob = FALSE


def Proc8(Array1Par, Array2Par, IntParI1, IntParI2):
	global IntGlob

	IntLoc = IntParI1 + 5
	Array1Par[IntLoc] = IntParI2
	Array1Par[IntLoc+1] = Array1Par[IntLoc]
	Array1Par[IntLoc+30] = IntLoc
	for IntIndex in range(IntLoc, IntLoc+2):
		Array2Par[IntLoc][IntIndex] = IntLoc
	Array2Par[IntLoc][IntLoc-1] = Array2Par[IntLoc][IntLoc-1] + 1
	Array2Par[IntLoc+20][IntLoc] = Array1Par[IntLoc]
	IntGlob = 5

def Func1(CharPar1, CharPar2):
	CharLoc1 = CharPar1
	CharLoc2 = CharLoc1
	if CharLoc2 != CharPar2:
		return Ident1
	else:
		return Ident2

def Func2(StrParI1, StrParI2):
	IntLoc = 1
	while IntLoc <= 1:
		if Func1(StrParI1[IntLoc], StrParI2[IntLoc+1]) == Ident1:
			CharLoc = 'A'
			IntLoc = IntLoc + 1
	if CharLoc >= 'W' and CharLoc <= 'Z':
		IntLoc = 7
	if CharLoc == 'X':
		return TRUE
	else:
		if StrParI1 > StrParI2:
			IntLoc = IntLoc + 7
			return TRUE
		else:
			return FALSE

def Proc1(PtrParIn):
	NextRecord = PtrGlb.copy()
	PtrParIn.PtrComp = NextRecord
	PtrParIn.IntComp = 5
	NextRecord.IntComp = PtrParIn.IntComp
	NextRecord.PtrComp = PtrParIn.PtrComp
	NextRecord.PtrComp = Proc3(NextRecord.PtrComp)
	if NextRecord.Discr == Ident1:
		NextRecord.IntComp = 6
		NextRecord.EnumComp = Proc6(PtrParIn.EnumComp)
		NextRecord.PtrComp = PtrGlb.PtrComp
		NextRecord.IntComp = Proc7(NextRecord.IntComp, 10)
	else:
		PtrParIn = NextRecord.copy()
	NextRecord.PtrComp = None
	return PtrParIn


def Proc0(loops):
	global IntGlob
	global BoolGlob
	global Char1Glob
	global Char2Glob
	global Array1Glob
	global Array2Glob
	global PtrGlb
	global PtrGlbNext

	PtrGlbNext = Record(None, 0, 0, 0, 0 )
	PtrGlb = Record(PtrGlbNext, Ident1, Ident3, 40, "DHRYSTONE PROGRAM, SOME STRING")

	String1Loc = "DHRYSTONE PROGRAM, 1'ST STRING"
	Array2Glob[8][7] = 10

	ops = 0
	for i in range(loops):
		Proc5()
		Proc4()
		IntLoc1 = 2
		IntLoc2 = 3
		String2Loc = "DHRYSTONE PROGRAM, 2'ND STRING"
		EnumLoc = Ident2
		BoolGlob = not Func2(String1Loc, String2Loc)
		while IntLoc1 < IntLoc2:
			IntLoc3 = 5 * IntLoc1 - IntLoc2
			IntLoc3 = Proc7(IntLoc1, IntLoc2)
			IntLoc1 = IntLoc1 + 1
			ops += 1
		Proc8(Array1Glob, Array2Glob, IntLoc1, IntLoc3)
		PtrGlb = Proc1(PtrGlb)
		CharIndex = 'A'
		while CharIndex <= Char2Glob:
			if EnumLoc == Func1(CharIndex, 'C'):
				EnumLoc = Proc6(Ident1)
			CharIndex = chr(ord(CharIndex)+1)
			ops += 1
		IntLoc3 = IntLoc2 * IntLoc1
		IntLoc2 = IntLoc3 / IntLoc1
		IntLoc2 = 7 * (IntLoc3 - IntLoc2) - IntLoc1
		IntLoc1 = Proc2(IntLoc1)
		ops += 1
	return ops


def pystones(loops):
	return Proc0(loops)


def main():
	LOOPS = 100000
	ops = pystones( LOOPS )
	print(ops)

main()
