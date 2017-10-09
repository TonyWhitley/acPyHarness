
import ac
import acsys
import math


SmileyShowTime = 0.1	


DriftSpeedMin = 25		


SlipAngleMin = 4

SlipAngleMid = 20		


SlipAngleHigh = 45

# in the real driftbox hardware this should be 100°, but in AC it seems the angle can never be reached - can be set higher though 
SlipAngleSpin = 86

# real driftbox this would be 10 kph. slightly higher for better effect
DSpeedSpin = 12

# Code starts here, stay away! ###

SmileyTimer = 0
DriftAngle = 0
DSpeed = 0
DPeak = 0

Peakcounter = 1

background = "apps/python/driftbox/gfx/db_bg_driftpractice.png"
spinout = "apps/python/driftbox/gfx/db_bg_spinfull.png"

def acMain(ac_version):

	global DriftAngle, DSpeed, DPeak, appWindow, CurSlipAngle
	
	ac.initFont(0, "Roboto", 1, 1)
	
	# Frame settings.
	appWindow = ac.newApp("driftbox")
	ac.setSize(appWindow, 400, 226)
	ac.setTitle(appWindow, "")
	ac.drawBorder(appWindow, 0)
	
	ac.setBackgroundTexture(appWindow, background)
	ac.setBackgroundOpacity(appWindow,0)
	ac.setIconPosition(appWindow, 59, 163)
	
	DPeak = ac.addLabel(appWindow, "0°")
	DriftAngle = ac.addLabel(appWindow, "0°")
	DSpeed = ac.addLabel(appWindow, "0")
	ac.setPosition(DPeak, 234, 66)
	ac.setPosition(DriftAngle, 166, 64)
	ac.setPosition(DSpeed, 120, 66)
	ac.setFontAlignment(DPeak, "right")
	ac.setFontAlignment(DriftAngle, "center")
	ac.setFontAlignment(DSpeed, "center")
	ac.setSize(DPeak, 39, 30)
	ac.setSize(DriftAngle, 73, 47)
	ac.setSize(DSpeed, 42, 25)
	ac.setFontSize(DriftAngle, 41)
	ac.setFontSize(DSpeed, 25)
	ac.setFontSize(DPeak, 25)
	ac.setCustomFont(DriftAngle, "Roboto", 1, 0)
	ac.setCustomFont(DSpeed, "Roboto", 1, 0)
	ac.setCustomFont(DPeak, "Roboto", 1, 0)
	ac.setFontColor(DriftAngle, 0.05, 0.05, 0.05, 1)
	ac.setFontColor(DSpeed, 0.05, 0.05, 0.05, 1)
	ac.setFontColor(DPeak, 0.05, 0.05, 0.05, 1)

	ac.addRenderCallback(appWindow, driftanglebar)
	
	
		
def acUpdate(deltaT):
	global SmileyTimer, SmileyShowTime, SlipAngleMin, SlipAngleMid, SlipAngleHigh, DriftAngle, DSpeed, DSpeedSpin, SlipAngleSpin, DPeak, Peakcounter, appWindow, CurSlipAngle, CurSpeed, Peakindicator
	
	CurSpeed = ac.getCarState(0, acsys.CS.SpeedKMH)
	FL, FR, RL, RR = ac.getCarState(0, acsys.CS.SlipAngle)
	CurSlipAngle = math.fabs( round( (RL+RR)/2 ) )


	if SmileyTimer > SmileyShowTime:
		
		ac.setVisible(DSpeed, 1)
		ac.setVisible(DriftAngle, 1)
		ac.setVisible(DPeak, 1)
		ac.setBackgroundTexture(appWindow, background)
		if CurSpeed >= DriftSpeedMin:
			SmileyShowTime = 0.1
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
			ac.setVisible(DriftAngle, 0)
			ac.setVisible(DPeak, 0)
			ac.setBackgroundTexture(appWindow, spinout)
			Peakcounter = 0
			ac.setText(DriftAngle, "0°")
			SmileyTimer = 0
		if CurSpeed <= DSpeedSpin and CurSlipAngle >= SlipAngleHigh:
			SmileyShowTime = 1.5
			ac.setVisible(DSpeed, 0)
			ac.setVisible(DriftAngle, 0)
			ac.setVisible(DPeak, 0)
			ac.setBackgroundTexture(appWindow, spinout)
			Peakcounter = 0
			ac.setText(DriftAngle, "0°")
			SmileyTimer = 0
		SmileyTimer = 0
	else:
		SmileyTimer += deltaT
	
def driftanglebar(deltaT):
	global SmileyTimer, SmileyShowTime, SlipAngleMin, SlipAngleMid, SlipAngleHigh, DriftAngle, DSpeed, DSpeedSpin, SlipAngleSpin, DPeak, Peakcounter, appWindow, CurSlipAngle, CurSpeed, Peakindicator

	if SmileyShowTime != 1.5:
		ac.glColor4f(0.05, 0.05, 0.05, 0.8)
		ac.glQuad(123, 120, (CurSlipAngle * 1.7), 15)
		ac.glColor4f(0.05, 0.05, 0.05, 0.8)
		ac.glQuad( 123 + Peakindicator * 1.7, 120, 2, 15)
		