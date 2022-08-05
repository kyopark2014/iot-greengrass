# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from random import gauss

class DummySensor(object):
    def __init__(self, mean=25, variance=1):
        self.mu = mean
        self.sigma = variance
        
    def read_value(self):
        return float("%.2f" % (gauss(1000, 20)))

if __name__ == '__main__':
    sensor = DummySensor()
    print(sensor.read_value())
