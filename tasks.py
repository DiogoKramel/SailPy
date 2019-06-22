import os
import redis
from celery import Celery

from functions import optimization_platypus_vpp


celery_app = Celery("Celery App", broker=os.environ['REDIS_URL'])
redis_instance = redis.StrictRedis.from_url(os.environ['REDIS_URL'])

REDIS_HASH_NAME = os.environ.get("DASH_APP_NAME", "app-data")
REDIS_KEYS = {"DATASET": "DATASET", "DATE_UPDATED": "DATE_UPDATED"}


@celery_app.task
def optimize_appendages(offspringsplatypus, gamethod, windspeedrange, windanglerange):
    optimization_platypus_vpp(offspringsplatypus, gamethod, windspeedrange, windanglerange)
        
        
    '''
    # Save the dataframe in redis so that the Dash app, running on a separate
    # process, can read it
    redis_instance.hset(
        REDIS_HASH_NAME,
        REDIS_KEYS["DATASET"],
        json.dumps(
            df.to_dict(),
            # This JSON Encoder will handle things like numpy arrays
            # and datetimes
            cls=plotly.utils.PlotlyJSONEncoder,
        ),
    )
    # Save the timestamp that the dataframe was updated
    redis_instance.hset(
        REDIS_HASH_NAME, REDIS_KEYS["DATE_UPDATED"], str(datetime.datetime.now())
    )
    '''