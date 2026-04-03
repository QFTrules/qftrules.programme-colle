set table "magnet_field.plot.table"; set format "%.5f"
 f(x,y) = 1.0*(y+0.4)/sqrt((y+0.4)**2+x**2) - (1.0)*(y-0.4)/sqrt((y-0.4)**2+x**2); set xrange [-3:3]; set yrange [-3:3]; set view 0,0; set isosample 800,800; set cont base; set cntrparam levels discrete 0.05,0.1,0.2,0.3,0.4; unset surface; splot f(x,y) 
