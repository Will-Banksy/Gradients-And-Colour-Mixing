col1 = color(255, 0, 0)
col2 = color(0, 255, 0)

def setup():
	size(600, 600)
	background(0xaaaaaa)
	midAdd = additiveMix(col1, col2, "scale")
	print("midAdd: r={}, g={}, b={}".format(red(midAdd), green(midAdd), blue(midAdd)))
	midSub = subtractiveMix(col1, col2, "scale")
	print("midSub: r={}, g={}, b={}".format(red(midSub), green(midSub), blue(midSub)))
	# rgb = HSBtoRGB(120, 50, 75)
	# print("rgb: r={}, g={}, b={}".format(red(rgb), green(rgb), blue(rgb)))
	# print("HSB", RGBtoHSB(color(255, 255, 0)))
	# rgb = getCol_MixMethod3(col1, col2, 1)
	# print("rgb: r={}, g={}, b={}".format(red(rgb), green(rgb), blue(rgb)))

def draw():
	for i in range(width):
		colour = getCol_MixMethod5(col1, col2, map(i, 0, width, 0, 1))
		stroke(colour)
		line(i, 0, i, height)
		noLoop()

# Simple linear interpolation
def getCol_MixMethod1(col1, col2, amt):
	return lerpColor(col1, col2, amt)

# Additive Mixing
def getCol_MixMethod2(col1, col2, amt):
	mid = additiveMix(col1, col2, "scale")
	if(amt < 0.5):
		return lerpColor(col1, mid, amt * 2)
	elif(amt == 0.5):
		return mid
	else:
		return lerpColor(mid, col2, map(amt, 0.5, 1, 0, 1))

# Interpolate across HSB cylinder
def getCol_MixMethod3(col1, col2, amt, debug = False):
	if(debug == True):
		print("-- start mix --")
		
		print("COL1", red(col1), green(col1), blue(col1))
		print("COL2", red(col2), green(col2), blue(col2))
	
	hsb1 = RGBtoHSB(col1)
	hsb2 = RGBtoHSB(col2)
	
	if(debug == True):
		print("HSB1", hsb1)
		print("HSB2", hsb2)
	
	ang1 = hsb1[0]
	dist1 = hsb1[1]
	z1 = hsb1[2]
	
	v1 = PVector(cos(radians(ang1)) * dist1, sin(radians(ang1)) * dist1)
	
	if(debug == True):
		print("ADZ1", ang1, dist1, z1)
		print("V1", v1)
	
	ang2 = hsb2[0]
	dist2 = hsb2[1]
	z2 = hsb2[2]
	
	v2 = PVector(cos(radians(ang2)) * dist2, sin(radians(ang2)) * dist2)
	
	if(debug == True):
		print("ADZ2", ang2, dist2, z2)
		print("V2", v2)
	
	vres = PVector.lerp(v1, v2, amt)
	angres = degrees(vres.heading())
	distres = vres.mag()
	zres = lerp(z1, z2, amt)
	
	if(debug == True):
		print("VRES", vres)
		print("ANGRES", angres)
		print("DISTRES", distres)
	
	H = angres
	S = distres
	Br = zres
	
	if(H < 0):
		H += 360
	elif(H > 360):
		H -= 360
	
	H = constrain(H, 0, 360)
	S = constrain(S, 0, 100)
	Br = constrain(Br, 0, 100)
	
	if(debug == True):
		print("HSB", H, S, Br)
	
		print("-- end mix --")
	
	# print(H, S, Br)
	return HSBtoRGB(H, S, Br)

# Subtractive Mixing
def getCol_MixMethod4(col1, col2, amt):
	mid = subtractiveMix(col1, col2, "scale")
	if(amt < 0.5):
		return lerpColor(col1, mid, amt * 2)
	elif(amt == 0.5):
		return mid
	else:
		return lerpColor(mid, col2, map(amt, 0.5, 1, 0, 1))

# Linear interpolation using the HSB colour model
def getCol_MixMethod5(col1, col2, amt):
	hsb1 = RGBtoHSB(col1)
	hsb2 = RGBtoHSB(col2)
	if(abs(hsb1[0] - hsb2[0]) > 180):
		H = lerp(hsb2[0], hsb1[0], amt) + 180
	else:
		H = lerp(hsb1[0], hsb2[0], amt)
	S = lerp(hsb1[1], hsb2[1], amt)
	B = lerp(hsb1[2], hsb2[2], amt)
	if(H < 0):
		H += 360
	elif(H > 360):
		H -= 360
	
	H = constrain(H, 0, 360)
	S = constrain(S, 0, 100)
	Br = constrain(B, 0, 100)
	return HSBtoRGB(H, S, B)

# Mixes two colours together subtractively
def additiveMix(col1, col2, mode):
	if(mode == "crop"):
		r = int(red(col1)) + int(red(col2))
		g = int(green(col1)) + int(green(col2))
		b = blue(col1) + blue(col2)
		r = 255 if r > 255 else r
		g = 255 if g > 255 else g
		b = 255 if b > 255 else b
	elif(mode == "scale"):
		r = int(red(col1)) + int(red(col2))
		g = int(green(col1)) + int(green(col2))
		b = blue(col1) + blue(col2)
		max = r if (r > g and r > b) else (g if (g > r and g > b) else b)
		if(max > 255):
			r = (r / max) * 255
			g = (g / max) * 255
			b = (b / max) * 255
	elif(mode == "bitwise"):
		r = int(red(col1)) | int(red(col2))
		g = int(green(col1)) | int(green(col2))
		b = int(blue(col1)) | int(blue(col2))
	return color(r, g, b)

# Mixes two colours together additively
def subtractiveMix(col1, col2, cutoffMode):
	cmyk1 = RGBtoCMYK(red(col1), green(col1), blue(col1))
	cmyk2 = RGBtoCMYK(red(col2), green(col2), blue(col2))
	
	c = cmyk1[0] + cmyk2[0]
	m = cmyk1[1] + cmyk2[1]
	y = cmyk1[2] + cmyk2[2]
	k = cmyk1[3] + cmyk2[3]
	mx = Max(c, m, y, k)
	
	if(mx > 255):
		if(cutoffMode == "crop"):
			c = 255 if c > 255 else c
			m = 255 if m > 255 else m
			y = 255 if y > 255 else y
			k = 255 if k > 255 else k
		elif(cutoffMode == "scale"):
			c = (float(c) / mx) * 255
			m = (float(m) / mx) * 255
			y = (float(y) / mx) * 255
			k = (float(k) / mx) * 255
	rgb = CMYKtoRGB(c, m, y, k)
	return rgb

# Returns a CMYK tuple
def RGBtoCMYK(r, g, b):
	r = float(r)
	g = float(g)
	b = float(b)
	k = float(255 - Max(r, g, b))
	if(k == 255):
		return (0, 0, 0, 255)
	c = constrain(int((255 - r - k) / (255 - k) * 255), 0, 255)
	m = constrain(int((255 - g - k) / (255 - k) * 255), 0, 255)
	y = constrain(int((255 - b - k) / (255 - k) * 255), 0, 255)
	return (c, m, y, k)

# Returns an RGB tuple
def CMYKtoRGB(c, m, y, k):
	c = float(c)
	m = float(m)
	y = float(y)
	k = float(k)
	r = constrain(int(255 * (1 - c / 255) * (1 - k / 255)), 0, 255)
	g = constrain(int(255 * (1 - m / 255) * (1 - k / 255)), 0, 255)
	b = constrain(int(255 * (1 - y / 255) * (1 - k / 255)), 0, 255)
	return color(r, g, b)

# Returns an HSB tuple
def RGBtoHSB(col):
	R = red(col) / 255
	G = green(col) / 255
	B = blue(col) / 255
	
	mx = Max(R, G, B)
	mn = Min(R, G, B)
	delta = mx - mn
	
	H = 0
	if(delta == 0):
		H = 0
	elif(mx == R):
		H = 60 * (((G - B) / delta) + 0)
	elif(mx == G):
		H = 60 * (((B - R) / delta) + 2)
	elif(mx == B):
		H = 60 * (((R - G) / delta) + 4)
	
	S = 0
	if(mx == 0):
		S = 0
	else:
		S = delta / mx
	
	Br = mx
	
	if(H < 0):
		H += 360
	elif(H > 360):
		H -= 360
	
	H = constrain(H, 0, 360)
	S = constrain(S * 100, 0, 100)
	Br = constrain(Br * 100, 0, 100)
	
	return (H, S, Br)

def Min(*args):
	mn = args[0]
	for i in args:
		if(i < mn):
			mn = i
	return mn

def Max(*args):
	mx = args[0]
	for i in args:
		if(i > mx):
			mx = i
	return mx

# Returns an RGB tuple
def HSBtoRGB(H, S, Br):
	S = float(S) / 100
	Br = float(Br) / 100
	
	k = ((5) + H / 60) % 6;
	R = Br - Br * S * max(0, Min(k, 4 - k, 1));
	
	k = ((3) + H / 60) % 6;
	G = Br - Br * S * max(0, Min(k, 4 - k, 1));
	
	k = ((1) + H / 60) % 6;
	B = Br - Br * S * max(0, Min(k, 4 - k, 1));
	
	R = constrain(R * 255, 0, 255)
	G = constrain(G * 255, 0, 255)
	B = constrain(B * 255, 0 , 255)
	
	return color(R, G, B)