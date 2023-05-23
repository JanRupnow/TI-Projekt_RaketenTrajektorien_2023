#from astropy import get_body_barycentric_posvel
import datetime
from astropy.time import Time
from variables.konstanten import *
from astropy.coordinates import get_body_barycentric_posvel

print(get_body_barycentric_posvel("mars", Time(datetime.datetime.now()))[1].xyz[0]*(AU/86400))
print(get_body_barycentric_posvel("mars", Time(datetime.datetime.now()))[1].xyz[1]*(AU/86400))