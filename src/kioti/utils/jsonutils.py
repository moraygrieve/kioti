import json

class JsonConverter(object):
    translate = {}

    @classmethod
    def registerTranslation(clsself, s1, s2):
        clsself.translate[s1] = s2

    @classmethod
    def complex_handler(clsself, obj):
        dict = {}
        for key in clsself.objectMembers(obj).keys():
            if clsself.translate.has_key(key): dict[clsself.translate[key]] = clsself.objectMembers(obj)[key]
            else: dict[key] = clsself.objectMembers(obj)[key]
        return dict

    @classmethod
    def toJSON(clsself, obj, indent=None, sort_keys=None):
        return json.dumps(clsself.objectMembers(obj), default=clsself.complex_handler, indent=indent, sort_keys=sort_keys)

    @classmethod
    def toFile(clsself, obj, path, indent=None):
        with open(path, 'w') as jfile:
            jfile.writelines([clsself.toJSON(obj, indent=indent)])
        return path

    @classmethod
    def objectMembers(clsself, obj):
        dict={}
        if hasattr(obj.__class__, 'props'):
            for prop in obj.__class__.props(): dict[prop] = getattr(obj, prop)
        if hasattr(obj, '__dict__'):
            for attr,value in obj.__dict__.items():
                if not attr.startswith('_'):
                    dict[attr] = value
        return dict
