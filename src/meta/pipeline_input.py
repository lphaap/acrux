class PipelineInputMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (
                hasattr(subclass, 'publish_input') and
                callable(subclass.publish_input) and

                hasattr(subclass, 'start') and
                callable(subclass.start) and

                hasattr(subclass, 'stop') and
                callable(subclass.stop) and

                hasattr(subclass, 'pause') and
                callable(subclass.pause) and

                hasattr(subclass, 'is_active') and
                callable(subclass.stop) and

                hasattr(subclass, 'active')
            )

class PipelineInput(metaclass=PipelineInputMeta):
    pass
