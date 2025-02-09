# Import the time module to handle time-related operations (e.g., adding delays)
import time

# Import the redis module to interact with a Redis database
import redis

# Import the Flask class from the flask module to create a web application
from flask import Flask

# Create an instance of the Flask class. The __name__ argument helps Flask determine the root path.
app = Flask(__name__)

# Create a connection to the Redis server.
# - host='redis': Specifies the hostname of the Redis server (typically 'redis' in Docker Compose setups).
# - port=6379: Specifies the port Redis is running on (6379 is the default port for Redis).
cache = redis.Redis(host='redis', port=6379)

# Define a function to get and increment the hit count stored in Redis.
def get_hit_count():
    # Set the number of retry attempts to 5 in case of connection errors.
    retries = 5

    # Start an infinite loop to keep trying the operation until it succeeds or retries are exhausted.
    while True:
        try:
            # Increment the value of the key 'hits' in Redis by 1 and return the new value.
            # If the key doesn't exist, Redis creates it with an initial value of 0 before incrementing.
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            # If a ConnectionError occurs (e.g., Redis is unavailable), handle it here.
            if retries == 0:
                # If all retries are exhausted, raise the exception to stop the program.
                raise exc
            # Decrement the retry counter by 1.
            retries -= 1
            # Pause the program for 0.5 seconds before retrying the connection.
            time.sleep(0.5)

# Define a route for the root URL ('/').
# When a user visits the root URL, Flask calls the hello() function.
@app.route('/')
def hello():
    # Call the get_hit_count() function to get the current value of the 'hits' counter from Redis.
    count = get_hit_count()

    # Return a response to the client. The f-string allows embedding the value of 'count' directly into the string.
    return f'Hello World! I have been seen {count} times.\n'

# This block ensures the Flask app runs only if the script is executed directly (not imported as a module).
if __name__ == '__main__':
    # Run the Flask app on all available IPs (0.0.0.0) and port 5000.
    app.run(host='0.0.0.0', port=5000)
