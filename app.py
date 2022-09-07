from housingPrediction.pipeline.pipeline import Pipeline
from housingPrediction.config.configration import Configration

config = Configration()
pipeline = Pipeline(config=config)

pipeline.run_pipeline()