import hashlib as HL

from .config import Config
from .encode import Encode
from .decode import Decode

class Hash:
	def __init__(self, config: Config = Config()) -> None:
		self.config = config
	
	def md5(self, string: str) -> str:
		return HL.md5(str(string + self.config._md5_solt).encode(self.config._encoding)).hexdigest()

	def password(self, string: str) -> str:
		return HL.md5(Encode(string, self.config).b64_str().encode()).hexdigest()

	def password_equals(self, password: str, string: str) -> str:
		psw = self.password(string)

		if psw == password or password == psw:
			return True
		return False