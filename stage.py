from typing import List
from progress.bar import Bar
import warnings
import timeit
import os

#Stage represents a stage in the video pipeline
class stage:
    def __init__(self, name, output_dir, function, show_progress: bool, **metadata):
        self.name = name
        self.output_dir = output_dir
        self.function = function
        self.metadata = metadata
        if show_progress:
            self.progress_indicator = Bar(name)
        else:
            self.progress_indicator = None

    def set_input_dir(self, input_dir: str) -> None:
        self.input_dir = input_dir
        if self.progress_indicator != None:
            self.progress_indicator.max = len(os.listdir(input_dir))

    def execute(self):
        files = os.listdir(self.input_dir)
        for file in files:
            self.function(file, self.output_dir, self.metadata)
            if self.progress_indicator != None:
                self.progress_indicator.next()
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
