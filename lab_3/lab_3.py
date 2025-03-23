from pydantic import BaseModel, Field
from typing import List, Dict
import yaml
import matplotlib.pyplot as plt


class TimeSeriesEntry(BaseModel):
    timestamp: str
    value: float

class MetaData(BaseModel):
    location: str
    units: str

class DataSource(BaseModel):
    name: str
    type: str
    url: str
    metadata: MetaData
    time_series: List[TimeSeriesEntry] = Field(default=list)

class Configuration(BaseModel):
    version: str
    description: str
    data_sources: List[DataSource]


def load_config_from_yaml(yaml_path: str):
    try:
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        return Configuration(**data)
    except FileNotFoundError:
        raise FileNotFoundError(f"YAML не найден в: {yaml_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Ошибкаа парсинга YAML: {e}")
    except Exception as e:
        raise ValueError(f"Ошибка загрузки конфигурации: {e}")
    
def visualization(data: List[TimeSeriesEntry]):
    dct = dict()
    for temp in data:
        dct[temp.timestamp] = temp.value

    plt.plot(dct.keys(), dct.values())
    plt.xlabel('Дата')
    plt.ylabel('Темпиратура')
    plt.title('Темпиратура по датам')
    plt.show(block=True)
    
if __name__ == "__main__":
    config = load_config_from_yaml("temp.yaml")
    visualization(config.data_sources[0].time_series)