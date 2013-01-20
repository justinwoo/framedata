import fdataget
from multiprocessing import Process, Lock

lock = Lock()

engine = fdataget.fdataengine('./out', './aliastable.dat', lock)
line = ':nick!username@host PRIVMSG (channel)/(nick) :]seth low strong'
print engine.parsePRIVMSG(line)
line = ':nick!username@host PRIVMSG #kigurumi :]seth crouch strong'
print engine.parsePRIVMSG(line)
line = ':right1!comcast.net PRIVMSG #kigurumi :]seth crouch'
print engine.parsePRIVMSG(line)
line = ':dfnsdfjkl@host PRIVMSG #kigurumi :]seth rouch'
print engine.parsePRIVMSG(line)