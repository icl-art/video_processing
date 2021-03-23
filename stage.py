from typing import List
import warnings
import timeit

#Stage represents a stage in the video pipeline
class stage:
    def __init__(self, name, output_dir, function, **metadata):
        self.name = name
        self.output_dir = output_dir
        self.function = function
        self.metadata = metadata

    def set_input_dir(self, input_dir: str) -> None:
        self.input_dir = input_dir

    def execute(self):
        self.function(self.input_dir, self.output_dir, self.metadata)

class pipeline:
    #Connect all stages
    def __init__(self, input_dir: str, stages: List[stage]):
        if len(stages) == 0:
            warnings.warn("Your pipeline is empty")
            return
        stages[0].input_dir = input_dir
        for i in range(1, len(stages)):
            stages[i].set_input_dir(stages[i-1].output_dir)

        self.stages = stages
        print(f"Pipeline set up successfully. Outputs can be found at {stages[-1].output_dir}")

    def execute(self, time: bool, progress: bool) -> None:
        for (i, stage) in enumerate(self.stages):
            if time:
                timeit.timeit(stage.execute())
            else:
                stage.execute()
            if progress:
                print(f"Stage {stage.name} completed. {i+1}/{len(self.stages)}")

        print("================================")
        print("Pipeline completed")