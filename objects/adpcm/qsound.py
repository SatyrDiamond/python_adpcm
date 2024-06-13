
from ctypes import *
from objects import audio_data

class qsound():
	codec_lib = cdll.LoadLibrary("./libs/bs_codec.dll")

	codec_lib.bs_encode.argtypes = [POINTER(c_int16), POINTER(c_ubyte), c_long]
	codec_lib.bs_encode.restype = None

	codec_lib.bs_decode.argtypes = [POINTER(c_ubyte), POINTER(c_int16), c_long]
	codec_lib.bs_decode.restype = None

	def decode(self, indata):
		insize = len(indata)

		inp = (c_ubyte*insize)()[0:insize] = indata
		p_inp = cast(inp, POINTER(c_ubyte))

		outp = (c_int16*(insize*2))()
		p_outp = cast(outp, POINTER(c_int16))
		qsound.codec_lib.bs_decode(p_inp, p_outp, insize*2)

		audio_obj = audio_data.audio_obj()
		audio_obj.codec = 'uint16'
		audio_obj.pcm_from_list(p_outp[0:insize*2])
		return audio_obj
		