import enum

class Item():
	def __init__(self, name, value):
		self.name=name
		self.value=value
	
	def getName(self):
		return self.name
	
	def getValue(self):
		return self.value

class ItemType(enum.Enum):
	key="KEY"
	weapon="WEAPON"
	armor="ARMOR"
	

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
