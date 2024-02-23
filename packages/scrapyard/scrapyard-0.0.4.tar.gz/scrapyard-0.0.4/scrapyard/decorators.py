class _MetadataDecorator:
	CHECK_EXP = lambda self, obj: True
	ATTRIBUTE_NAME = "__object_metadata__"

	def __call__(self, obj: object) -> object:
		if self.CHECK_EXP(obj):
			metadata_list = getattr(obj, self.ATTRIBUTE_NAME, [])
			metadata_list.append(self)
			setattr(obj, self.ATTRIBUTE_NAME, metadata_list)
			return obj

		else:
			raise Exception(f"Cannot add metadata '{self.__class__.__qualname__}' to object '{obj}'")
		

class _CallableDecorator(_MetadataDecorator):
	CHECK_EXP = lambda self, obj: callable(obj)


class _ClassDecorator(_MetadataDecorator):
	CHECK_EXP = lambda self, obj: isinstance(obj, type)

		

# Callable decorators

class EventListener(_CallableDecorator):
	def __init__(self, event_name: str):
		self.event_name = event_name
	


# Class decorators
		
class DependsOn(_ClassDecorator):
	FORCED_DEPENDENCY = True
	def __init__(self, *dependencies: str):
		self.dependencies = frozenset(dependencies)
		
	
class DependsOnIfExists(DependsOn):
	FORCED_DEPENDENCY = False
		


class DependsOnTags(_ClassDecorator):
	def __init__(self, *tags: str):
		self.tags = frozenset(tags)



class TaggedWith(_ClassDecorator):
	def __init__(self, *tags: str):
		self.tags = frozenset(tags)