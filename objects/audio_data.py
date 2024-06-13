
import numpy

class audio_obj:
	def __init__(self):

		self.is_pcm = False
		self.pcm_data = []
		self.pcm_bits = 8
		self.pcm_uses_float = False
		self.pcm_signed = False

		self.channels = 1
		self.rate = 44100
		self.codec = None

	def set_codec_meta(self):
		self.is_pcm = (self.codec in ['uint8','int8','uint16','int16','uint32','int32'])

		if self.codec == 'uint8': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 8, False
		if self.codec == 'int8': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 8, True
		if self.codec == 'uint16': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 16, False
		if self.codec == 'int16': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 16, True
		if self.codec == 'uint32': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 32, False
		if self.codec == 'int32': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = False, 32, True
		if self.codec == 'float': self.pcm_uses_float, self.pcm_bits, self.pcm_signed = True, 32, True

	def pcm_from_stream(self, in_arr, in_size):
		if self.codec == 'uint8': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.uint8, count=in_size)
		elif self.codec == 'int8': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.int8, count=in_size)
		elif self.codec == 'uint16': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.uint16, count=in_size//2)
		elif self.codec == 'int16': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.int16, count=in_size//2)
		elif self.codec == 'uint32': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.uint32, count=in_size//4)
		elif self.codec == 'int32': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.int32, count=in_size//4)
		elif self.codec == 'float': self.pcm_data = numpy.fromfile(in_arr, dtype=numpy.float32, count=in_size//4)
		self.set_codec_meta()

	def pcm_from_bytes(self, in_arr):
		if self.codec == 'uint8': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.uint8)
		elif self.codec == 'int8': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.int8)
		elif self.codec == 'uint16': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.uint16)
		elif self.codec == 'int16': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.int16)
		elif self.codec == 'uint32': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.uint32)
		elif self.codec == 'int32': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.int32)
		elif self.codec == 'float': self.pcm_data = numpy.frombuffer(in_arr, dtype=numpy.float32)
		self.set_codec_meta()

	def pcm_from_list(self, in_arr):
		if self.codec == 'uint8': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.uint8)
		elif self.codec == 'int8': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.int8)
		elif self.codec == 'uint16': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.uint16)
		elif self.codec == 'int16': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.int16)
		elif self.codec == 'uint32': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.uint32)
		elif self.codec == 'int32': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.int32)
		elif self.codec == 'float': self.pcm_data = numpy.asarray(in_arr, dtype=numpy.float32)
		self.set_codec_meta()

	def pcm_to_signed(self):
		if self.pcm_signed and self.is_pcm:
			self.pcm_signed = False
			if self.codec == 'uint8': 
				self.pcm_data = self.pcm_data.astype('int8')-128
				self.codec = 'int8'
			if self.codec == 'uint16': 
				self.pcm_data = self.pcm_data.astype('int16')-32768
				self.codec = 'int16'
			if self.codec == 'uint32': 
				self.pcm_data = self.pcm_data.astype('int32')-2147483648
				self.codec = 'int32'

	def pcm_to_unsigned(self):
		if not self.pcm_signed and self.is_pcm:
			self.pcm_signed = True
			if self.codec == 'int8': 
				self.pcm_data = self.pcm_data.astype('uint8')-128
				self.codec = 'uint8'
			if self.codec == 'int16': 
				self.pcm_data = self.pcm_data.astype('uint16')-32768
				self.codec = 'uint16'
			if self.codec == 'int32': 
				self.pcm_data = self.pcm_data.astype('uint32')-2147483648
				self.codec = 'uint32'

	def pcm_to_float(self):
		if not self.pcm_uses_float and self.is_pcm:
			self.pcm_to_signed()
			self.set_codec_meta()
			self.pcm_uses_float = True
			if self.pcm_bits == 8: self.pcm_data = self.pcm_data.astype('float32')/127
			if self.pcm_bits == 16: self.pcm_data = self.pcm_data.astype('float32')/32768
			if self.pcm_bits == 32: self.pcm_data = self.pcm_data.astype('float32')/2147483648

	def pcm_from_float(self, n_bits):
		if self.pcm_uses_float and self.is_pcm:
			self.pcm_signed = True
			self.pcm_bits = n_bits
			self.pcm_uses_float = False
			if n_bits == 8: 
				self.pcm_data = (self.pcm_data*127).astype('int8')
				self.codec = 'int8'
			if n_bits == 16: 
				self.pcm_data = (self.pcm_data*32768).astype('int16')
				self.codec = 'int16'
			if n_bits == 32: 
				self.pcm_data = (self.pcm_data*2147483648).astype('int32')
				self.codec = 'int32'

	def pcm_bits_up(self, n_bits):
		if not self.pcm_uses_float and self.is_pcm:
			if self.pcm_bits == 8:
				if n_bits == 16: 
					self.pcm_data = self.pcm_data.astype('int16')*(257)
					if self.codec == 'int8': self.codec == 'int16'
					if self.codec == 'uint8': self.codec == 'uint16'
				if n_bits == 32: 
					self.pcm_data = self.pcm_data.astype('int32')*((1<<24)+(1<<16)+(1<<8)+1)
					if self.codec == 'int8': self.codec == 'int32'
					if self.codec == 'uint8': self.codec == 'uint32'
			if self.pcm_bits == 16:
				if n_bits == 32: 
					self.pcm_data = self.pcm_data.astype('int32')*((256*256)+1)
					if self.codec == 'int16': self.codec == 'int32'
					if self.codec == 'uint16': self.codec == 'uint32'
			self.pcm_bits = n_bits

	def pcm_bits_down(self, n_bits):
		if not self.pcm_uses_float and self.is_pcm:
			if self.pcm_bits == 16:
				if n_bits == 8: 
					self.pcm_data = (self.pcm_data//256).astype('int8')
					if self.codec == 'int16': self.codec == 'int8'
					if self.codec == 'uint16': self.codec == 'uint8'
			if self.pcm_bits == 32:
				if n_bits == 16: 
					self.pcm_data = (self.pcm_data>>16).astype('int16')
					if self.codec == 'int32': self.codec == 'int16'
					if self.codec == 'uint32': self.codec == 'uint16'
				if n_bits == 8: 
					self.pcm_data = (self.pcm_data>>24).astype('int8')
					if self.codec == 'int32': self.codec == 'int8'
					if self.codec == 'uint32': self.codec == 'uint8'
			self.pcm_bits = n_bits

	def pcm_change_bits(self, n_bits):
		if self.pcm_bits < n_bits: self.pcm_bits_up(n_bits)
		if self.pcm_bits > n_bits: self.pcm_bits_down(n_bits)

	def to_raw(self):
		return self.pcm_data.tobytes()

