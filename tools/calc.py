try:
	while True:
		w = int(input("width:"))
		h = int(input("height:"))
		try:
			while True:
				x0 = int(input("x0:"))
				y0 = int(input("y0:"))
				w1 = int(input("w1:"))
				h1 = int(input("h1:"))
				x1 = round(x0 / w, 2)
				y1 = round(y0 / h, 2)
				x2 = round((x0 + w1) / w, 2)
				y2 = round((y0 + h1) / h, 2)
				print(
					',{\n      "x_range": ' + f"[{x1:.2f}, {x2:.2f}]" + ',\n      "y_range": ' + f"[{y1:.2f}, {y2:.2f}]" + '\n    }')
		except ValueError:
			pass
except ValueError:
	pass
except KeyboardInterrupt:
	pass
