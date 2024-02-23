import base64

from .config import Config
from .validator import Validator

class Encode:
	def __init__(self, data: str | dict, config: Config = Config()) -> None:
		self.__data = data
		self.config = config
		self.validator = Validator(self.__data, self.config._use_print)

	def _b64_encode(self, content: str = None) -> str:
		data = self.__data
		if content:
			data = content
		if self.validator.isBoolean(data):
			if not self.config._encode_bool:
				return data

		bytes = str(data).encode(self.config._encoding)
		content_bytes = base64.b64encode(bytes)
		return content_bytes.decode(self.config._encoding)

	def b64_str(self) -> str:
		if self.validator.check(_type=str):
			encoded = self._b64_encode()
			return encoded

	def b64_dict(self, encode_values: bool=True, encode_keys: bool=False) -> dict:
		if self.validator.check(_type=dict):
			dict_encoded = {}
			if encode_values:
				for key, value in self.__data.items():
					if encode_keys:
						key = self._b64_encode(str(key))
					dict_encoded[key] = self._b64_encode(str(value))
				return dict_encoded