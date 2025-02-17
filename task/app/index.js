const express = require('express');
const { Client } = require('pg');
const redis = require('redis');

const app = express();
const port = 3000;

// PostgreSQL client setup
const dbClient = new Client({
  user: process.env.DB_USER,
  host: process.env.DB_HOST,
  database: process.env.DB_NAME,
  password: process.env.DB_PASSWORD,
  port: 5432,
});

// Redis client setup
const redisClient = redis.createClient({
  url: `redis://${process.env.REDIS_HOST}:6379`,
});

// Connect to PostgreSQL
dbClient.connect()
  .then(() => console.log('Connected to PostgreSQL'))
  .catch(err => console.error('PostgreSQL connection error', err));

// Connect to Redis
redisClient.connect()
  .then(() => console.log('Connected to Redis'))
  .catch(err => console.error('Redis connection error', err));

// Simple route
app.get('/', async (req, res) => {
  try {
    // Increment a counter in Redis
    const count = await redisClient.incr('counter');

    // Fetch data from PostgreSQL
    const result = await dbClient.query('SELECT NOW() as now');
    const dbTime = result.rows[0].now;

    res.send(`
      <h1>Hello from Docker Compose!</h1>
      <p>Redis Counter: ${count}</p>
      <p>PostgreSQL Time: ${dbTime}</p>
    `);
  } catch (err) {
    res.status(500).send(`Error: ${err.message}`);
  }
});

// Start the server
app.listen(port, () => {
  console.log(`App running on http://localhost:${port}`);
});
