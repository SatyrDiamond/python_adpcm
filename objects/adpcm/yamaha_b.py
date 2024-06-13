
from ctypes import *
from objects import audio_data

class yamaha_b():
	codec_lib = cdll.LoadLibrary("./libs/ymb_codec.dll")

	codec_lib.ymb_encode.argtypes = [POINTER(c_int16), POINTER(c_ubyte), c_long]
	codec_lib.ymb_encode.restype = None

	codec_lib.ymb_decode.argtypes = [POINTER(c_ubyte), POINTER(c_int16), c_long]
	codec_lib.ymb_decode.restype = None

	def decode(self, indata):
		insize = len(indata)

		inp = (c_ubyte*insize)()[0:insize] = indata
		p_inp = cast(inp, POINTER(c_ubyte))

		outp = (c_int16*(insize*2))()
		p_outp = cast(outp, POINTER(c_int16))
		yamaha_b.codec_lib.ymb_decode(p_inp, p_outp, insize*2)

		audio_obj = audio_data.audio_obj()
		audio_obj.codec = 'uint16'
		audio_obj.pcm_from_list(p_outp[0:insize*2])
		return audio_obj
		