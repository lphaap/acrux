from src.pipelineRunner import PipelineRunner
from src.meta.controllable import Controllable
from src.meta.pipelineInput import PipelineInput
from src.meta.pipelineFilter import PipelineFilter
from multiprocessing.connection import Connection
from multiprocessing import Process, Pipe
from dataclasses import dataclass
from threading import Thread
from typing import List

import src.utils.logger as logger;

@dataclass
class PipelineProcess:
    runner: PipelineRunner
    connection: Connection
    process: Process

class PipelineManager(Controllable):

    def __init__(self, input: PipelineInput.__class__):
        logger.log("PipelineManager: init")
        self.input = input(self)
        self.pipelines = []
        self.active = False

    def createPipeline(self, filters: List[PipelineFilter]):
        parentConnection, childConnection = Pipe()

        runner = PipelineRunner(filters, childConnection)
        process = Process(target=runner.start)

        self.pipelines.append(
            PipelineProcess(runner, parentConnection, process)
        )

    def process(self, data):
        for pipeline in self.pipelines:
            pipeline.connection.send(data)

    def listen(self, connection):
        logger.log(self.active)
        while self.active:
            logger.log("PipelineManager: Listening process")
            data = connection.recv()
            try:
                # Stop called by child thread
                if data['stop']:
                    self.stop()
            except:
                continue

    def start(self):
        logger.log("PipelineManager: start")
        self.active = True;

        if len(self.pipelines) <= 0:
            raise Exception("PipelineManager: No pipelines setup")

        for pipeline in self.pipelines:
            logger.log("PipelineManager: Creating process")
            pipeline.process.start()
            listener = Thread(
                target=self.listen,
                args=(pipeline.connection,)
            )
            listener.start()

        self.input.start();

    def stop(self):
        if not self.active:
            return

        self.active = False;

        logger.log("PipelineManager: stop")
        for pipeline in self.pipelines:
            if pipeline.process.is_alive():
                pipeline.connection.send( {'stop': True} )

        self.input.stop();

    def isActive(self):
        return self.active;
