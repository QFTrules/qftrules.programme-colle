set table "dipole.plot.table"; set format "%.5f"
 f(x,y) = +10*(x+0.1)/sqrt((x+0.1)**2+y**2) + -10*(x-0.1)/sqrt((x-0.1)**2+y**2); set xrange [-6:6]; set yrange [-6:6]; set view 0,0; set isosample 400,400; set cont base; set cntrparam levels discrete 0.1,0.3,0.5,0.8,1,2; unset surface; splot f(x,y) 
