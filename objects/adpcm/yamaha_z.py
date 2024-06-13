
from ctypes import *
from objects import audio_data

class yamaha_z():
	codec_lib = cdll.LoadLibrary("./libs/ymz_codec.dll")

	codec_lib.aica_encode.argtypes = [POINTER(c_int16), POINTER(c_ubyte), c_long]
	codec_lib.aica_encode.restype = None

	codec_lib.aica_decode.argtypes = [POINTER(c_ubyte), POINTER(c_int16), c_long]
	codec_lib.aica_decode.restype = None

	codec_lib.ymz_encode.argtypes = [POINTER(c_int16), POINTER(c_ubyte), c_long]
	codec_lib.ymz_encode.restype = None

	codec_lib.ymz_decode.argtypes = [POINTER(c_ubyte), POINTER(c_int16), c_long]
	codec_lib.ymz_decode.restype = None

	def decode_aica(self, indata):
		insize = len(indata)

		inp = (c_ubyte*insize)()[0:insize] = indata
		p_inp = cast(inp, POINTER(c_ubyte))

		outp = (c_int16*(insize*2))()
		p_outp = cast(outp, POINTER(c_int16))
		yamaha_z.codec_lib.aica_decode(p_inp, p_outp, insize*2)

		audio_obj = audio_data.audio_obj()
		audio_obj.codec = 'uint16'
		audio_obj.pcm_from_list(p_outp[0:insize*2])
		return audio_obj

	def decode(self, indata):
		insize = len(indata)

		inp = (c_ubyte*insize)()[0:insize] = indata
		p_inp = cast(inp, POINTER(c_ubyte))

		outp = (c_int16*(insize*2))()
		p_outp = cast(outp, POINTER(c_int16))
		yamaha_z.codec_lib.ymz_decode(p_inp, p_outp, insize*2)

		audio_obj = audio_data.audio_obj()
		audio_obj.codec = 'uint16'
		audio_obj.pcm_from_list(p_outp[0:insize*2])
		return audio_obj