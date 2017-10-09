
import ac
import acsys
import math


SmileyShowTime = 0.1	


DriftSpeedMin = 25		


SlipAngleMin = 4

SlipAngleMid = 20		


SlipAngleHigh = 45

# in the real driftbox hardware this should be 100°, but in AC it seems the angle can never be reached - 87
SlipAngleSpin = 86

# real driftbox this would be 10 kph. slightly higher for better effect
DSpeedSpin = 12

# Code starts here, stay away! ###

SmileyTimer = 0
DriftAngle = 0
DSpeed = 0
DPeak = 0

Peakcounter = 1

def acMain(ac_version):

	global DriftAngle, DSpeed, DPeak, appWindow, CurSlipAngle, speedlabel, peaklabel
	
	ac.initFont(0, "Roboto", 1, 1)
	
	# Frame settings.
	appWindow = ac.newApp("driftbox_transparent")
	ac.setSize(appWindow, 200, 100)
	ac.setTitle(appWindow, "driftbox")
	ac.drawBorder(appWindow,0)
	
	ac.setBackgroundOpacity(appWindow, 0.1)
	ac.setIconPosition(appWindow, -10, -10)
	speedlabel = ac.addLabel(appWindow, "km/h")
	peaklabel = ac.addLabel(appWindow, "peak")
	ac.setPosition(peaklabel, 185, 30)
	ac.setPosition(speedlabel, 20, 30)
	ac.setFontAlignment(peaklabel, "center")
	ac.setFontAlignment(speedlabel, "center")
	ac.setFontSize(speedlabel, 10)
	ac.setFontSize(peaklabel, 10)
	DPeak = ac.addLabel(appWindow, "0°")
	DriftAngle = ac.addLabel(appWindow, "0°")
	DSpeed = ac.addLabel(appWindow, "0")
	ac.setPosition(DPeak, 194, 40)
	ac.setPosition(DriftAngle, 100, 20)
	ac.setPosition(DSpeed, 16, 44)
	ac.setFontAlignment(DPeak, "right")
	ac.setFontAlignment(DriftAngle, "center")
	ac.setFontAlignment(DSpeed, "center")
	#ac.setSize(DPeak, 39, 30)
	#ac.setSize(DriftAngle, 73, 47)
	#ac.setSize(DSpeed, 42, 25)
	ac.setFontSize(DriftAngle, 55)
	ac.setFontSize(DSpeed, 17)
	ac.setFontSize(DPeak, 27)
	ac.setCustomFont(DriftAngle, "Roboto", 1, 0)
	ac.setCustomFont(DSpeed, "Roboto", 1, 0)
	ac.setCustomFont(DPeak, "Roboto", 1, 0)
	ac.setFontColor(DriftAngle, 0.95, 0.95, 0.95, 1)
	ac.setFontColor(DSpeed, 0.75, 0.75, 0.75, 1)
	ac.setFontColor(DPeak, 0.65, 0.65, 0.65, 1)

	ac.addRenderCallback(appWindow, driftanglebar)
	
	
		
def acUpdate(deltaT):
	global SmileyTimer, SmileyShowTime, SlipAngleMin, SlipAngleMid, SlipAngleHigh, DriftAngle, DSpeed, DSpeedSpin, SlipAngleSpin, DPeak, Peakcounter, appWindow, CurSlipAngle, CurSpeed, Peakindicator
	
	CurSpeed = ac.getCarState(0, acsys.CS.SpeedKMH)
	FL, FR, RL, RR = ac.getCarState(0, acsys.CS.SlipAngle)
	CurSlipAngle = math.fabs( round( (RL+RR)/2 ) )


	if SmileyTimer > SmileyShowTime:
		
		
		if CurSpeed >= DriftSpeedMin:
			SmileyShowTime = 0.1
			ac.setVisible(DPeak, 1)
			ac.setVisible(DSpeed, 1)
			ac.setVisible(peaklabel, 1)
			ac.setVisible(speedlabel, 1)
			if CurSlipAngle > Peakcounter:
				Peakcounter = CurSlipAngle
				Peakindicator = CurSlipAngle
			ac.setText(DriftAngle, "{:.0f}°".format(CurSlipAngle))
			ac.setText(DSpeed, "{:.0f}".format(CurSpeed))
			ac.setText(DPeak, "{:.0f}°".format(Peakcounter))
		else:
			Peakcounter = 0
		if CurSlipAngle >= SlipAngleSpin:
			SmileyShowTime = 1.5
			ac.setVisible(DSpeed, 0)
			ac.setVisible(DPeak, 0)
			ac.setVisible(peaklabel, 0)
			ac.setVisible(speedlabel, 0)
			ac.setText(DriftAngle, "SPIN!")
			Peakcounter = 0
			SmileyTimer = 0
		if CurSpeed <= DSpeedSpin and CurSlipAngle >= SlipAngleHigh:
			SmileyShowTime = 1.5
			ac.setVisible(DSpeed, 0)
			ac.setVisible(DPeak, 0)
			ac.setVisible(peaklabel, 0)
			ac.setVisible(speedlabel, 0)
			ac.setText(DriftAngle, "SPIN!")
			Peakcounter = 0
			SmileyTimer = 0
		SmileyTimer = 0
	else:
		SmileyTimer += deltaT
	
def driftanglebar(deltaT):
	global SmileyTimer, SmileyShowTime, SlipAngleMin, SlipAngleMid, SlipAngleHigh, DriftAngle, DSpeed, DSpeedSpin, SlipAngleSpin, DPeak, Peakcounter, appWindow, CurSlipAngle, CurSpeed, Peakindicator

	ac.glColor4f(0.05, 0.05, 0.05, 0.25)
	ac.glQuad(5, 82, 185, 15)
	if SmileyShowTime != 1.5:
		ac.glColor4f(0.15, 0.75, 0.75, 0.7)
		ac.glQuad(5, 82, (CurSlipAngle * 1.8), 15)
		ac.glColor4f(0.55, 0.15, 0.15, 0.7)
		ac.glQuad( 5 + Peakindicator * 1.8, 82, 2, 15)
		