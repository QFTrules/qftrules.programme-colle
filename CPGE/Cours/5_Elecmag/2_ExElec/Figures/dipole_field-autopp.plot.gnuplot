set table "dipole_field-autopp.plot.table"; set format "%.5f"
 f(x,y) = 1.0*(y+0.05)/sqrt((y+0.05)**2+x**2) - (1.0)*(y-0.05)/sqrt((y-0.05)**2+x**2); set xrange [-3:3]; set yrange [-3:3]; set view 0,0; set isosample 800,800; set cont base; set cntrparam levels discrete 0.003,0.012,0.03,0.045,0.07,0.1; unset surface; splot f(x,y) 
