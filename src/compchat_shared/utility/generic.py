import typing

# Some functions that might be useful

# Check dict for index, if it doesn't exist, call GetFunction to get the value, store the value
# in the dict. After either case, return the value.
def cacheGet(Dictionary: dict, Index: any, GetFunction: typing.Callable):
	if Dictionary.get(Index) != None:
		return Dictionary.get(Index)
	
	else:
		NewValue = GetFunction(Index)
		Dictionary[Index] = NewValue

	return NewValue

