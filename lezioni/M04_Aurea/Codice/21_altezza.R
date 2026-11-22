# X uniforme [0, .2], adimensionale
dunif(.1, 0, .2)        # densita' 5
punif(.15, 0, .2) -
  punif(.05, 0, .2)     # area .5
# Il punto singolo ha area zero
punif(.1, 0, .2) - punif(.1, 0, .2)
