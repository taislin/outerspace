

# general holder for ALL data in game
class IDataHolder:

    #def __setattr__(self, key, value):
    #    self.__dict__[key] = value
    #    self.__dict__['_v_modified'] = 1

    #def setModified(self, modified):
    #    self.__dict__['_v_modified'] = modified

    # for debug only
    def __repr__(self):
        result = '<%s.%s %X ' % (self.__class__.__module__, self.__class__.__name__, id(self))
        items = self.__dict__.items()
        items.sort()
        for key, value in items:
            result += '%s=%s, ' % (key, repr(value))
        result += '>'
        return result

def makeIDataHolder(**kwargs):
    obj = IDataHolder()
    for key, value in kwargs.items():
        setattr(obj, key, value)
    return obj
