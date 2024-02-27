import os


class Config:
    HOST_URL = os.getenv("HOST_URL", 'http://cortexone-396161853.us-east-1.elb.amazonaws.com/')


config = Config()
