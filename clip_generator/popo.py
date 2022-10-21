fase = 0
sec_step = [3, 1, 0.5]


j = 0
i = sec_step[fase]-offset
offset = 0.001


while i<duracion
if i>duracion:
	timestamp["start"].append(j)
	timestamp["end"].append(duracion)
	return

timestamp["start"].append(j)
timestamp["end"].append(i)
	
j = i + offset
i += sec_step[fase]



PUTA VIDA, TODO ESTO SE PUEDE SOLUCIONAR CON EL CHOPPER, el metodo de cortar cada cierto segundos, lo unico es ver como unir los dos ultimos videos y ya, que los trozos de timestamp no validados que no estan conectados se guerden en una carpeta aparte, y asi cada vez que se le haga chop, no haya complicaciones