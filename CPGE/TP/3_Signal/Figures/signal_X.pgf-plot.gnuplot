set table "signal_X.pgf-plot.table"; set format "%.5f"
set samples 300.0; plot [x=0:6] 2* 0.5 * sin(2*3.14*0.5* x) * sin(2*3.14*5* x) * sin(2*3.14*5* x)
