from typing import List
from progress.bar import Bar
from progress.counter import Counter
import warnings
import timeit
import os

#Stage represents a stage in the video pipeline
class stage:
    def __init__(self, name, output_dir, function, **metadata):
        self.name = name
        self.output_dir = output_dir
        self.function = function
        self.metadata = metadata
        self.progress_indicator = None
        if not os.path.exists(output_dir):
            warnings.warn(f"Directory: {output_dir} does not exist, creating now")
            os.mkdir(output_dir)

    def set_input_dir(self, input_dir: str) -> None:
        self.input_dir = input_dir
        if not os.path.exists(input_dir):
             warnings.warn(f"Directory: {input_dir} does not exist, creating now")
             os.mkdir(input_dir)
        if self.progress_indicator != None:
            self.progress_indicator.max = len(os.listdir(input_dir))

    def add_progress_bar(self):
        self.progress_indicator = Bar(self.name, max=len(os.listdir(self.input_dir)))

    def execute(self):
        for _ in self.function(self.input_dir, self.output_dir, self.metadata):
            if self.progress_indicator != None:
                self.progress_indicator.next()

#File_stage is a pipeline stage that only operates on 1 file
class file_stage(stage):
    def add_progress_bar(self):
        self.progress_indicator = Counter(self.name)
    
    def execute(self):
        next(self.function(self.input_dir, self.output_dir, self.metadata))

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

    def execute(self, time: bool, progress: bool) -> str:
        for (i, stage) in enumerate(self.stages):
            if progress:
                stage.add_progress_bar()
            if time:
                start = timeit.default_timer()
                stage.execute()
                print(timeit.default_timer() - start)
            else:
                stage.execute()
            if progress:
                print(f"Stage {stage.name} completed. {i+1}/{len(self.stages)}")
        return self.stages[-1].output_dir

        print("================================")
        print("Pipeline completed")
