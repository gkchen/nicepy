from factories.factories import FACTORIES, ConfigDataWriter
import yaml
import copy


def read_config(path):
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config


def load_factories(config):
    orig_config = copy.copy(config)
    for factory in ["DataLoader", "DataProcessor", "DataAggregator"]:
        conf = config[factory]
        cls = FACTORIES[factory][conf["type"]]
        params = conf.get("params", {})
        config[factory] = cls(**params)

    conf = config["DataWriter"]
    objs = [ConfigDataWriter(conf["path"], orig_config)]
    for writer in conf["writers"]:
        cls = FACTORIES["DataWriter"][writer["type"]]
        params = writer.get("params", {})
        objs.append(cls(path=conf["path"], **params))
    config["DataWriter"] = objs

    return config


def execute_factories(config):
    data = {}
    for factory in ["DataLoader", "DataProcessor", "DataAggregator", "DataWriter"]:
        objs = config[factory]
        if not isinstance(objs, list):
            objs = [objs]
        for obj in objs:
            obj(data)


def run(path):
    config = read_config(path)
    config = load_factories(config)
    execute_factories(config)


run("default.yaml")
