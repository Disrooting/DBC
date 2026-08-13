from queue import Queue


class UIQueue:

    def __init__(self):

        self.queue = Queue()

    def call(

        self,

        func,

        *args,

        **kwargs

    ):

        self.queue.put(

            (

                func,

                args,

                kwargs

            )

        )

    def process(self):

        while not self.queue.empty():

            func, args, kwargs = self.queue.get()

            func(

                *args,

                **kwargs

            )