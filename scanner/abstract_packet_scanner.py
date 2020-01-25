"""
This provides an abstract class that handles flow/congestion control
(in a very basic manner) and that can be used to build a network scanner.
"""

import time

TIMEOUT = 5
SLEEP = 1 / 256

class AbstractPacketScanner:
    def __init__(self, timeout = TIMEOUT, sleep = SLEEP):
        self.timeout = timeout
        self.sleep = sleep

    def __should_abort(self, timeout_start):
        if timeout_start:
            return (time.time() - timeout_start) > self.timeout
        else:
            return False

    def scan(self, targets, *args):
        results = set()
        targets_iter = iter(targets)
        timeout_start = None

        while not self.__should_abort(timeout_start):
            # if we're not finished sending all the packets
            if timeout_start is None:
                try:
                    # send the next packet
                    self.send_packet(next(targets_iter), *args)
                except StopIteration:
                    # no packets left, start the timeout
                    timeout_start = time.time()

            time.sleep(self.sleep)

            for res in self.receive_packets(*args):
                results.add(res)

                # check if we should abort so we don't get stuck
                # inside this loop because more data keeps coming in
                if self.__should_abort(timeout_start):
                    break
        
        return results

    def send_packet(self, target, *args):
        raise NotImplementedError()

    def receive_packets(self, *args):
        raise NotImplementedError()
