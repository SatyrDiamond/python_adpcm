

from objects.adpcm import yamaha_z

decode_object = yamaha_z.yamaha_z()

f = open('snd_01.raw', 'rb')

outdata = decode_object.decode_aica(f.read())

o = open('out.raw', 'wb')

o.write(outdata.to_raw())
