import time
import random

from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import sentry_sdk


sentry_sdk.init(
    dsn="https://24c99a4e92742cb8748a7645b2d11e9b@o4505132345917440.ingest.us.sentry.io/4506864686858240",
    enable_tracing=True,
)


app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route("/one")
@metrics.do_not_track()
@metrics.counter('counter_status', 'Request latencies by status',
                 labels={'status': lambda r: r.status_code})
def first_route():
    time.sleep(random.random() * 0.2)
    return "ok"


@app.route("/error")
def hello_world():
    1/0
    return "<p>error!</p>"


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, threaded=True)
