from abc import ABC, abstractclassmethod

FACTORIES = {}


def register(cls):
    def helper(c):
        if c == ABC:
            return True
        for base in c.__bases__:
            if helper(base):
                FACTORIES[c.__name__] = FACTORIES.get(c.__name__, {})
                if c != cls:
                    FACTORIES[c.__name__][cls.__name__] = cls
        return False

    helper(cls)
    return cls


@register
class DataLoader(ABC):
    @abstractclassmethod
    def load(cls):
        pass

    @abstractclassmethod
    def __call__(cls):
        pass


@register
class DataProcessor(ABC):
    @abstractclassmethod
    def process(cls):
        pass

    @abstractclassmethod
    def __call__(cls):
        pass


@register
class DataAggregator(ABC):
    @abstractclassmethod
    def aggregate(cls):
        pass

    @abstractclassmethod
    def __call__(self):
        pass


@register
class DataWriter(ABC):
    @abstractclassmethod
    def __call__(cls):
        pass


@register
class TofDataLoader(DataLoader):
    def __init__(self, path, delimiter, keys) -> None:
        self.path = path
        self.delimiter = delimiter
        self.keys = keys

    def load(self):
        pass

    def __call__(self, data):
        data["DataLoader"] = True


@register
class TofDataProcessor(DataProcessor):
    def __init__(self, use_fluor, time_to_mass, noise_range, bkg_range) -> None:
        self.use_fluor = use_fluor
        self.time_to_mass = time_to_mass
        self.noise_range = noise_range
        self.bkg_range = bkg_range

    def process(self):
        pass

    def __call__(self, data):
        data["DataProcessor"] = True


@register
class TofDataAggregator(DataAggregator):
    def __init__(self, masses, groupby_keys) -> None:
        self.masses = masses
        self.groupby_keys = groupby_keys

    def aggregate(self):
        pass

    def __call__(self, data):
        data["DataAggregator"] = True


@register
class CsvDataWriter(DataWriter):
    def __init__(self, path) -> None:
        self.path = path

    def __call__(self, data):
        data["Csv"] = True


@register
class PlotDataWriter(DataWriter):
    def __init__(self, path, figsize) -> None:
        self.path = path
        self.figsize = figsize

    def __call__(self, data):
        data["Plot"] = True


@register
class ConfigDataWriter(DataWriter):
    def __init__(self, path, config) -> None:
        self.path = path
        self.config = config

    def __call__(self, data):
        data["Config"] = self.config
