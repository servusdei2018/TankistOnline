"""
TankistOnline - Client > Viewport
Copyright (C) 2019. All Rights Reserved.
"""

class Viewport:
	
	def __init__(self, topLeftX: int, topLeftY: int, width: int, height: int):
		
		"""
		Initialize this Viewport object.
		
		Params:
		  :self: This new Viewport object
		  :topLeftX: The top-left X locus of the viewport
		  :topLeftY: The top-left Y locus of the viewport
		  :width: The width of the viewport
		  :height: The height of the viewport
		"""
		
		self.topLeftX=topLeftX
		self.topLeftY=topLeftY
		self.width=width
		self.height=height
		
	def updateXY(self, x: int, y: int):
		
		"""
		Return a XY locus relative to the viewport
		
		Params:
		  :self: A Viewport object
		  :x: X locus to relativize
		  :y: Y locus to relativize
		"""	
		
		#If an object if outside of viewport's bounds, make sure it doesn't get
		#displayed on the screen.
		if x < self.topLeftX or x > self.topLeftX+self.width:
			return (-999,-999)
		if y < self.topLeftY-self.height or y > self.topLeftY:
			return (-999,-999)
			
		diffX = abs(x-self.topLeftX)
		diffY = abs(y-self.topLeftY)
		
		return (diffX, diffY)
