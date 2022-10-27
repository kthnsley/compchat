import typing

def cacheGet(Dictionary: dict, Index: any, GetFunction: typing.Callable):
	if Dictionary.get(Index) != None:
		return Dictionary.get(Index)
	
	else:
		NewValue = GetFunction(Index)
		Dictionary[Index] = NewValue

	return NewValue

